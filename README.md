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


## history


* [**dev**](https://github.com/jedie/PyInventory/compare/v0.19.2...main)
  * Bugfix the "parent" field on location admin page
  * tbc
* [v0.19.2 - 17.08.2023](https://github.com/jedie/PyInventory/compare/v0.19.1...v0.19.2)
  * Bugfix packaging and missing "requests" dependencies
* [v0.19.1 - 17.08.2023](https://github.com/jedie/PyInventory/compare/v0.19.0...v0.19.1)
  * Update requirements
* [v0.19.0 - 21.07.2023](https://github.com/jedie/PyInventory/compare/v0.18.1...v0.19.0)
  * Update to Django 4.2
  * Remove `django-processinfo`, `django-axes` and unmaintained "docker-compose" installation
  * Use `pip-tools`, `unittests` and [manage_django_project](https://github.com/jedie/manage_django_project)
  * Bugfix `ItemModelAdmin`
* [v0.18.1 - 15.06.2023](https://github.com/jedie/PyInventory/compare/v0.18.0...v0.18.1)
  * Update requirements
* [v0.18.0 - 04.04.2023](https://github.com/jedie/PyInventory/compare/v0.17.0...v0.18.0)
  * Bugfix missing static files by tagulous bug
  * Update requirements and project setup
* [v0.17.0 - 03.10.2022](https://github.com/jedie/PyInventory/compare/v0.16.0...v0.17.0)
  * NEW: List all related objects on `item` change page with edit links.
  * Change `parent` and `location` fields on `item` change page to a autocompele field.
  * Add search to `location`
  * NEW: List number of item on `location` change list
* [v0.16.0 - 14.09.2022](https://github.com/jedie/PyInventory/compare/v0.15.0...v0.16.0)
  * Update requirements
  * Bugfix missing CK-Editor
  * Replace Creole base README with markdown
  * Remove Docker stuff from README
* [v0.15.0 - 19.08.2022](https://github.com/jedie/PyInventory/compare/v0.14.0...v0.15.0)
  * Speedup item change list by prefetch "location"
  * Better changelists for super users
  * Add `./devsetup.py manage seed_data` command to fill the database for development
  * Update requirements
  * Update project setup
* [v0.14.0 - 24.07.2022](https://github.com/jedie/PyInventory/compare/v0.13.1...v0.14.0)
  * [Fix #102](https://github.com/jedie/PyInventory/issues/102) by remove limitation of item parents.
  * Remove "Group Items" functionality
  * Replace "Group Items" change list filter by "Limit tree depth" for Item and Location.
  * Display Item and Location as a tree.
* [v0.13.1 - 21.07.2022](https://github.com/jedie/PyInventory/compare/v0.13.0...v0.13.1)
  * Rename git "master" branch into "main"
  * Update CI/Test setup:
    * Use darker and pytest-darker as code formatter
    * Run tests with Python 3.10, too and update requirements
    * Replace Selenium tests with Playwright
* [v0.13.0 - 01.01.2022](https://github.com/jedie/PyInventory/compare/v0.12.0...v0.13.0)
  * [Update requirements, e.g.: Django v3.2](https://github.com/jedie/PyInventory/pull/83)
* [v0.12.0 - 22.11.2021](https://github.com/jedie/PyInventory/compare/v0.11.0...v0.12.0)
  * NEW: [Protect user to overwrite newer Item/Memo/Location with a older one (e.g.: in other browser TAB)](https://github.com/jedie/PyInventory/pull/78)
  * update requirements
* [v0.11.0 - 09.10.2021](https://github.com/jedie/PyInventory/compare/v0.10.1...v0.11.0)
  * NEW: Memo model/admin: Store Information (incl. images/files/links) independent of items/locations
  * Bugfix CKEditor sizes and fix toolbar (e.g.: remove useless pdf generator button and add sourcecode function)
* [v0.10.1 - 09.10.2021](https://github.com/jedie/PyInventory/compare/v0.10.0...v0.10.1)
  * Update to Django 3.1.x
  * Don't make requests to the a name for a Link, if we already have one or if last request was not long ago.
* [v0.10.0 - 29.09.2021](https://github.com/jedie/PyInventory/compare/v0.9.4...v0.10.0)
  * Group item: default "automatic" mode and can be disabled by filter action
* [v0.9.4 - 15.09.2021](https://github.com/jedie/PyInventory/compare/v0.9.3...v0.9.4)
  * Pin `psycopg < 2.9` because of [https://github.com/psycopg/psycopg2/issues/1293](https://github.com/psycopg/psycopg2/issues/1293)
* [v0.9.3 - 15.09.2021](https://github.com/jedie/PyInventory/compare/v0.9.2...v0.9.3)
  * Optimize "items" changelist queries
  * Update requirements
  * Expand `run_testserver` command and recognize address and port argument
* [v0.9.2 - 11.05.2021](https://github.com/jedie/PyInventory/compare/v0.9.1...v0.9.2)
  * Update requirements
  * [Fix error handling if item link is broken](https://github.com/jedie/PyInventory/issues/50)
* [v0.9.1 - 28.04.2021](https://github.com/jedie/PyInventory/compare/v0.9.0...v0.9.1)
* NEW: Besides images, it's now possible to add file(s) to items, too.
* Add a auto login if Django dev. server is used.
* [v0.9.0 - 11.04.2021](https://github.com/jedie/PyInventory/compare/v0.8.4...v0.9.0)
  * Use [https://github.com/jedie/dev-shell](https://github.com/jedie/dev-shell) for development
* [v0.8.4 - 19.01.2021](https://github.com/jedie/PyInventory/compare/v0.8.3...v0.8.4)
  * Search items in change list by "kind" and "tags", too
  * update requirements
* [v0.8.3 - 29.12.2020](https://github.com/jedie/PyInventory/compare/v0.8.2...v0.8.3)
  * update requirements
  * remove colorama from direct dependencies
  * Small project setup changes
* [v0.8.2 - 20.12.2020](https://github.com/jedie/PyInventory/compare/v0.8.1...v0.8.2)
  * Bugfix [#33](https://github.com/jedie/PyInventory/issues/33): Upload images to new created Items
* [v0.8.1 - 09.12.2020](https://github.com/jedie/PyInventory/compare/v0.8.0...v0.8.1)
  * Fix migration: Don't create "/media/migrate.log" if there is nothing to migrate
  * Fix admin redirect by using the url pattern name
  * YunoHost app package created
  * update requirements
* [v0.8.0 - 06.12.2020](https://github.com/jedie/PyInventory/compare/v0.7.0...v0.8.0)
  * Outsource the "MEDIA file serve" part into [django.tools.serve_media_app](https://github.com/jedie/django-tools/tree/master/django_tools/serve_media_app#readme)
* [v0.7.0 - 23.11.2020](https://github.com/jedie/PyInventory/compare/v0.6.0...v0.7.0)
  * Change deployment setup:
    * Replace uwsgi with gunicorn
    * make deploy setup more generic by renaming "inventory" to "django"
    * Bugfix MEDIA path: store the files on a docker volumes
    * run app server as normal user and not root
    * pull all docker images before build
* [v0.6.0 - 15.11.2020](https://github.com/jedie/PyInventory/compare/v0.5.0...v0.6.0)
  * User can store images to every item: The image can only be accessed by the same user.
* [v0.5.0 - 14.11.2020](https://github.com/jedie/PyInventory/compare/v0.4.2...v0.5.0)
  * Merge separate git branches into one: "/src/" and "/development/" [#19](https://github.com/jedie/PyInventory/issues/19)
* [v0.4.2 - 13.11.2020](https://github.com/jedie/PyInventory/compare/v0.4.1...v0.4.2)
  * Serve static files by Caddy
  * Setup CKEditor file uploads: Store files into random sub directory
  * reduce CKEditor plugins
* [v0.4.1 - 2.11.2020](https://github.com/jedie/PyInventory/compare/v0.4.0...v0.4.1)
  * Small bugfixes
* [v0.4.0 - 1.11.2020](https://github.com/jedie/PyInventory/compare/v0.3.2...v0.4.0)
  * Move docker stuff and production use information into separate git branch
  * Add django-axes: keeping track of suspicious logins and brute-force attack blocking
  * Add django-processinfo: collect information about the running server processes
* [v0.3.2 - 26.10.2020](https://github.com/jedie/PyInventory/compare/v0.3.0...v0.3.2)
  * Bugfix missing translations
* [v0.3.0 - 26.10.2020](https://github.com/jedie/PyInventory/compare/v0.2.0...v0.3.0)
  * setup production usage:
    * Use [caddy server](https://caddyserver.com/) as reverse proxy
    * Use uWSGI as application server
    * autogenerate `secret.txt` file for `settings.SECRET_KEY`
    * Fix settings
  * split settings for local development and production use
  * Bugfix init: move "setup user group" from checks into "post migrate" signal handler
  * Bugfix for using manage commands `dumpdata` and `loaddata`
* [v0.2.0 - 24.10.2020](https://github.com/jedie/PyInventory/compare/v0.1.0...v0.2.0)
  * Simplify item change list by nested item
  * Activate Django-Import/Export
  * Implement multi user usage
  * Add Django-dbbackup
  * Add docker-compose usage
* [v0.1.0 - 17.10.2020](https://github.com/jedie/PyInventory/compare/v0.0.1...v0.1.0)
  * Enhance models, admin and finish project setup
* v0.0.1 - 14.10.2020
  * Just create a pre-alpha release to save the PyPi package name ;)

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
