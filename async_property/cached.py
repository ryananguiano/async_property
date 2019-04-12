import asyncio
import functools

from async_property.proxy import AwaitableOnly, AwaitableProxy

is_coroutine = asyncio.iscoroutinefunction


def async_cached_property(func, *args, **kwargs):
    assert is_coroutine(func), 'Can only use with async def'
    return AsyncCachedPropertyDescriptor(func, *args, **kwargs)


class AsyncCachedPropertyDescriptor:
    def __init__(self, _fget, _fset=None, _fdel=None, field_name=None):
        self._fget = _fget
        self._fset = _fset
        self._fdel = _fdel
        self.field_name = field_name or _fget.__name__
        functools.update_wrapper(self, _fget)

    def __set_name__(self, owner, name):
        self.field_name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if not hasattr(instance, self.field_attr):
            return self.not_loaded(instance)
        return self.already_loaded(instance)

    def __set__(self, instance, value):
        if self._fset is None:
            setattr(instance, self.field_attr, value)
        else:
            self._fset(instance, value)

    def __delete__(self, instance):
        if self._fdel is None:
            delattr(instance, self.field_attr)
        else:
            self._fdel(instance)

    def setter(self, method):
        self._check_method(method, f'@{self.field_name}.setter')
        return type(self)(self._fget, method, self._fdel, self.field_name)

    def deleter(self, method):
        self._check_method(method, f'@{self.field_name}.deleter')
        return type(self)(self._fget, self._fset, method, self.field_name)

    def _check_method(self, method, method_type):
        if method.__name__ != self.field_name:
            raise AssertionError(f'{method_type} name must match property name')
        if is_coroutine(method):
            raise AssertionError(f'{method_type} must be synchronous')

    @property
    def field_attr(self):
        return f'_{self.field_name}'

    @property
    def lock_attr(self):
        return f'_{self.field_name}_lock'

    def get_instance_lock(self, instance):
        try:
            lock = getattr(instance, self.lock_attr)
        except AttributeError:
            lock = asyncio.Lock()
            setattr(instance, self.lock_attr, lock)
        return lock

    def get_loader(self, instance):
        @functools.wraps(self._fget)
        async def load_value():
            async with self.get_instance_lock(instance):
                try:
                    return getattr(instance, self.field_attr)
                except AttributeError:
                    pass
                value = await self._fget(instance)
                self.__set__(instance, value)
                return value
        return load_value

    def not_loaded(self, instance):
        return AwaitableOnly(self.get_loader(instance))

    def already_loaded(self, instance):
        return AwaitableProxy(getattr(instance, self.field_attr))
