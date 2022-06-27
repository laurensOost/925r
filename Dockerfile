# Pull base image
FROM python:3.8-slim-buster as builder

# install python project dependencies pre-requisites
RUN apt-get update && \
    apt-get install -y python-dev libldap2-dev libsasl2-dev libssl-dev && \
    apt-get install -y gcc default-libmysqlclient-dev

# Set environment variables
COPY requirements.txt requirements.txt

# Install pipenv
RUN set -ex && pip install --upgrade pip

# Install dependencies
RUN set -ex && pip install -r requirements.txt

FROM builder as final
WORKDIR /code
COPY . /app/

RUN set -ex && bash -c "eval $(grep 'PYTHONDONTWRITEBYTECODE' .env)"
RUN set -ex && bash -c "eval $(grep 'PYTHONUNBUFFERED' .env)"