FROM python:3.9-slim-buster
# https://hub.docker.com/_/python

# Install deps
RUN apt-get update \
    && apt-mark auto $(apt-mark showinstall) \
    && apt-get install -y postgresql-client-11 python3-pip \
    && apt autoremove \
    && apt -y full-upgrade \
    && rm -rf /var/lib/apt \
    && python3 -m pip install -U pip \
    && python3 -m pip install poetry

WORKDIR /PyInventory

COPY . .

RUN poetry install --extras "postgres"


