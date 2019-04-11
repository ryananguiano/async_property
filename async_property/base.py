import functools
from asyncio import iscoroutinefunction as is_coroutine

from async_property.exceptions import AsyncPropertyException
from async_property.proxy import AwaitableOnly


def async_property(method):
    assert is_coroutine(method), 'Can only use with async def'
    return AsyncPropertyDescriptor(method)


class AsyncPropertyDescriptor:
    def __init__(self, _fget, _fset=None, _fdel=None, field_name=None, doc=None):
        self._fget = _fget
        self.field_name = field_name or _fget.__name__
        self.__doc__ = doc or _fget.__doc__

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

    @property
    def field_attr(self):
        return f'_{self.field_name}'

    @property
    def _error(self):
        return AsyncPropertyException(
            f'{self.field_name} is an async_property. Use await on the property value.'
        )

    def get_value(self, instance):
        @functools.wraps(self._fget)
        async def _get_value():
            return await self._fget(instance)
        return _get_value

    def get_awaitable(self, instance):
        name = f'{instance.__class__.__qualname__}.{self.field_name}'
        return AwaitableOnly(self.get_value(instance), name, self._error)
