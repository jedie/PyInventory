===========
PyInventory
===========

Web based management to catalog things including state and location etc. using Python/Django.

The project is in an early stage of development. Some things are already implemented and usable. But there is still a lot to do.

Pull requests welcome!

+-----------------------------------+-------------------------------------------------+
| |Build Status on github|          | `github.com/jedie/PyInventory/actions`_         |
+-----------------------------------+-------------------------------------------------+
| |Build Status on travis-ci.org|   | `travis-ci.org/jedie/PyInventory`_              |
+-----------------------------------+-------------------------------------------------+
| |Coverage Status on codecov.io|   | `codecov.io/gh/jedie/PyInventory`_              |
+-----------------------------------+-------------------------------------------------+
| |Coverage Status on coveralls.io| | `coveralls.io/r/jedie/PyInventory`_             |
+-----------------------------------+-------------------------------------------------+
| |Status on landscape.io|          | `landscape.io/github/jedie/PyInventory/master`_ |
+-----------------------------------+-------------------------------------------------+

.. |Build Status on github| image:: https://github.com/jedie/PyInventory/workflows/test/badge.svg?branch=master
.. _github.com/jedie/PyInventory/actions: https://github.com/jedie/PyInventory/actions
.. |Build Status on travis-ci.org| image:: https://travis-ci.org/jedie/PyInventory.svg
.. _travis-ci.org/jedie/PyInventory: https://travis-ci.org/jedie/PyInventory/
.. |Coverage Status on codecov.io| image:: https://codecov.io/gh/jedie/PyInventory/branch/master/graph/badge.svg
.. _codecov.io/gh/jedie/PyInventory: https://codecov.io/gh/jedie/PyInventory
.. |Coverage Status on coveralls.io| image:: https://coveralls.io/repos/jedie/PyInventory/badge.svg
.. _coveralls.io/r/jedie/PyInventory: https://coveralls.io/r/jedie/PyInventory
.. |Status on landscape.io| image:: https://landscape.io/github/jedie/PyInventory/master/landscape.svg
.. _landscape.io/github/jedie/PyInventory/master: https://landscape.io/github/jedie/PyInventory/master

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

    * Pictures

    * URLs

    * receiving and delivering (when, from whom, at what price, etc.)

    * Information: Publicly visible yes/no

* A public list of existing items (think about it, you can set in your profile if you want to)

* administration a wish & exchange list

any many more... ;)

------------
git branches
------------

Currently we have two main branches:

+-------------------+----------------------------------------------------------------+
| git branch        | description                                                    |
+===================+================================================================+
| **`master`_**     | The main PyInventory source code                               |
+-------------------+----------------------------------------------------------------+
| **`deployment`_** | separate project to deploy PyInventory for production use case |
+-------------------+----------------------------------------------------------------+

.. _master: https://github.com/jedie/PyInventory/tree/master
.. _deployment: https://github.com/jedie/PyInventory/tree/deployment

-------
install
-------

There exists two kind of installation/usage:

* local development installation using poetry

* production use with docker-compose

This README (in git **master** branch) contains only the information about local develompment installation.

Read `deployment README <https://github.com/jedie/PyInventory/tree/deployment#readme>`_ for instruction to install PyInventory on a root server.

prepare
=======

::

    ~$ git clone https://github.com/jedie/PyInventory.git
    ~$ cd PyInventory
    ~/PyInventory$ make
    help                 List all commands
    install-poetry       install or update poetry
    install              install PyInventory via poetry
    manage-update        Collectstatic + makemigration + migrate
    update               update the sources and installation
    lint                 Run code formatters and linter
    fix-code-style       Fix code formatting
    tox-listenvs         List all tox test environments
    tox                  Run pytest via tox with all environments
    tox-py36             Run pytest via tox with *python v3.6*
    tox-py37             Run pytest via tox with *python v3.7*
    tox-py38             Run pytest via tox with *python v3.8*
    pytest               Run pytest
    update-rst-readme    update README.rst from README.creole
    publish              Release new version to PyPi
    run-dev-server       Run the django dev server in endless loop.
    messages             Make and compile locales message files
    run-server           Run the gunicorn server in endless loop.
    backup               Backup everything
    create-starter       Create starter file.
    dbbackup             Backup database
    dbrestore            Restore a database backup

local development installation
==============================

::

    # install or update Poetry:
    ~/PyInventory$ make install-poetry
    
    # install PyInventory via poetry:
    ~/PyInventory$ make install
    ...
    
    # Collectstatic + makemigration + migrate:
    ~/PyInventory$ make manage-update
    
    # Create a django super user:
    ~/PyInventory$ ./manage.sh createsuperuser
    
    # start local dev. web server:
    ~/PyInventory$ make run-dev-server

The web page is available via: ``http://127.0.0.1:8000/``

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

Nothing, yet ;)

-------
history
-------

* `compare v0.4.1...master <https://github.com/jedie/PyInventory/compare/v0.4.1...master>`_ **dev** 

    * tbc

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

``Note: this file is generated from README.creole 2020-11-02 09:12:38 with "python-creole"``