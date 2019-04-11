import pytest

from async_property import async_cached_property, AwaitLoader


pytestmark = pytest.mark.asyncio


class MyModel(AwaitLoader):
    @async_cached_property
    async def foo(self):
        return 'bar'


async def test_loader():
    instance = await MyModel()
    assert hasattr(instance, '_foo')
    assert instance.foo == 'bar'


async def test_delayed_field():
    instance = MyModel()
    coro = instance.foo
    await instance
    assert instance.foo == 'bar'
    assert await coro == 'bar'


class LoadCalledException(Exception):
    pass


class MyModelWithLoad(AwaitLoader):
    async def load(self):
        raise LoadCalledException


async def test_call_load():
    with pytest.raises(LoadCalledException):
        await MyModelWithLoad()
