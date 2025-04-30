# PyInventory

Web based management to catalog things including state and location etc. using Python/Django.
Store information in WYSIWYG-HTML-Editor field and tag them and add Files, Images and Links to them.

[![tests](https://github.com/jedie/PyInventory/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jedie/PyInventory/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/PyInventory/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/PyInventory)
[![PyInventory @ PyPi](https://img.shields.io/pypi/v/PyInventory?label=PyInventory%20%40%20PyPi)](https://pypi.org/project/PyInventory/)
[![Python Versions](https://img.shields.io/pypi/pyversions/PyInventory)](https://github.com/jedie/PyInventory/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/PyInventory)](https://github.com/jedie/PyInventory/blob/main/LICENSE)

[![Install PyInventory with YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=pyinventory)

> [pyinventory_ynh](https://github.com/YunoHost-Apps/pyinventory_ynh) allows you to install PyInventory quickly and simply on a YunoHost server. If you don't have YunoHost, please consult [the guide](https://yunohost.org/#/install) to learn how to install it.

Pull requests welcome!

## about

The focus of this project is on the management of retro computing hardware.

Current features:


* Web-based
* Multiuser ready (Every user see and manage only his own entries)
* Chaotic warehousing
  * Grouped "Items" e.g.: Graphics card Foo is in computer Bar
* Data structure kept as general as possible
* Manage information to every item:
  * Description: free WYSIWYG-HTML-Editor field
  * Storage location
  * State
  * Images, Files and Web-Links
  * receiving and delivering (when, from whom, at what price, etc.)
* Manage "Memos" (Information independent of item/location):
  * A free WYSIWYG-HTML-Editor field
  * Tags
  * Images, Files and Web-Links

Future ideas:


* Information: Publicly visible yes/no
  * A public list of existing items (think about it, you can set in your profile if you want to)
  * administration a wish & exchange list

any many more... ;)




## Screenshots

More screenshots are here: [jedie.github.io/tree/master/screenshots/PyInventory](https://github.com/jedie/jedie.github.io/blob/master/screenshots/PyInventory/README.creole)

![PyInventory v0.2.0 screenshot 1.png](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory%20v0.2.0%20screenshot%201.png "PyInventory v0.2.0 screenshot 1.png")

----

![PyInventory v0.11.0 screenshot memo 1.png](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory%20v0.11.0%20screenshot%20memo%201.png "PyInventory v0.11.0 screenshot memo 1.png")

----

![PyInventory v0.1.0 screenshot 2.png](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory%20v0.1.0%20screenshot%202.png "PyInventory v0.1.0 screenshot 2.png")

----

![PyInventory v0.1.0 screenshot 3.png](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory%20v0.1.0%20screenshot%203.png "PyInventory v0.1.0 screenshot 3.png")

----

## Multi user support

PyInventory supports multiple users. The idea:


* Every normal user sees only his own created database entries
* All users used the Django admin

Note: All created Tags are shared for all existing users!

So setup a normal user:


* Set "Staff status"
* Unset "Superuser status"
* Add user to "normal_user" group
* Don't add any additional permissions

e.g.:

![normal user example](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory%20normal%20user%20example.png "normal user example")

More screenshots are here: [jedie.github.io/tree/master/screenshots/PyInventory](https://github.com/jedie/jedie.github.io/blob/master/screenshots/PyInventory/README.creole)


## local development installation

e.g.:
```
# Clone project (Use your fork SSH url!):
~$ git clone https://github.com/jedie/PyInventory.git
~$ cd PyInventory
~/PyInventory$ ./manage.py
```

Helpful for writing and debugging unittests is to run a local test server.
e.g.:
```
~/PyInventory$ ./manage.py run_dev_server
```

The web page is available via: `http://127.0.0.1:8000/`

You can also pass a other port number or `ipaddr:port` combination. See: `./manage.py run_dev_server --help`

Run tests, e.g.:
```
~/PyInventory$ ./manage.py test
~/PyInventory$ ./manage.py coverage
~/PyInventory$ ./manage.py tox
```

Install Playwright browsers, e.g.:
```
~/PyInventory$ .venv/bin/playwright install
```

Run only Playwright tests with the Playwright Inspector, e.g.:
```
~/PyInventory$ PWDEBUG=1 ./manage.py test --tag playwright
```


## Backwards-incompatible changes

### v0.19.0

* Remove ["/development/"](https://github.com/jedie/PyInventory/tree/v0.18.1/deployment) (unmaintained "docker-compose" installation),
please use YunoHost ;)
* Removed `django-processinfo` and `django-axes` in test project.
* Remove `poetry`, `pytest` and `devshell`
* Use `pip-tools`, `unittests` and [manage_django_project](https://github.com/jedie/manage_django_project)

### v0.20

Because of security reasons, the `ckeditor` package was replaced by `prose-editor`.

In 0.20.1 we switched to https://github.com/jazzband/django-tinymce/ because `prose-editor` has no table support.

## Make new release

We use [cli-base-utilities](https://github.com/jedie/cli-base-utilities#generate-project-history-base-on-git-commitstags) to generate the history in this README.


To make a new release, do this:

* Increase your project version number
* Run tests to update the README
* commit the changes
* Create release


## history

[comment]: <> (✂✂✂ auto generated history start ✂✂✂)

* [v0.21.1rc1](https://github.com/jedie/PyInventory/compare/v0.21.0...v0.21.1rc1)
  * 2025-05-01 - Replace setuptools with hatchling
  * 2025-04-30 - Update requirements and some small code parts
* [v0.21.0](https://github.com/jedie/PyInventory/compare/v0.20.1...v0.21.0)
  * 2025-03-23 - Bugfix publish: setuptools missing
  * 2025-03-23 - Migrate "pip-tools" -> "uv" and remove tox
* [v0.20.1](https://github.com/jedie/PyInventory/compare/v0.20.0...v0.20.1)
  * 2024-09-05 - switched to https://github.com/jazzband/django-tinymce/
* [v0.20.0](https://github.com/jedie/PyInventory/compare/v0.19.3...v0.20.0)
  * 2024-09-05 - Replace django-ckeditor with django-prose-editor and fix tests
  * 2024-09-05 - Project updates
  * 2024-01-16 - Use typeguard in tests
  * 2024-01-16 - Update requirements

<details><summary>Expand older history entries ...</summary>

* [v0.19.3](https://github.com/jedie/PyInventory/compare/v0.19.2...v0.19.3)
  * 2023-11-01 - Auto generate README history
  * 2023-11-01 - Update requirements
  * 2023-10-31 - Bugfix the "parent" field on location admin page
  * 2023-10-31 - Bugfix local test settings for development
  * 2023-10-08 - Use playwrigth manage command from manage-django-project
  * 2023-09-24 - Update test snapshot files
  * 2023-09-24 - Add playwright CLI wrapper command
* [v0.19.2](https://github.com/jedie/PyInventory/compare/v0.19.1...v0.19.2)
  * 2023-08-17 - Bugfix packaging by adding "requests" as normal dependencies
  * 2023-08-17 - Bugfix packageing by adding "requests" as normal dependencies
* [v0.19.1](https://github.com/jedie/PyInventory/compare/v0.19.0...v0.19.1)
  * 2023-08-17 - Update requirements
  * 2023-08-17 - Update from project template
* [v0.19.0](https://github.com/jedie/PyInventory/compare/v0.18.1...v0.19.0)
  * 2023-07-21 - Update README.md
  * 2023-07-21 - Migrate from "poetry-python" to "managed-django-project"
  * 2023-07-21 - Move source code from /src/
  * 2023-07-21 - Remove "/development/" - unmaintained "docker-compose" installation
  * 2023-07-21 - fix tox run
  * 2023-07-21 - Update to Django 4.2
  * 2023-07-21 - FIXME: Remove '_reorder_' from ItemModelAdmin.list_display
  * 2023-07-20 - Change item lust: move "producer" to first
* [v0.18.1](https://github.com/jedie/PyInventory/compare/v0.18.0...v0.18.1)
  * 2023-07-15 - Update requirements + fix test snapshot
  * 2023-06-11 - Update requirements
* [v0.18.0](https://github.com/jedie/PyInventory/compare/v0.17.0...v0.18.0)
  * 2023-04-04 - Apply manageprojects updates
  * 2022-12-22 - Bugfix missing static files by tagulous bug.
  * 2022-12-22 - Project updates
  * 2022-12-22 - Updat requirements
* [v0.17.0](https://github.com/jedie/PyInventory/compare/v0.16.0...v0.17.0)
  * 2022-10-03 - update requirements
  * 2022-10-03 - Check django-revision integration
  * 2022-09-30 - Enhance Location: Better change form and list all items in this location
  * 2022-09-30 - NEW: List number of item on `location` change list
  * 2022-09-30 - NEW: List all related objects on `item` change page with edit links.
  * 2022-09-30 - Validate current version via "packaging" as set it to v0.17.0rc0
  * 2022-09-30 - Add autocomplete fields to item
* [v0.16.0](https://github.com/jedie/PyInventory/compare/v0.15.0...v0.16.0)
  * 2022-09-13 - Bugfix missing CK-Editor
  * 2022-09-13 - Update devshell and skip broken poetry v1.2.0
  * 2022-09-04 - Update README.md
  * 2022-08-22 - Replace README.creole with README.md
  * 2022-08-22 - Bugfix wrong list in README.creole
  * 2022-08-29 - Update requirements
* [v0.15.0](https://github.com/jedie/PyInventory/compare/v0.14.0...v0.15.0)
  * 2022-08-18 - Use run_testserver and AlwaysLoggedInAsSuperUserMiddleware from django-tools
  * 2022-08-16 - Update requirements
  * 2022-07-28 - line_length = 100
  * 2022-07-28 - Add "./devsetup.py manage seed_data" command
  * 2022-07-28 - Better changelists for super users
  * 2022-07-28 - Speedup item change list by prefetch "location"
  * 2022-07-28 - fix project setup and "max line length" info
* [v0.14.0](https://github.com/jedie/PyInventory/compare/v0.13.1...v0.14.0)
  * 2022-07-21 - WIP: Fix #102 by store tree information for Item and Location
  * 2022-07-21 - Bugfix devshell "manage" command
* [v0.13.1](https://github.com/jedie/PyInventory/compare/v0.13.0...v0.13.1)
  * 2022-07-21 - Fix publishing
  * 2022-07-21 - Update to new devshell version
  * 2022-07-21 - Update requirements
  * 2022-06-29 - Fix coverage upload to codecov.io
  * 2022-06-29 - Expand Playwright tests and add a Item with Tag and Image
  * 2022-06-20 - Replace Selenium tests with Playwright
  * 2022-06-20 - Run tests with Python 3.10, too and update requirements
  * 2022-05-16 - Use assert_html_response_snapshot from bx_django_utils
  * 2022-05-16 - update pyproject.toml
  * 2022-02-05 - Code style: Lower line length to 100
  * 2022-02-05 - Fix devshell CLI run
  * 2022-02-05 - Remove seperate linting step (pytest run checks code style)
  * 2022-01-30 - Update README: "master" -> "main"
  * 2022-01-30 - Switch to darker code styler
* [v0.13.0](https://github.com/jedie/PyInventory/compare/v0.12.0...v0.13.0)
  * 2022-01-01 - Add devshell command: "update_test_snapshots"
  * 2021-12-05 - Update requirements
  * 2021-12-05 - Activate secure settings by default
  * 2021-12-05 - Test "manage.py check" in tests
  * 2021-12-05 - setup DEBUG in tests
  * 2021-11-24 - deprecate docker-compose production usage
  * 2021-11-24 - Added translations to Catalan and Spanish. Po files need to be compiled.
* [v0.12.0](https://github.com/jedie/PyInventory/compare/v0.11.0...v0.12.0)
  * 2021-11-22 - remove obsolete file
  * 2021-11-22 - Fix #75 protect overwriting a new version with a older one
  * 2021-11-20 - Update ci.yml
  * 2021-11-20 - Update requirements
  * 2021-11-20 - Bugfix tests by mock {% now "Z" %}
* [v0.11.0](https://github.com/jedie/PyInventory/compare/v0.10.1...v0.11.0)
  * 2021-10-09 - Update README
  * 2021-10-09 - NEW: Memo model/admin: Store Information independent of items/locations
  * 2021-10-09 - Fix CKEditor
* [v0.10.1](https://github.com/jedie/PyInventory/compare/v0.10.0...v0.10.1)
  * 2021-10-09 - Use new assert_html_snapshot() in bx_py_utils
  * 2021-10-09 - Make lest requests on save
  * 2021-10-09 - update README
  * 2021-10-09 - Update to Django 3.1.x
  * 2021-10-09 - Better tracebacks on html validation errors
  * 2021-10-09 - Compare HTML code in pretty format
* [v0.10.0](https://github.com/jedie/PyInventory/compare/v0.9.4...v0.10.0)
  * 2021-09-29 - Group item: default "automatic" mode and can be disabled by filter action
  * 2021-09-29 - Update requirements.
* [v0.9.4](https://github.com/jedie/PyInventory/compare/v0.9.3...v0.9.4)
  * 2021-09-15 - Pin psycopg < 2.9 because of https://github.com/psycopg/psycopg2/issues/1293
* [v0.9.3](https://github.com/jedie/PyInventory/compare/v0.9.2...v0.9.3)
  * 2021-09-15 - Update "django-tagulous" v1.2 -> v1.3
  * 2021-09-15 - Optimize "items" changelist queries
  * 2021-09-15 - Bugfix wrong translations
  * 2021-08-16 - Fix #56 "psycopg2-binary" not installable under ARM boards
  * 2021-08-16 - Update requirements
  * 2021-08-04 - Pass cli arguments to "run_testserver" command
* [v0.9.2](https://github.com/jedie/PyInventory/compare/v0.9.1...v0.9.2)
  * 2021-05-11 - Update requirements and README
  * 2021-05-10 - Bugfix #50 - Wrong exception logging
* [v0.9.1](https://github.com/jedie/PyInventory/compare/v0.9.0...v0.9.1)
  * 2021-04-28 - Release v0.9.1
  * 2021-04-28 - NEW: Add files to items.
  * 2021-04-28 - Add a auto login if Django dev. server is used
  * 2021-04-28 - Fix tests
  * 2021-04-28 - Delete manage.sh
  * 2021-04-28 - Fix manage call, again:
  * 2021-04-28 - Bugfix manage calls
  * 2021-04-28 - Update requirements
  * 2021-04-13 - Update own bootstrap file from dev-shell via tests
* [v0.9.0](https://github.com/jedie/PyInventory/compare/v0.8.4...v0.9.0)
  * 2021-04-11 - Update "deployment/project.env", too
  * 2021-04-11 - relase as v0.9.0
  * 2021-04-11 - fix gitignore
  * 2021-04-11 - Update devshell to v0.2.0
  * 2021-04-05 - Use https://github.com/jedie/dev-shell
* [v0.8.4](https://github.com/jedie/PyInventory/compare/v0.8.3...v0.8.4)
  * 2021-01-19 - update requirements
  * 2021-01-19 - Search items in change list by "kind" and "tags", too
  * 2020-12-29 - remove obsolete badges
* [v0.8.3](https://github.com/jedie/PyInventory/compare/v0.8.2...v0.8.3)
  * 2020-12-29 - remove colorama and update requirements
  * 2020-12-29 - +add info about running docker container
  * 2020-12-29 - update pip before call "poetry update"
  * 2020-12-29 - Just install poetry via pip
* [v0.8.2](https://github.com/jedie/PyInventory/compare/v0.8.1...v0.8.2)
  * 2020-12-20 - release v0.8.2
  * 2020-12-20 - Add tests for creating a new Item
  * 2020-12-20 - FIX #33 by set user before save the image
  * 2020-12-20 - Move get_queryset() to base class
  * 2020-12-20 - update requirements
  * 2020-12-20 - typo
* [v0.8.1](https://github.com/jedie/PyInventory/compare/v0.8.0...v0.8.1)
  * 2020-12-09 - 0.8.1rc2
  * 2020-12-09 - Update requirements
  * 2020-12-09 - update README and release as 0.8.1rc2
  * 2020-12-09 - Fix admin redirect by using the url pattern name and not hardcoded URL
  * 2020-12-07 - Fix migration: Don't create "/media/migrate.log" if there is nothing to migrate
* [v0.8.0](https://github.com/jedie/PyInventory/compare/v0.7.0...v0.8.0)
  * 2020-12-06 - release v0.8.0rc1
  * 2020-12-06 - Use "serve_media_app" to serve users uploads
  * 2020-12-06 - update requirements
* [v0.7.0](https://github.com/jedie/PyInventory/compare/v0.6.0...v0.7.0)
  * 2020-11-23 - bugfix tests
  * 2020-11-23 - 0.7.0rc2
  * 2020-11-23 - Replace .env with project.env
  * 2020-11-23 - Bugfix Dockerfile and installation of the project
  * 2020-11-23 - Set XDG_CACHE_HOME and PYTHONUNBUFFERED in Dockerfile
  * 2020-11-23 - cleanup docker-compose.dev.yml
  * 2020-11-23 - bugfix gateway problems: gunicorn must bind to "django:8000"
  * 2020-11-22 - move some gunicorn settings into gunicorn.conf.py
  * 2020-11-22 - Run gunicorn as "django" user and not as root
  * 2020-11-22 - setup gunicorn logs
  * 2020-11-22 - bugfix "make reload_django"
  * 2020-11-22 - fix "make shell_docker-dev-server"
  * 2020-11-22 - Bugfix media files: save them on a volume
  * 2020-11-22 - More generic deployment: rename "inventory" to "django"
  * 2020-11-22 - replace uwsgi with gunicorn
  * 2020-11-22 - pull before build
* [v0.6.0](https://github.com/jedie/PyInventory/compare/v0.5.0...v0.6.0)
  * 2020-11-15 - Bugfix file excluding for lint/format tools
  * 2020-11-15 - Add tests to uploaded user images
  * 2020-11-15 - remove appended slash to /media/ urls
  * 2020-11-15 - bugfix image __str__() im name is None
  * 2020-11-15 - update translations
  * 2020-11-15 - Store Images to Items
  * 2020-11-14 - Update deployment setup:
  * 2020-11-14 - add basic selenium tests
  * 2020-11-14 - activate pytest-parallel in "make pytest"
  * 2020-11-14 - use pytest-parallel
  * 2020-11-14 - Quote DB name and user
* [v0.5.0](https://github.com/jedie/PyInventory/compare/v0.4.2...v0.5.0)
  * 2020-11-14 - update "make update" and pull from master
  * 2020-11-14 - setup Caddy volumens for "data" and "config"
  * 2020-11-14 - Bugfix "make run-docker-dev-server" by clean dist
  * 2020-11-14 - Add "make run-docker-dev-server" for local docker test run
  * 2020-11-14 - Exclude docker volumes form pytest
  * 2020-11-14 - +"make createsuperuser"
  * 2020-11-14 - remove unused make targets
  * 2020-11-14 - Bugfix building the template dirs path
  * 2020-11-14 - cleanup
  * 2020-11-14 - Add "header" in Makefiles
  * 2020-11-14 - update deployment README
  * 2020-11-13 - remove obsolete yapf config
  * 2020-11-13 - move .isort.cfg into pyproject.toml
  * 2020-11-13 - add a note about https://gitlab.com/pycqa/flake8/-/issues/428
  * 2020-11-13 - move pytest.ini into pyproject.toml
  * 2020-11-13 - move tox.ini into pyproject.toml
  * 2020-11-13 - fix tox
  * 2020-11-13 - update requirements
  * 2020-11-13 - WIP: Fix project layout
  * 2020-11-13 - update path to meta files
  * 2020-11-13 - fix github action
  * 2020-11-13 - Start to update README
  * 2020-11-13 - setup .gitignore
  * 2020-11-13 - move stuff into /src/
  * 2020-11-13 - seperate pip installations
  * 2020-11-13 - Update default install
  * 2020-11-13 - Bugfix servind static files
  * 2020-11-11 - Don't generate migrations
  * 2020-11-11 - Serve static/media files by Caddy
  * 2020-11-11 - add "make reload_caddy"
  * 2020-11-11 - Bugfix Makefile help target
  * 2020-10-27 - +acpid
  * 2020-10-27 - Add scripts/apt-cleanup.sh
  * 2020-10-27 - Add some notes
  * 2020-10-27 - cleanup (call "docker system prune") after start
  * 2020-10-27 - update README
  * 2020-10-27 - add .dockerignore
  * 2020-10-27 - chmod +x
  * 2020-10-27 - add root server helper shell scripts
  * 2020-10-27 - update docker containers on "make update", too
  * 2020-10-27 - Update README.creole
  * 2020-10-26 - init deployment branch
* [v0.4.2](https://github.com/jedie/PyInventory/compare/v0.4.1...v0.4.2)
  * 2020-11-13 - fix code style
  * 2020-11-11 - update README
  * 2020-11-11 - reduce CKEditor plugins
  * 2020-11-11 - move dev scripts
  * 2020-11-11 - Setup CKEditor uploads
  * 2020-11-11 - Add settings.SERVE_FILES and serve static files only for local development
* [v0.4.1](https://github.com/jedie/PyInventory/compare/v0.4.0...v0.4.1)
  * 2020-11-02 - prepare v0.4.1 release
  * 2020-11-02 - update requirements
  * 2020-11-02 - change template context key: version_string -> inventory_version_string
* [v0.4.0](https://github.com/jedie/PyInventory/compare/v0.3.2...v0.4.0)
  * 2020-11-01 - Add Django-Processinfo
  * 2020-11-01 - test code lint via pytest
  * 2020-11-01 - fix code linting tests
  * 2020-11-01 - refactoring/fix tests
  * 2020-11-01 - add django-axes
  * 2020-10-27 - update README
  * 2020-10-27 - Cleanup: remove docker-compose stuff
  * 2020-10-27 - Add link to python-forum.de in README
* [v0.3.2](https://github.com/jedie/PyInventory/compare/v0.3.1...v0.3.2)
  * 2020-10-26 - v0.3.2: move translations
  * 2020-10-26 - move translations
* [v0.3.1](https://github.com/jedie/PyInventory/compare/v0.3.0...v0.3.1)
  * 2020-10-26 - rename /locale/ to /inventory_locales/ and include it in package
* [v0.3.0](https://github.com/jedie/PyInventory/compare/v0.2.0...v0.3.0)
  * 2020-10-26 - update README
  * 2020-10-26 - deny robots via Caddyfile
  * 2020-10-26 - deny robots via html meta
  * 2020-10-26 - "hide" information from login page
  * 2020-10-26 - use inventory_project.settings.local as fallback
  * 2020-10-25 - Bump version to v0.3.0
  * 2020-10-25 - Don't link static files: uWSGI reject the files ;)
  * 2020-10-25 - Use caddy with uWSGI in docker-compose usage
  * 2020-10-25 - Refactor settings
  * 2020-10-25 - Fix https://github.com/radiac/django-tagulous/issues/101
  * 2020-10-25 - write start information to stderr
  * 2020-10-25 - Bugfix init: move Database access from checks into post-migate signal
* [v0.2.0](https://github.com/jedie/PyInventory/compare/v0.1.0...v0.2.0)
  * 2020-10-24 - fix "make fix-code-style"
  * 2020-10-24 - Update README and prepare v0.2.0 release
  * 2020-10-24 - sort nestet items
  * 2020-10-24 - bugfix BaseUserOnlyModelForm
  * 2020-10-24 - "merge" nested items
  * 2020-10-24 - Make Location.description optional
  * 2020-10-24 - implement multi user usage
  * 2020-10-24 - Add Django dbbackup
  * 2020-10-24 - base activation of Django import/exort
  * 2020-10-24 - install new packages via docker entrypoint, too
  * 2020-10-24 - Speedup make usage
  * 2020-10-24 - update README
  * 2020-10-24 - exclude docker-compose "volumes" directory from code formatters and linters
  * 2020-10-24 - fix code style
  * 2020-10-24 - Update requirements
  * 2020-10-24 - add forum links to README
  * 2020-10-20 - Add docker-compose usage
* [v0.1.0](https://github.com/jedie/PyInventory/compare/v0.0.1...v0.1.0)
  * 2020-10-17 - Fix README.rst
  * 2020-10-17 - update screenshots
  * 2020-10-17 - bugfix link reversion error
  * 2020-10-17 - change Tag fields: case_sensitive=False, space_delimiter=False
  * 2020-10-17 - Setup Header with versionsnumber and footer link to github
  * 2020-10-17 - +test_update_rst_readme()
  * 2020-10-17 - remove obsolete MANIFEST.in file and include AUTHORS
  * 2020-10-17 - bugfix pyupgrade call: Exclude files form: .tox
  * 2020-10-17 - add project setup test
  * 2020-10-17 - Add test for missing migrations
  * 2020-10-17 - add migrations
  * 2020-10-17 - update translations
  * 2020-10-17 - enhance admin
  * 2020-10-17 - limit ItemModel.parent to "root"-Elements
  * 2020-10-17 - make ItemModel.description optional
  * 2020-10-17 - Enhance models and admin
  * 2020-10-17 - Add 'bx_py_utils' to INSTALLED_APPS to activate translations from this package
  * 2020-10-16 - Update README.creole
  * 2020-10-16 - update tests
  * 2020-10-16 - Add de/en translations
  * 2020-10-16 - Basic project usage:
  * 2020-10-16 - Don't prefix URLs with language_code
  * 2020-10-16 - print Django version, too
  * 2020-10-16 - fix CKeditor
  * 2020-10-16 - fix ignore static/media
  * 2020-10-16 - Use TimetrackingBaseModel from bx_py_utils
  * 2020-10-16 - use default template settings
  * 2020-10-16 - 'ckeditor/ckeditor/' -> 'ckeditor/'
  * 2020-10-16 - move static/media/sqlite into project root path
  * 2020-10-16 - fix code style
  * 2020-10-16 - bugfix isort config
  * 2020-10-16 - Test with python 3.7 - 3.9
  * 2020-10-16 - support python >=3.7,<4.0.0
  * 2020-10-16 - Minimal Django project setup
  * 2020-10-15 - update README
* [v0.0.1](https://github.com/jedie/PyInventory/compare/a2a59c3...v0.0.1)
  * 2020-10-14 - init

</details>


[comment]: <> (✂✂✂ auto generated history end ✂✂✂)

## links

|          |                                                                                |
|----------|--------------------------------------------------------------------------------|
| Homepage | [http://github.com/jedie/PyInventory](http://github.com/jedie/PyInventory)     |
| PyPi     | [https://pypi.org/project/PyInventory/](https://pypi.org/project/PyInventory/) |

Discuss here:


* [vogons.org Forum Thread (en)](https://www.vogons.org/viewtopic.php?f=5&t=77285)
* [Python-Forum (de)](https://www.python-forum.de/viewtopic.php?f=9&t=50024)
* [VzEkC e. V. Forum Thread (de)](https://forum.classic-computing.de/forum/index.php?thread/21738-opensource-projekt-pyinventory-web-basierte-verwaltung-um-seine-dinge-zu-katalog/)
* [dosreloaded.de Forum Thread (de)](https://dosreloaded.de/forum/index.php?thread/3702-pyinventory-retro-sammlung-katalogisieren/)

## donation


* [paypal.me/JensDiemer](https://www.paypal.me/JensDiemer)
* [Flattr This!](https://flattr.com/submit/auto?uid=jedie&url=https%3A%2F%2Fgithub.com%2Fjedie%2FPyInventory%2F)
* Send [Bitcoins](http://www.bitcoin.org/) to [1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F](https://blockexplorer.com/address/1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F)
