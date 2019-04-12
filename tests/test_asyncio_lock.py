import asyncio
import time

import pytest

from async_property import async_cached_property, AwaitLoader

pytestmark = pytest.mark.asyncio


class MyModel(AwaitLoader):
    def __init__(self):
        self.num_loaded = 0

    @async_cached_property
    async def first(self):
        await asyncio.sleep(0.1)
        self.num_loaded += 1

    @async_cached_property
    async def second(self):
        await asyncio.sleep(0.2)
        self.num_loaded += 1

    @async_cached_property
    async def third(self):
        await asyncio.sleep(0.3)
        self.num_loaded += 1


async def test_is_locking():
    start = time.time()
    instance = MyModel()
    await asyncio.gather(instance.first, instance.first, instance.first)
    duration = time.time() - start
    assert instance.num_loaded == 1
    assert 0.1 <= duration < 0.15


async def test_lock_multiple_instances():
    start = time.time()
    instance_one = MyModel()
    instance_two = MyModel()
    await asyncio.gather(instance_one.first, instance_two.first)
    duration = time.time() - start
    assert 0.1 <= duration < 0.15


async def test_concurrent():
    start = time.time()
    instance = MyModel()
    await asyncio.gather(instance.first, instance.second, instance.third)
    duration = time.time() - start
    assert instance.num_loaded == 3
    assert 0.3 <= duration < 0.4


async def test_await_concurrent():
    start = time.time()
    instance = await MyModel()
    duration = time.time() - start
    assert instance.num_loaded == 3
    assert 0.3 <= duration < 0.4
