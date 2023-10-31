from time import perf_counter
from os import getenv
from contextlib import asynccontextmanager
from asyncio import gather

import structlog
from fastapi import FastAPI, Request, Response
from asgi_correlation_id.context import correlation_id
from asgi_correlation_id import CorrelationIdMiddleware
from uvicorn.protocols.utils import get_path_with_query_string

from src.tbot import dp, bot
from src.logger import setup_logging


LOG_LEVEL = getenv("LOG_LEVEL", "INFO")
setup_logging(log_level=LOG_LEVEL)
logger = structlog.stdlib.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    gather(dp.start_polling(bot, skip_updates=True, handle_signals=False))

    yield

    await dp.stop_polling()
    await bot.session.close()


app = FastAPI(lifespan=lifespan)


# Settings up custom middleware for logs.
@app.middleware("http")
async def logging_middleware(request: Request, call_next) -> Response:
    access_logger = structlog.stdlib.get_logger("api.access")
    structlog.contextvars.clear_contextvars()
    # These context vars will be added to all log entries emitted during the request
    request_id = correlation_id.get()
    structlog.contextvars.bind_contextvars(request_id=request_id)

    start_time = perf_counter()
    # If the call_next raises an error, we still want to return our own 500 response,
    # so we can add headers to it (process time, request ID...)
    response = Response(status_code=500)
    try:
        response = await call_next(request)
    except Exception:
        # TODO: Validate that we don't swallow exceptions (unit test?)
        structlog.stdlib.get_logger("api.error").exception("Uncaught exception")
        raise
    finally:
        process_time = perf_counter() - start_time
        status_code = response.status_code
        url = get_path_with_query_string(request.scope)
        client_host = request.client.host
        client_port = request.client.port
        http_method = request.method
        http_version = request.scope["http_version"]
        # Recreate the Uvicorn access log format, but add all parameters as structured information
        access_logger.info(
            f"""{client_host}:{client_port} - "{http_method} {url} HTTP/{http_version}" {status_code}""",
            network={"client": {"ip": client_host, "port": client_port}},
            duration=process_time,
        )
        response.headers["X-Process-Time"] = str(process_time)
        return response

app.add_middleware(CorrelationIdMiddleware)