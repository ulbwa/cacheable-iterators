import asyncio
from typing import (AsyncIterable, AsyncIterator, Callable, Iterator, List,
                    ParamSpec, TypeVar)

T = TypeVar("T")
P = ParamSpec("P")


class AsyncIteratorWrapper(AsyncIterable[T]):
    """
    A wrapper that wraps a synchronous iterator to an asynchronous iterator.

    :param __iterator: The synchronous iterator to wrap.
    :type __iterator: Iterator[T]
    """

    def __init__(self, __iterator: Iterator[T], /) -> None:
        """
        Initialize the AsyncIteratorWrapper.

        :param __iterator: The synchronous iterator to wrap.
        :type __iterator: Iterator[T]
        """
        self.iterator = __iterator

    def __aiter__(self) -> AsyncIterator[T]:
        """
        Return the asynchronous iterator.

        :return: The asynchronous iterator.
        :rtype: AsyncIterator[T]
        """
        return self

    async def __anext__(self) -> T:
        """
        Provide the next value from the synchronous iterator wrapped for asynchronous usage.

        :return: The next value from the synchronous iterator.
        :rtype: T

        :raises StopAsyncIteration: If the end of the iterator is reached.
        """
        try:
            value = next(self._sync_iterator)
            await asyncio.sleep(0)  # Allow other tasks to run
            return value
        except StopIteration:
            raise StopAsyncIteration()


class CacheableAsyncIteratorWrapper(AsyncIterable[T]):
    """
    A cacheable async iterator wrapper class that wraps a standard async iterator into a "cached" one,
    allowing the iterator to be cycled through multiple times. If a value is already in the cache,
    iteration will not occur until the next value is needed from the iterator, i.e., lazy loading.
    This is useful for specific concurrent tasks that need to use the same iterator but cannot do so with
    standard Python means.

    :param __iterator: The original async iterator to be wrapped.
    :type __iterator: AsyncIterator[T]
    """

    def __init__(self, __iterator: AsyncIterator[T], /):
        """
        Initialize the CacheableAsyncIteratorWrapper.

        :param __iterator: The original async iterator to be wrapped.
        :type __iterator: AsyncIterator[T]
        """
        self.iterator = __iterator
        self.values: List[T] = []
        self.done: bool = False

    def __aiter__(self) -> AsyncIterator[T]:
        """
        Return an iterator over the cached values.

        :return: An iterator over the cached values.
        :rtype: AsyncIterator[T]
        """
        if self.done:
            return AsyncIteratorWrapper(iter(self.values))
        return CacheableAsyncIterator(self)


class CacheableAsyncIterator(AsyncIterator[T]):
    """
    An iterator for the CacheableAsyncIteratorWrapper class.

    :param __wrapper: The CacheableAsyncIteratorWrapper instance to iterate over.
    :type __wrapper: CacheableAsyncIteratorWrapper
    """

    def __init__(self, __wrapper: CacheableAsyncIteratorWrapper, /):
        """
        Initialize the CacheableAsyncIterator.

        :param __wrapper: The CacheableAsyncIteratorWrapper instance to iterate over.
        :type __wrapper: CacheableAsyncIteratorWrapper
        """
        self.wrapper = __wrapper
        self.index = 0

    async def __anext__(self) -> T:
        """
        Return the next value from the iterator.

        :return: The next value from the iterator.
        :rtype: T

        :raises StopAsyncIteration: If the end of the iterator is reached.
        """
        if self.index < len(self.wrapper.values):
            value = self.wrapper.values[self.index]
        else:
            try:
                value = await anext(self.wrapper.iterator)
            except StopAsyncIteration:
                self.wrapper.__done = True
                raise StopAsyncIteration()
            else:
                self.wrapper.values.append(value)

        self.index += 1

        return value


def cacheable_async_iterator(
    __func: Callable[P, AsyncIterator[T]], /
) -> Callable[P, AsyncIterable[T]]:
    """
    Decorator function to convert an async iterator-returning function into one that returns a
    CacheableAsyncIteratorWrapper.

    :param __func: The function that returns an async iterator.
    :type __func: Callable[P, AsyncIterator[T]]

    :return: A new function that returns a CacheableAsyncIteratorWrapper.
    :rtype: Callable[P, AsyncIterable[T]]
    """

    def inner(*args: P.args, **kwargs: P.kwargs) -> AsyncIterable[T]:
        return CacheableAsyncIteratorWrapper(__func(*args, **kwargs))

    return inner


# __all__ = (
#     "AsyncIteratorWrapper",
#     "CacheableAsyncIteratorWrapper",
#     "cacheable_async_iterator",
# )
