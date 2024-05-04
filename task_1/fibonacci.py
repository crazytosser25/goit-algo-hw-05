"""Task 1"""
def caching_fibonacci() -> int:
    """Calculating fibonacci numbers and saving them to cache. Returning
    values from cache in case of need.
    """
    cache = {0: 0, 1: 1}
    def fibonacci(n: int) -> int:
        if n in cache:
            print('return from cache')
            return cache[n]
        cache[n] = fibonacci(n-2) + fibonacci(n-1)
        print('return calculated')
        return cache[n]
    return fibonacci


if __name__ == "__main__":
    fib = caching_fibonacci()
    print(f'Result: {fib(0)}')
    print(f'Result: {fib(1)}')
    print(f'Result: {fib(10)}')
    print(f'Result: {fib(10)}')
    print(f'Result: {fib(15)}')
    print(f'Result: {fib(15)}')
