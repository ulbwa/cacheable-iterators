from cached_iterators import CacheableIteratorWrapper, cacheable_iterator


def generate_numbers():
    for i in range(5):
        yield i


def test_cacheable_iterator_wrapper():
    iterator = generate_numbers()
    cached_iter = CacheableIteratorWrapper(iterator)

    first_pass = list(cached_iter)
    assert first_pass == [0, 1, 2, 3, 4]

    second_pass = list(cached_iter)
    assert second_pass == [0, 1, 2, 3, 4]

    assert first_pass == second_pass


def test_cacheable_iterator_decorator():
    @cacheable_iterator
    def decorated_generate_numbers():
        for i in range(5):
            yield i

    cached_iter = decorated_generate_numbers()

    first_pass = list(cached_iter)
    assert first_pass == [0, 1, 2, 3, 4]

    second_pass = list(cached_iter)
    assert second_pass == [0, 1, 2, 3, 4]

    assert first_pass == second_pass
