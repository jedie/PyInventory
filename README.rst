===========
PyInventory
===========

Web based management to catalog things including state and location etc. using Python/Django.

Current status: Just start the project. Nothing is done, nothing is useable, yet ;)

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

-------
install
-------

tbd

::

    ~$ git clone https://github.com/jedie/PyInventory.git
    ~$ cd PyInventory
    ~/PyInventory$ make
    help                 List all commands
    install-poetry       install or update poetry
    install              install PyInventory via poetry
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
    run-server           Run the gunicorn server in endless loop.
    backup               Backup everything
    create-starter       Create starter file.
    ~/PyInventory$ make install
    ...

-----------
Screenshots
-----------

|PyInventory v0.1.0 screenshot 1.png|

.. |PyInventory v0.1.0 screenshot 1.png| image:: https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory v0.1.0 screenshot 1.png

----

|PyInventory v0.1.0 screenshot 2.png|

.. |PyInventory v0.1.0 screenshot 2.png| image:: https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory v0.1.0 screenshot 2.png

----

|PyInventory v0.1.0 screenshot 3.png|

.. |PyInventory v0.1.0 screenshot 3.png| image:: https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory v0.1.0 screenshot 3.png

----

------------------------------
Backwards-incompatible changes
------------------------------

Nothing, yet ;)

-------
history
-------

* `compare v0.1.0...master <https://github.com/jedie/PyInventory/compare/v0.1.0...master>`_ **dev** 

    * tbc

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

--------
donation
--------

* `paypal.me/JensDiemer <https://www.paypal.me/JensDiemer>`_

* `Flattr This! <https://flattr.com/submit/auto?uid=jedie&url=https%3A%2F%2Fgithub.com%2Fjedie%2FPyInventory%2F>`_

* Send `Bitcoins <http://www.bitcoin.org/>`_ to `1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F <https://blockexplorer.com/address/1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F>`_

------------

``Note: this file is generated from README.creole 2020-10-17 22:30:59 with "python-creole"``