import pytest

from async_property import async_property
from async_property.base import AsyncPropertyDescriptor
from async_property.proxy import AwaitableOnly

pytestmark = pytest.mark.asyncio


class MyModel:
    @async_property
    async def foo(self) -> str:
        return 'bar'


async def test_descriptor():
    assert isinstance(MyModel.foo, AsyncPropertyDescriptor)
    assert MyModel.foo.__name__ == 'foo'
    assert MyModel.foo.__annotations__['return'] == str


async def test_property():
    instance = MyModel()
    assert isinstance(instance.foo, AwaitableOnly)
    assert await instance.foo == 'bar'


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


async def test_sync_error():
    with pytest.raises(AssertionError):
        class MyModel:
            @async_property
            def foo(self):
                return 'bar'
