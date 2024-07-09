from typing import Callable, Iterable, Iterator, List, ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


class CacheableIteratorWrapper(Iterable[T]):
    """
    A cacheable iterator wrapper class that wraps a standard iterator into a "cached" one,
    allowing the iterator to be cycled through multiple times. If a value is already in the cache,
    iteration will not occur until the next value is needed from the iterator, i.e., lazy loading.
    This is useful for specific concurrent tasks that need to use the same iterator but cannot do so with
    standard Python means.

    :param __iterator: The original iterator to be wrapped.
    :type __iterator: Iterator[T]
    """

    def __init__(self, __iterator: Iterator[T], /) -> None:
        """
        Initialize the CacheableIteratorWrapper.

        :param __iterator: The original iterator to be wrapped.
        :type __iterator: Iterator[T]
        """
        self.iterator = __iterator
        self.values: List[T] = []
        self.done: bool = False

    def __iter__(self) -> Iterator[T]:
        """
        Return an iterator over the cached values.

        :return: An iterator over the cached values.
        :rtype: Iterator[T]
        """
        if self.done:
            return iter(self.values)
        return CacheableIterator(self)


class CacheableIterator(Iterator[T]):
    """
    An iterator for the CacheableIteratorWrapper class.

    :param __wrapper: The CacheableIteratorWrapper instance to iterate over.
    :type __wrapper: CacheableIteratorWrapper
    """

    def __init__(self, __wrapper: CacheableIteratorWrapper, /):
        """
        Initialize the CacheableIterator.

        :param __wrapper: The CacheableIteratorWrapper instance to iterate over.
        :type __wrapper: CacheableIteratorWrapper
        """
        self.wrapper = __wrapper
        self.index = 0

    def __next__(self) -> T:
        """
        Return the next value from the iterator.

        :return: The next value from the iterator.
        :rtype: T

        :raises StopIteration: If the end of the iterator is reached.
        """
        if self.index < len(self.wrapper.values):
            value = self.wrapper.values[self.index]
        else:
            try:
                value = next(self.wrapper.iterator)
            except StopIteration:
                self.wrapper.__done = True
                raise StopIteration()
            else:
                self.wrapper.values.append(value)

        self.index += 1

        return value


def cacheable_iterator(__func: Callable[P, Iterator[T]], /) -> Callable[P, Iterable[T]]:
    """
    Decorator function to convert an iterator-returning function into one that returns a CacheableIteratorWrapper.

    :param __func: The function that returns an iterator.
    :type __func: Callable[P, Iterator[T]]

    :return: A new function that returns a CacheableIteratorWrapper.
    :rtype: Callable[P, Iterable[T]]
    """

    def inner(*args: P.args, **kwargs: P.kwargs) -> Iterable[T]:
        """
        Create a CacheableIteratorWrapper from the original function.

        :param args: Positional arguments to pass to the original function.
        :param kwargs: Keyword arguments to pass to the original function.

        :return: A CacheableIteratorWrapper instance.
        :rtype: Iterable[T]
        """
        return CacheableIteratorWrapper(__func(*args, **kwargs))

    return inner


# __all__ = (
#     "CacheableIteratorWrapper",
#     "cacheable_iterator",
# )
