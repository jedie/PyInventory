FROM python:3.9-slim-buster
# https://hub.docker.com/_/python

# Install deps
RUN apt-get update \
    && apt-mark auto $(apt-mark showinstall) \
    && apt-get install -y postgresql-client-11 python3-pip \
    && apt autoremove \
    && apt -y full-upgrade \
    && rm -rf /var/lib/apt \
    && python3 -m pip install -U pip

WORKDIR /inventory

RUN pip install psycopg2-binary "pyinventory>=0.4.2"


