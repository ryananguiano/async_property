import pytest

from async_property import async_property, AsyncPropertyException
from async_property.base import AsyncPropertyDescriptor
from async_property.proxy import AwaitableOnly

pytestmark = pytest.mark.asyncio


class MyModel:
    @async_property
    async def foo(self):
        return 'bar'


async def test_descriptor():
    assert isinstance(MyModel.foo, AsyncPropertyDescriptor)


async def test_property():
    instance = MyModel()
    assert isinstance(instance.foo, AwaitableOnly)
    assert await instance.foo == 'bar'


async def test_no_await():
    instance = MyModel()
    with pytest.raises(AsyncPropertyException):
        assert instance.foo == 'bar'


async def test_multiple_calls():
    instance = MyModel()
    assert await instance.foo == 'bar'
    assert await instance.foo == 'bar'


async def test_setter():
    instance = MyModel()
    with pytest.raises(ValueError):
        instance.foo = 'abc'


async def test_deleter():
    instance = MyModel()
    with pytest.raises(ValueError):
        del instance.foo
