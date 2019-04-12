import asyncio
import functools

from async_property.proxy import AwaitableOnly

is_coroutine = asyncio.iscoroutinefunction


def async_property(func, *args, **kwargs):
    assert is_coroutine(func), 'Can only use with async def'
    return AsyncPropertyDescriptor(func, *args, **kwargs)


class AsyncPropertyDescriptor:
    def __init__(self, _fget, field_name=None):
        self._fget = _fget
        self.field_name = field_name or _fget.__name__
        functools.update_wrapper(self, _fget)

    def __set_name__(self, owner, name):
        self.field_name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.get_awaitable(instance)

    def __set__(self, instance, value):
        raise ValueError('Cannot set @async_property. Use @async_cached_property instead.')

    def __delete__(self, instance):
        raise ValueError('Cannot delete @async_property. Use @async_cached_property instead.')

    def get_value(self, instance):
        @functools.wraps(self._fget)
        async def _get_value():
            return await self._fget(instance)
        return _get_value

    def get_awaitable(self, instance):
        name = f'{instance.__class__.__qualname__}.{self.field_name}'
        return AwaitableOnly(self.get_value(instance), name)
