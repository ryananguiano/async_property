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

    $ pip install async-property


Or if you have pipenv:

.. code-block:: console

    $ pipenv install async-property


Usage
-----

You can use ``@async_property`` just as you would with ``@property``, but on an async function.

.. code-block:: python

    class Foo:
        @async_property
        async def remote_value(self):
            return await get_remote_value()

The property ``remote_value`` now returns an awaitable coroutine.

.. code-block:: python

    instance = Foo()
    await instance.remote_value


Cached Properties
~~~~~~~~~~~~~~~~~

``@async_cached_property`` will call the function only once. Subsequent awaits to the property will return a cached value.

.. code-block:: python

    class Foo:
        @async_cached_property
        async def value(self):
            print('loading value')
            return 123

    >>> instance = Foo()
    >>> instance.value
    <AwaitableOnly "Foo.value">
    >>> await instance.value
    loading value
    123
    >>> await instance.value
    123
    >>> instance.value
    123

    >>> instance.value = 'abc'
    >>> await instance.value
    'abc'

    >>> del instance.value
    >>> await instance.value
    loading value
    123


AwaitLoader
~~~~~~~~~~~

If you have an object with multiple cached properties, you can subclass ``AwaitLoader``. This will make your class instances awaitable and will load all ``@async_cached_property`` fields concurrently.

.. code-block:: python


    class Foo(AwaitLoader):
        @async_cached_property
        async def db_lookup(self):
            return 'success'

        @async_cached_property
        async def api_call(self):
            return 'works every time'

    >>> instance = await Foo()
    >>> instance.db_lookup
    'success'
    >>> instance.api_call
    'works every time'

Features
--------

* Both regular and cached property.
* Cached properties can be accessed multiple times without repeating function call.
* Cached properties use asyncio.Lock to ensure function is only called once.
* AwaitLoader will call ``await instance.load()``, if it exists, before loading properties.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


The ObjectProxy_ class was taken from wrapt_ library by Graham Dumpleton.

.. _ObjectProxy: https://github.com/GrahamDumpleton/wrapt/blob/master/src/wrapt/wrappers.py
.. _wrapt: https://github.com/GrahamDumpleton/wrapt
