import pytest

from async_property import async_cached_property
from async_property.cached import AsyncCachedPropertyDescriptor
from async_property.proxy import AwaitableOnly, AwaitableProxy

pytestmark = pytest.mark.asyncio


class MyModel:
    @async_cached_property
    async def foo(self) -> str:
        return 'bar'


async def test_descriptor():
    assert isinstance(MyModel.foo, AsyncCachedPropertyDescriptor)
    assert MyModel.foo.__name__ == 'foo'
    assert MyModel.foo.__annotations__['return'] == str


async def test_field():
    instance = MyModel()
    assert isinstance(instance.foo, AwaitableOnly)
    assert await instance.foo == 'bar'
    assert hasattr(instance, '_foo')


async def test_awaited_repeated():
    instance = MyModel()
    assert await instance.foo == 'bar'
    assert isinstance(instance.foo, AwaitableProxy)
    assert instance.foo == 'bar'
    assert await instance.foo == 'bar'


async def test_default_setter():
    instance = MyModel()
    instance.foo = 'abc'
    assert hasattr(instance, '_foo')
    assert instance.foo == 'abc'


async def test_default_deleter():
    instance = MyModel()
    await instance.foo
    assert hasattr(instance, '_foo')
    del instance.foo
    assert not hasattr(instance, '_foo')


class ModelWithSetterDeleter:
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
    instance = ModelWithSetterDeleter()
    instance.foo = 'abc'
    assert instance.foo == 'abc'
    assert await instance.foo == 'abc'
    assert hasattr(instance, '_foo')
    assert hasattr(instance, '_bar')
    assert instance._bar == '123'


async def test_async_property_with_deleter():
    instance = ModelWithSetterDeleter()
    await instance.foo
    assert hasattr(instance, '_foo')
    assert hasattr(instance, '_bar')
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
