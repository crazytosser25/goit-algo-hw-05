"""Task 1"""
def caching_fibonacci() -> int:
    """Calculating fibonacci numbers and saving them to cache. Returning
    values from cache in case of need.

    Args:
        n (int): number

    Returns:
        int: number
    """
    cache = {0: 0, 1: 1}
    def fibonacci(n: int) -> int:
        if n in cache:
            return cache[n]
        cache[n] = fibonacci(n-2) + fibonacci(n-1)
        return cache[n]
    return fibonacci


if __name__ == "__main__":
    fib = caching_fibonacci()
    print(fib(5))
    print(fib(5))
    print(fib(10))
    print(fib(15))
