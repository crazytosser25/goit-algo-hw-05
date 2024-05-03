"""Task 1"""
def caching_fibonacci(n: int) -> int:
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
        result = fibonacci(n-2) + fibonacci(n-1)
        cache[n] = result
        return result
    return fibonacci(n)


if __name__ == "__main__":
    print(caching_fibonacci(5))
    print(caching_fibonacci(5))
