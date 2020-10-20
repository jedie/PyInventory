SHELL := /bin/bash
MAX_LINE_LENGTH := 119
POETRY_VERSION := $(shell poetry --version 2>/dev/null)
COMPOSE_VERSION := $(shell poetry run docker-compose --version 2>/dev/null)

help: ## List all commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9 -]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

check-poetry:
	@if [[ "${POETRY_VERSION}" == *"Poetry"* ]] ; \
	then \
		echo "Found ${POETRY_VERSION}, ok." ; \
	else \
		echo 'Please install poetry first, with e.g.:' ; \
		echo 'make install-poetry' ; \
		exit 1 ; \
	fi

install-poetry: ## install or update poetry
	@if [[ "${POETRY_VERSION}" == *"Poetry"* ]] ; \
	then \
		echo 'Update poetry v$(POETRY_VERSION)' ; \
		poetry self update ; \
	else \
		echo 'Install poetry' ; \
		curl -sSL "https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py" | python3 ; \
	fi

install: check-poetry ## install PyInventory via poetry
	poetry install

manage-update: ## Collectstatic + makemigration + migrate
	./manage.sh collectstatic --noinput --link
	./manage.sh makemigrations
	./manage.sh migrate

update: check-poetry ## update the sources and installation
	git fetch --all
	git pull origin master
	poetry update

lint: ## Run code formatters and linter
	poetry run flynt --fail-on-change --line_length=${MAX_LINE_LENGTH} .
	poetry run isort --check-only .
	poetry run flake8 .

fix-code-style: ## Fix code formatting
	poetry run flynt --line_length=${MAX_LINE_LENGTH} .
	poetry run pyupgrade --exit-zero-even-if-changed --py3-plus --py36-plus --py37-plus `find . -name "*.py" -type f -not -path "./.tox/*"`
	poetry run isort .
	poetry run autopep8 --aggressive --aggressive --in-place --recursive .

tox-listenvs: check-poetry ## List all tox test environments
	poetry run tox --listenvs

tox: check-poetry ## Run pytest via tox with all environments
	poetry run tox

tox-py36: check-poetry ## Run pytest via tox with *python v3.6*
	poetry run tox -e py36

tox-py37: check-poetry ## Run pytest via tox with *python v3.7*
	poetry run tox -e py37

tox-py38: check-poetry ## Run pytest via tox with *python v3.8*
	poetry run tox -e py38

pytest: check-poetry ## Run pytest
	poetry run pytest

update-rst-readme: ## update README.rst from README.creole
	poetry run update_rst_readme

publish: ## Release new version to PyPi
	poetry run publish


run-dev-server:  ## Run the django dev server in endless loop.
	./manage.sh runserver

messages: ## Make and compile locales message files
	./manage.sh makemessages --all --no-location --no-obsolete
	./manage.sh compilemessages

run-server:  ## Run the gunicorn server in endless loop.
	poetry run inventory run-server

backup:  ## Backup everything
	poetry run inventory backup

create-starter:  ## Create starter file.
	poetry run inventory create-starter

##############################################################################
# docker-compose usage


check-compose:
	@if [[ "${COMPOSE_VERSION}" == *"docker-compose version"* ]] ; \
	then \
		echo "Found ${COMPOSE_VERSION}, ok." ; \
	else \
		echo 'Please install extras first, with e.g.:' ; \
		echo 'make install-compose' ; \
		exit 1 ; \
	fi

install-compose: check-poetry  ## Install "docker-compose", too
	poetry install --extras "docker"

up: check-compose  ## Start containers via docker-compose
	./compose.sh up -d
	./compose.sh logs --tail=500 --follow

down:  ## Stop all containers
	./compose.sh down

prune:  ## Cleanup docker
	docker system prune --force --all --filter until=4464h

build: check-compose  ## Update docker container build
	./compose.sh build --pull

init_postgres:  ## Create postgres database
	./compose.sh exec postgres ./docker/postgres_init.sh

##############################################################################

docker_createsuperuser:  ## Create super user
	./compose.sh exec inventory ./manage.sh createsuperuser

shell_inventory:  ## Go into bash shell in inventory container
	./compose.sh exec inventory /bin/bash

shell_postgres:  ## Go into bash shell in postgres container
	./compose.sh exec postgres /bin/bash

##############################################################################

logs:  ## Display docker logs from all containers
	./compose.sh logs --tail=500 --follow

logs_postgres:  ## Display docker logs from postgres container
	./compose.sh logs --tail=500 --follow postgres

logs_inventory:  ## Display docker logs from postgres container
	./compose.sh logs --tail=500 --follow inventory

##############################################################################

restart: down up  ## Restart all containers

upgrade_inventory: ## Upgrade "inventory" container and restart it
	$(MAKE) build
	./compose.sh stop inventory
	$(MAKE) up

reload_inventory: ## Reload server in "inventory" container
	./compose.sh exec inventory ./docker/kill_python.sh
	./compose.sh logs --tail=500 --follow inventory

.PHONY: help install lint fix test publish