#!/bin/sh

set -ex

exec poetry run docker-compose "$@"
