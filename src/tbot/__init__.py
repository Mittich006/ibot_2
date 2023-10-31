import os
import importlib.util

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from src.config import settings

bot = Bot(token=settings.TELEGRAM_BOT_API_KEY, parse_mode=ParseMode.HTML)
dp = Dispatcher()


# Get the current package path
package_path = os.path.dirname(__file__)

# Dynamically import modules from subdirectories
for foldername, _, filenames in os.walk(package_path):
    for filename in filenames:
        if filename.endswith(".py") and not filename.startswith("__init__"):
            # Construct the full module name
            module_name = f"src.tbot.{os.path.relpath(os.path.join(foldername, filename), package_path)[:-3].replace(os.sep, '.')}"
            try:
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(foldername, filename))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Add functions/classes from the module to the dp object
                for name in dir(module):
                    func = getattr(module, name)
                    if callable(func):
                        dp.register_message_handler(func)

            except Exception as e:
                print(f"Error importing module '{module_name}': {e}")