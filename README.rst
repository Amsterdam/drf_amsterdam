======================================================
Django REST Framework extensions by Amsterdam Datapunt
======================================================

Extenstions to Django REST Framework by Amsterdam Datapunt. Amsterdam Datapunt
provides access to municipal data through, at times public, APIs. This project
drf_amsterdam provides some basic classes and instructions to set the behavior
of Django REST Framework API to the standards of Amsterdam Datapunt.

Installlation instructions
--------------------------

Given that you have a Django project that generates a REST API using Django
REST Framework:

```
pip install drf_amsterdam
```

To use the API page styling provided by this package you must add it to the
Django settings file in INSTALLED_APPS, ahead of 'rest_framework' so that the
templates and static files included in drf_amsterdam override those included
with Django REST Framework.

Running tests
-------------

Run the tests in a virtualenv and run the script runtests.py from project root.

requirements: spatialite, sqllite extension

or user the docker-compose [TODO]

Make Release
------------

use bumpversion [major, minor, patch] to tag the branch.

make dist
make release. passwords are in the passwords safes.
