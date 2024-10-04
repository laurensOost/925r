# Pull base image
FROM python:3.9-slim-bookworm as builder

# Install python project dependencies pre-requisites
RUN apt-get update && \
    apt-get install -y libldap2-dev libsasl2-dev libssl-dev && \
    apt-get install -y gcc default-libmysqlclient-dev pkg-config

# Copy Pipfile dependency list
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# Install pipenv
RUN set -ex && pip install --upgrade pip && pip install pipenv

# Update the Pipfile.lock
RUN set -ex && pipenv lock

# Install dependencies
COPY requirements.txt requirements.txt
RUN set -ex && pip install -r requirements.txt && pipenv install --deploy --system

FROM builder AS final
WORKDIR /code