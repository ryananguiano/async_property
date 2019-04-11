==============
async_property
==============


.. image:: https://img.shields.io/pypi/v/async_property.svg
        :target: https://pypi.python.org/pypi/async_property

.. image:: https://img.shields.io/travis/ryananguiano/async_property.svg
        :target: https://travis-ci.org/ryananguiano/async_property

.. image:: https://readthedocs.org/projects/async-property/badge/?version=latest
        :target: https://async-property.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/ryananguiano/async_property/shield.svg
     :target: https://pyup.io/repos/github/ryananguiano/async_property/
     :alt: Updates


Python decorator for async properties.

* Free software: MIT license
* Documentation: https://async-property.readthedocs.io.

Install
-------

To install async_property, run this command in your terminal:

.. code-block:: console

    $ pip install async_property


Or if you have pipenv:

.. code-block:: console

    $ pipenv install async_property


Usage
-----

You can use ``@async_property`` just as you would with ``@property``, but on a async function.

.. code-block:: python

    class Foo:
        @async_property
        async def remote_value(self):
            return await get_remote_value()

The property ``remote_value`` now returns an awaitable coroutine.

.. code-block:: python

    instance = Foo()
    await instance.remote_value


Features
--------

* Both regular and cached property.
* Cached properties can be accessed multiple times without repeating function.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


The ObjectProxy_ class was taken from wrapt_ library by Graham Dumpleton.

.. _ObjectProxy: https://github.com/GrahamDumpleton/wrapt/blob/master/src/wrapt/wrappers.py
.. _wrapt: https://github.com/GrahamDumpleton/wrapt
