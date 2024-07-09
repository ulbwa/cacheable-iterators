# cached-iterators

A Python library providing cacheable iterator wrappers for both synchronous and asynchronous iterators. This allows 
iterators to be reused multiple times with cached values, reducing the need for recomputations.

<!-- TOC -->
* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
  * [Synchronous Iterator Wrapper](#synchronous-iterator-wrapper)
    * [Output](#output)
  * [Asynchronous Iterator Wrapper](#asynchronous-iterator-wrapper)
    * [Output](#output-1)
<!-- TOC -->

## Features

- **Reusable Iterators**: Wrap synchronous and asynchronous iterators to allow them to be iterated multiple times 
  with cached results.
- **Lazy Loading**: Only fetch and cache results as needed, avoiding unnecessary computations or I/O operations.
- **Ease of Use**: Simple API with decorators for easy integration.
- **Improved Concurrency**: Efficiently handle concurrent tasks that need to use the same iterator.

## Installation

You can install this package via pip:

```shell
python3 -m pip install cached-iterators
```

## Usage

### Synchronous Iterator Wrapper

You can use the synchronous iterator wrapper in two ways: by decorating a function that returns an iterator or by directly wrapping an iterator instance.

1. **Decorating a function**:

```python
from cached_iterators import cacheable_iterator
from typing import Iterator


@cacheable_iterator
def generate_numbers() -> Iterator[int]:
  for i in range(5):
    print(f"Generating {i}")
    yield i


# Create a cacheable iterator using the decorated function
cached_iter = generate_numbers()

# First iteration (values will be generated and cached)
print("First iteration:")
for num in cached_iter:
  print(num)

# Second iteration (values will be retrieved from cache)
print("Second iteration:")
for num in cached_iter:
  print(num)
```

2. **Wrapping an existing iterator**:

```python
from cached_iterators import CacheableIteratorWrapper
from typing import Iterator


def generate_numbers() -> Iterator[int]:
  for i in range(5):
    print(f"Generating {i}")
    yield i


# Create a cacheable iterator by wrapping an existing iterator instance
iterator = generate_numbers()
cached_iter = CacheableIteratorWrapper(iterator)

# First iteration (values will be generated and cached)
print("First iteration:")
for num in cached_iter:
  print(num)

# Second iteration (values will be retrieved from cache)
print("Second iteration:")
for num in cached_iter:
  print(num)
```

#### Output

```
First iteration:
Generating 0
0
Generating 1
1
Generating 2
2
Generating 3
3
Generating 4
4
Second iteration:
0
1
2
3
4
```

### Asynchronous Iterator Wrapper

Similarly, the asynchronous iterator wrapper can be used by decorating a function that returns an asynchronous 
iterator or by directly wrapping an asynchronous iterator instance.

1. **Decorating a function**:

```python
import asyncio
from cached_iterators import cacheable_async_iterator
from typing import AsyncIterator


@cacheable_async_iterator
async def async_generate_numbers() -> AsyncIterator[int]:
  for i in range(5):
    print(f"Generating {i}")
    yield i
    await asyncio.sleep(0)  # Simulate async work


# Create a cacheable async iterator using the decorated function
cached_iter = async_generate_numbers()


async def main():
  # First iteration (values will be generated and cached)
  print("First iteration:")
  async for num in cached_iter:
    print(num)

  # Second iteration (values will be retrieved from cache)
  print("Second iteration:")
  async for num in cached_iter:
    print(num)


# Run the example
asyncio.run(main())
```

2. **Wrapping an existing iterator**:

```python
import asyncio
from cached_iterators import CacheableAsyncIteratorWrapper
from typing import AsyncIterator


async def async_generate_numbers() -> AsyncIterator[int]:
  for i in range(5):
    print(f"Generating {i}")
    yield i
    await asyncio.sleep(0)  # Simulate async work


# Create a cacheable async iterator by wrapping an existing async iterator instance
iterator = async_generate_numbers()
cached_iter = CacheableAsyncIteratorWrapper(iterator)


async def main():
  # First iteration (values will be generated and cached)
  print("First iteration:")
  async for num in cached_iter:
    print(num)

  # Second iteration (values will be retrieved from cache)
  print("Second iteration:")
  async for num in cached_iter:
    print(num)


# Run the example
asyncio.run(main())
```

#### Output

```
First iteration:
Generating 0
0
Generating 1
1
Generating 2
2
Generating 3
3
Generating 4
4
Second iteration:
0
1
2
3
4
```