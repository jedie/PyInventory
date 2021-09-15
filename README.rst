===========
PyInventory
===========

Web based management to catalog things including state and location etc. using Python/Django.

The project is in an early stage of development. Some things are already implemented and usable. But there is still a lot to do.

Pull requests welcome!

+---------------------------------+-----------------------------------------+
| |Build Status on github|        | `github.com/jedie/PyInventory/actions`_ |
+---------------------------------+-----------------------------------------+
| |Coverage Status on codecov.io| | `codecov.io/gh/jedie/PyInventory`_      |
+---------------------------------+-----------------------------------------+

.. |Build Status on github| image:: https://github.com/jedie/PyInventory/workflows/test/badge.svg?branch=master
.. _github.com/jedie/PyInventory/actions: https://github.com/jedie/PyInventory/actions
.. |Coverage Status on codecov.io| image:: https://codecov.io/gh/jedie/PyInventory/branch/master/graph/badge.svg
.. _codecov.io/gh/jedie/PyInventory: https://codecov.io/gh/jedie/PyInventory

-----
about
-----

The focus of this project is on the management of retro computing hardware.

Plan:

* Web-based

* Multiuser ready

* Chaotic warehousing

    * Grouped "Storage": Graphics card is in computer XY

* Data structure kept as general as possible

* You should be able to add the following to the items:

    * Storage location

    * State

    * Pictures and Files

    * URLs

    * receiving and delivering (when, from whom, at what price, etc.)

    * Information: Publicly visible yes/no

* A public list of existing items (think about it, you can set in your profile if you want to)

* administration a wish & exchange list

any many more... ;)

-----------------
Project structure
-----------------

There are two main directories:

+---------------------+--------------------------------------------+
| directory           | description                                |
+=====================+============================================+
| **`/src/`_**        | The main PyInventory source code           |
+---------------------+--------------------------------------------+
| **`/deployment/`_** | deploy PyInventory for production use case |
+---------------------+--------------------------------------------+

.. _/src/: https://github.com/jedie/PyInventory/tree/master/src
.. _/deployment/: https://github.com/jedie/PyInventory/tree/master/deployment

-------
install
-------

There exists these kind of installation/usage:

* local development installation using poetry

* production use with docker-compose on a root server

* Install as `YunoHost <https://yunohost.org>`_ App via `pyinventory_ynh <https://github.com/YunoHost-Apps/pyinventory_ynh>`_

This README contains only the information about local development installation.

Read `/deployment/README <https://github.com/jedie/PyInventory/tree/master/deployment#readme>`_ for instruction to install PyInventory on a root server.

local development installation
==============================

e.g.:

::

    # Clone project (Use your fork SSH url!):
    ~$ git clone https://github.com/jedie/PyInventory.git
    ~$ cd PyInventory
    ~/PyInventory$ ./devshell.py

Helpful for writing and debugging unittests is to run a local test server.
e.g.:

::

    ~/PyInventory$ ./devshell.py run_testserver

The web page is available via: ``http://127.0.0.1:8000/``

You can also pass a other port number or ``ipaddr:port`` combination. See: ``./devshell.py run_testserver --help``

Call manage commands from test project, e.g.:

::

    ~/PyInventory$ ./devshell.py manage --help

local docker dev run
====================

You can run the deployment docker containers with current source code with:

::

    ~/PyInventory$ make run-docker-dev-server

Just hit Cntl-C to stop the containers

The web page is available via: ``https://localhost/``

-----------
Screenshots
-----------

|PyInventory v0.2.0 screenshot 1.png|

.. |PyInventory v0.2.0 screenshot 1.png| image:: https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory v0.2.0 screenshot 1.png

----

|PyInventory v0.1.0 screenshot 2.png|

.. |PyInventory v0.1.0 screenshot 2.png| image:: https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory v0.1.0 screenshot 2.png

----

|PyInventory v0.1.0 screenshot 3.png|

