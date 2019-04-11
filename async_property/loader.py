from asyncio import wait, iscoroutinefunction as is_coroutine
from .cached import AsyncCachedPropertyDescriptor


class AsyncCachedPropertyObjectMeta(type):
    def __new__(mcs, name, bases, attrs) -> type:
        loaders = []
        for value in attrs.values():
            if isinstance(value, AsyncCachedPropertyDescriptor):
                loaders.append(value.load_value)
        attrs['_async_property_loaders'] = loaders
        return super().__new__(mcs, name, bases, attrs)


class AsyncCachedPropertyLoader(metaclass=AsyncCachedPropertyObjectMeta):
    _async_property_loaders = []

    def __await__(self):
        return self._load().__await__()

    async def _load(self):
        """Calls overridable async load method"""
        if hasattr(self, 'load') and is_coroutine(self.load):
            await self.load()
        if self._async_property_loaders:
            await wait([
                loader(self) for loader in self._async_property_loaders
            ])
        return self
