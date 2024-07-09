import asyncio

import pytest

from cacheable_iterators import CacheableAsyncIteratorWrapper, cacheable_async_iterator


async def async_generate_numbers():
    for i in range(5):
        yield i
        await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_cacheable_async_iterator_wrapper():
    iterator = async_generate_numbers()
    cached_iter = CacheableAsyncIteratorWrapper(iterator)

    first_pass = [num async for num in cached_iter]
    assert first_pass == [0, 1, 2, 3, 4]

    second_pass = [num async for num in cached_iter]
    assert second_pass == [0, 1, 2, 3, 4]

    assert first_pass == second_pass


@pytest.mark.asyncio
async def test_cacheable_async_iterator_decorator():
    @cacheable_async_iterator
    async def decorated_async_generate_numbers():
        for i in range(5):
            yield i
            await asyncio.sleep(0)

    cached_iter = decorated_async_generate_numbers()

    first_pass = [num async for num in cached_iter]
    assert first_pass == [0, 1, 2, 3, 4]

    second_pass = [num async for num in cached_iter]
    assert second_pass == [0, 1, 2, 3, 4]

    assert first_pass == second_pass
