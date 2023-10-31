======================================================
Django REST Framework extensions by Amsterdam Datapunt
======================================================

Extensions to Django REST Framework by Amsterdam Datapunt. Amsterdam Datapunt
provides access to municipal data through, at times, public APIs. This project
provides some basic classes and instructions to set the behavior
of Django REST Framework API to the standards of Amsterdam Datapunt.

Installation instructions
--------------------------

Given that you have a Django project that generates a REST API using Django
REST Framework:

.. code-block:: sh
    pip install drf_amsterdam

To use the API page styling provided by this package you must add it to the
Django settings file in INSTALLED_APPS, ahead of 'rest_framework' so that the
templates and static files included in drf_amsterdam override those included
with Django REST Framework.

Running tests
-------------

Run the tests in a virtualenv and run the script runtests.py from project root.

requirements: spatialite, sqlite extension

or user the docker-compose [TODO]

Make Release
------------

use
.. code-block:: sh
    bumpversion [major, minor, patch]

to tag the branch.

.. code-block:: sh
    make dist
    make release

passwords are in the passwords safes.