.. |PyInventory v0.1.0 screenshot 3.png| image:: https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory v0.1.0 screenshot 3.png

----

------------------
Multi user support
------------------

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

|normal user example|

.. |normal user example| image:: https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory normal user example.png

------------------------------
Backwards-incompatible changes
------------------------------

v0.7.0
======

Docker-Compose usage: The MEDIA files was not stored on a docker volumes.

You should backup rhe media files **before** update the containers!

e.g.:

::

    ~/PyInventory/deployment$ make shell_inventory
    root@inventory:/django# cp -Rfv /media/ /django_volumes/media/

The files are stored locally here:

::

    ~/PyInventory/deployment$ ls -la volumes/django/media/

Now, update the containers and copy the files back.

v0.5.0
======

Git branches "master" and "deployment" was merged into one.
Files are separated into: "/src/" and "/development/"

-------
history
-------

* `compare v0.9.3...master <https://github.com/jedie/PyInventory/compare/v0.9.3...master>`_ **dev** 

    * tbc

* `v0.9.3 - 15.09.2021 <https://github.com/jedie/PyInventory/compare/v0.9.2...v0.9.3>`_ 

    * Optimize "items" changelist queries

    * Update requirements

    * Expand ``run_testserver`` command and recognize address and port argument

* `v0.9.2 - 11.05.2021 <https://github.com/jedie/PyInventory/compare/v0.9.1...v0.9.2>`_ 

    * Update requirements

    * `Fix error handling if item link is broken <https://github.com/jedie/PyInventory/issues/50>`_

* `v0.9.1 - 28.04.2021 <https://github.com/jedie/PyInventory/compare/v0.9.0...v0.9.1>`_

* NEW: Besides images, it's now possible to add file(s) to items, too.

* Add a auto login if Django dev. server is used.

* `v0.9.0 - 11.04.2021 <https://github.com/jedie/PyInventory/compare/v0.8.4...v0.9.0>`_ 

    * Use `https://github.com/jedie/dev-shell <https://github.com/jedie/dev-shell>`_ for development

* `v0.8.4 - 19.01.2021 <https://github.com/jedie/PyInventory/compare/v0.8.3...v0.8.4>`_ 

    * Search items in change list by "kind" and "tags", too

    * update requirements

* `v0.8.3 - 29.12.2020 <https://github.com/jedie/PyInventory/compare/v0.8.2...v0.8.3>`_ 

    * update requirements

    * remove colorama from direct dependencies

    * Small project setup changes

* `v0.8.2 - 20.12.2020 <https://github.com/jedie/PyInventory/compare/v0.8.1...v0.8.2>`_ 

    * Bugfix `#33 <https://github.com/jedie/PyInventory/issues/33>`_: Upload images to new created Items

* `v0.8.1 - 09.12.2020 <https://github.com/jedie/PyInventory/compare/v0.8.0...v0.8.1>`_ 

    * Fix migration: Don't create "/media/migrate.log" if there is nothing to migrate

    * Fix admin redirect by using the url pattern name

    * YunoHost app package created

    * update requirements

* `v0.8.0 - 06.12.2020 <https://github.com/jedie/PyInventory/compare/v0.7.0...v0.8.0>`_ 

    * Outsource the "MEDIA file serve" part into `django.tools.serve_media_app <https://github.com/jedie/django-tools/tree/master/django_tools/serve_media_app#readme>`_

* `v0.7.0 - 23.11.2020 <https://github.com/jedie/PyInventory/compare/v0.6.0...v0.7.0>`_ 

    * Change deployment setup:

        * Replace uwsgi with gunicorn

        * make deploy setup more generic by renaming "inventory" to "django"

        * Bugfix MEDIA path: store the files on a docker volumes

        * run app server as normal user and not root

        * pull all docker images before build

* `v0.6.0 - 15.11.2020 <https://github.com/jedie/PyInventory/compare/v0.5.0...v0.6.0>`_ 

    * User can store images to every item: The image can only be accessed by the same user.

