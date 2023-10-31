FROM python:3.11.1-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
ADD . /app/
RUN apt update -y
RUN apt install lsb-release wget gnupg2 -y
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt update -y
RUN apt install postgresql-client -y
RUN pip install --no-cache-dir --upgrade pip pipenv
RUN pipenv install --system --deploy --ignore-pipfile
ENTRYPOINT [ "/bin/bash" ]
CMD [ "./entrypoint.sh" ]