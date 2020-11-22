FROM python:3.9-slim-buster
# https://hub.docker.com/_/python

ARG XDG_CACHE_HOME
ENV XDG_CACHE_HOME=${XDG_CACHE_HOME}

# Install deps
RUN apt-get update \
    && apt-mark auto $(apt-mark showinstall) \
    && apt-get install -y postgresql-client-11 python3-pip \
    && apt autoremove \
    && apt -y full-upgrade \
    && rm -rf /var/lib/apt \
    && python3 -m pip install -U pip \
    && pip install -U psycopg2-binary

RUN addgroup --system django \
    && adduser --system --no-create-home --disabled-password --ingroup django --shell /bin/bash django

WORKDIR /django

RUN pip install "pyinventory>=0.6.0"


