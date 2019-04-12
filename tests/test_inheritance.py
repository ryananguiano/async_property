import pytest

from async_property import async_cached_property, AwaitLoader
from async_property.loader import get_loaders

pytestmark = pytest.mark.asyncio


class TestLoaderA(AwaitLoader):
    @async_cached_property
    async def foo(self):
        return True


class TestLoaderB(AwaitLoader):
    @async_cached_property
    async def bar(self):
        return False


class TestLoader(TestLoaderA, TestLoaderB):
    @async_cached_property
    async def abc(self):
        return 123

    @async_cached_property
    async def foo(self):
        return False


async def test_loaders_exist():
    instance = TestLoader()
    assert len(get_loaders(instance)) == 3


async def test_loader_keys():
    instance = TestLoader()
    assert set(get_loaders(instance)) == {'foo', 'bar', 'abc'}


async def test_inherited_value():
    instance = await TestLoader()
    assert instance.foo == False
