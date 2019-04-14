import pytest
from async_property import async_cached_property, AwaitLoader

pytestmark = pytest.mark.asyncio


class MyModel(AwaitLoader):
    @async_cached_property
    async def foo(self):
        return 'bar'


async def test_empty_instance():
    assert await AwaitLoader()


async def test_loader():
    instance = await MyModel()
    assert 'foo' in instance.__async_property__.cache
    assert instance.foo == 'bar'


async def test_delayed_field():
    instance = MyModel()
    coro = instance.foo
    await instance
    assert instance.foo == 'bar'
    assert await coro == 'bar'


async def test_delayed_field_with_setter():
    instance = MyModel()
    coro = instance.foo
    await instance
    assert instance.foo == 'bar'
    instance.foo = 'abc'
    assert await coro == 'abc'


async def test_empty_instance_loaders():
    assert AwaitLoader._async_property_loaders == ()


async def test_instance_loaders():
    assert MyModel._async_property_loaders == (
        ('foo', MyModel.foo.get_loader),
    )


class MyModelWithLoad(AwaitLoader):
    async def load(self):
        self.loaded = True


async def test_call_load():
    instance = await MyModelWithLoad()
    assert instance.loaded == True
