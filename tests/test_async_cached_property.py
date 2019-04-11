import pytest

from async_property import async_cached_property, AsyncPropertyException
from async_property.cached import AsyncCachedPropertyDescriptor
from async_property.proxy import AwaitableOnly, AwaitableProxy

pytestmark = pytest.mark.asyncio


class MyModel:
    @async_cached_property
    async def foo(self):
        return 'bar'


async def test_descriptor():
    assert isinstance(MyModel.foo, AsyncCachedPropertyDescriptor)


async def test_field():
    instance = MyModel()
    assert isinstance(instance.foo, AwaitableOnly)
    assert await instance.foo == 'bar'
    assert hasattr(instance, '_foo')


async def test_not_awaited():
    instance = MyModel()
    with pytest.raises(AsyncPropertyException):
        assert instance.foo
    assert not hasattr(instance, '_foo')


async def test_awaited_repeated():
    instance = MyModel()
    with pytest.raises(AsyncPropertyException):
        assert instance.foo == 'bar'
    assert await instance.foo == 'bar'
    assert isinstance(instance.foo, AwaitableProxy)
    assert instance.foo == 'bar'
    assert await instance.foo == 'bar'


async def test_default_setter():
    instance = MyModel()
    assert not hasattr(instance, '_foo')
    instance.foo = 'abc'
    assert hasattr(instance, '_foo')
    assert instance.foo == 'abc'


async def test_default_deleter():
    instance = MyModel()
    assert not hasattr(instance, '_foo')
    await instance.foo
    assert hasattr(instance, '_foo')
    assert instance.foo == 'bar'
    del instance.foo
    assert not hasattr(instance, '_foo')


class ModelWithSetter:
    @async_cached_property
    async def foo(self):
        return 'bar'

    @foo.setter
    def foo(self, value):
        self._foo = value
        self._bar = '123'

    @foo.deleter
    def foo(self):
        del self._foo
        del self._bar


async def test_async_property_with_setter():
    instance = ModelWithSetter()
    instance.foo = 'abc'
    assert instance.foo == 'abc'
    assert await instance.foo == 'abc'
    assert hasattr(instance, '_foo')
    assert hasattr(instance, '_bar')
    assert instance._bar == '123'


async def test_async_property_with_deleter():
    instance = ModelWithSetter()
    assert await instance.foo == 'bar'
    assert hasattr(instance, '_foo')
    assert hasattr(instance, '_bar')
    assert instance._bar == '123'
    del instance.foo
    assert not hasattr(instance, '_foo')
    assert not hasattr(instance, '_bar')


class MyModelWithMultiple:
    @async_cached_property
    async def first(self):
        return 123

    @async_cached_property
    async def second(self):
        return 456


async def test_multiple_fields():
    instance = MyModelWithMultiple()
    assert await instance.first == 123
    assert await instance.second == 456
