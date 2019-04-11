import pytest

from async_property import async_cached_property, AsyncPropertyException, AsyncCachedPropertyLoader


pytestmark = pytest.mark.asyncio


class MyModel(AsyncCachedPropertyLoader):
    @async_cached_property
    async def foo(self):
        return 'bar'


async def test_loader():
    instance = await MyModel()
    assert hasattr(instance, '_foo')
    assert instance.foo == 'bar'


async def test_field():
    instance = MyModel()
    assert not hasattr(instance, '_foo')
    assert await instance.foo == 'bar'
    assert hasattr(instance, '_foo')


async def test_not_awaited():
    instance = MyModel()
    assert not hasattr(instance, '_foo')
    with pytest.raises(AsyncPropertyException):
        assert instance.foo


async def test_awaited_repeated():
    instance = MyModel()
    with pytest.raises(AsyncPropertyException):
        assert instance.foo == 'bar'
    assert await instance.foo == 'bar'
    assert instance.foo == 'bar'
    assert await instance.foo == 'bar'


async def test_default_setter():
    instance = MyModel()
    assert not hasattr(instance, '_foo')
    instance.foo = 'abc'
    assert hasattr(instance, '_foo')
    assert instance.foo == 'abc'


class ModelWithSetter(AsyncCachedPropertyLoader):
    @async_cached_property
    async def foo(self):
        return 'bar'

    @foo.setter
    def foo(self, value):
        self._foo = value
        self._bar = '123'


async def test_async_property_with_setter():
    instance = await ModelWithSetter()
    assert hasattr(instance, '_foo')
    assert hasattr(instance, '_bar')
    assert instance.foo == 'bar'
    assert instance._bar == '123'


class MyModelWithMultiple(AsyncCachedPropertyLoader):
    @async_cached_property
    async def first(self):
        return 123

    @async_cached_property
    async def second(self):
        return 456


async def test_multiple_loaders():
    instance = await MyModelWithMultiple()
    assert instance.first == 123
    assert instance.second == 456


async def test_multiple_fields():
    instance = MyModelWithMultiple()
    assert await instance.first == 123

    with pytest.raises(AsyncPropertyException):
        assert instance.second

    assert await instance.second == 456
