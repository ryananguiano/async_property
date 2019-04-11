import asyncio
from async_property.cached import AsyncCachedPropertyDescriptor

is_coroutine = asyncio.iscoroutinefunction


class AwaitLoaderMeta(type):
    def __new__(mcs, name, bases, attrs) -> type:
        loaders = []
        for value in attrs.values():
            if isinstance(value, AsyncCachedPropertyDescriptor):
                loaders.append(value.load_value)
        attrs['_async_property_loaders'] = loaders
        return super().__new__(mcs, name, bases, attrs)


class AwaitLoader(metaclass=AwaitLoaderMeta):
    _async_property_loaders = []

    def __await__(self):
        return self._load().__await__()

    async def _load(self):
        """Calls overridable async load method and then async property loaders"""
        if hasattr(self, 'load') and is_coroutine(self.load):
            await self.load()
        if self._async_property_loaders:
            await asyncio.wait([
                load_property(self)()
                for load_property
                in self._async_property_loaders
            ])
        return self