* `v0.5.0 - 14.11.2020 <https://github.com/jedie/PyInventory/compare/v0.4.2...v0.5.0>`_ 

    * Merge separate git branches into one: "/src/" and "/development/" `#19 <https://github.com/jedie/PyInventory/issues/19>`_

* `v0.4.2 - 13.11.2020 <https://github.com/jedie/PyInventory/compare/v0.4.1...v0.4.2>`_ 

    * Serve static files by Caddy

    * Setup CKEditor file uploads: Store files into random sub directory

    * reduce CKEditor plugins

* `v0.4.1 - 2.11.2020 <https://github.com/jedie/PyInventory/compare/v0.4.0...v0.4.1>`_ 

    * Small bugfixes

* `v0.4.0 - 1.11.2020 <https://github.com/jedie/PyInventory/compare/v0.3.2...v0.4.0>`_ 

    * Move docker stuff and production use information into separate git branch

    * Add django-axes: keeping track of suspicious logins and brute-force attack blocking

    * Add django-processinfo: collect information about the running server processes

* `v0.3.2 - 26.10.2020 <https://github.com/jedie/PyInventory/compare/v0.3.0...v0.3.2>`_ 

    * Bugfix missing translations

* `v0.3.0 - 26.10.2020 <https://github.com/jedie/PyInventory/compare/v0.2.0...v0.3.0>`_ 

    * setup production usage:

        * Use `caddy server <https://caddyserver.com/>`_ as reverse proxy

        * Use uWSGI as application server

        * autogenerate ``secret.txt`` file for ``settings.SECRET_KEY``

        * Fix settings

    * split settings for local development and production use

    * Bugfix init: move "setup user group" from checks into "post migrate" signal handler

    * Bugfix for using manage commands ``dumpdata`` and ``loaddata``

* `v0.2.0 - 24.10.2020 <https://github.com/jedie/PyInventory/compare/v0.1.0...v0.2.0>`_ 

    * Simplify item change list by nested item

    * Activate Django-Import/Export

    * Implement multi user usage

    * Add Django-dbbackup

    * Add docker-compose usage

* `v0.1.0 - 17.10.2020 <https://github.com/jedie/PyInventory/compare/v0.0.1...v0.1.0>`_ 

    * Enhance models, admin and finish project setup

* v0.0.1 - 14.10.2020

    * Just create a pre-alpha release to save the PyPi package name ;)

-----
links
-----

+----------+------------------------------------------+
| Homepage | `http://github.com/jedie/PyInventory`_   |
+----------+------------------------------------------+
| PyPi     | `https://pypi.org/project/PyInventory/`_ |
+----------+------------------------------------------+

.. _http://github.com/jedie/PyInventory: http://github.com/jedie/PyInventory
.. _https://pypi.org/project/PyInventory/: https://pypi.org/project/PyInventory/

Discuss here:

* `vogons.org Forum Thread (en) <https://www.vogons.org/viewtopic.php?f=5&t=77285>`_

* `Python-Forum (de) <https://www.python-forum.de/viewtopic.php?f=9&t=50024>`_

* `VzEkC e. V. Forum Thread (de) <https://forum.classic-computing.de/forum/index.php?thread/21738-opensource-projekt-pyinventory-web-basierte-verwaltung-um-seine-dinge-zu-katalog/>`_

* `dosreloaded.de Forum Thread (de) <https://dosreloaded.de/forum/index.php?thread/3702-pyinventory-retro-sammlung-katalogisieren/>`_

--------
donation
--------

* `paypal.me/JensDiemer <https://www.paypal.me/JensDiemer>`_

* `Flattr This! <https://flattr.com/submit/auto?uid=jedie&url=https%3A%2F%2Fgithub.com%2Fjedie%2FPyInventory%2F>`_

* Send `Bitcoins <http://www.bitcoin.org/>`_ to `1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F <https://blockexplorer.com/address/1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F>`_

------------

``Note: this file is generated from README.creole 2021-09-15 21:11:45 with "python-creole"``