"""imports"""
from typing import Callable, Generator, Any
import re

"""Task 2"""
def generator_numbers(text: str) -> Generator[float, Any, Any]:
    """Generate real numbers from the given text.

    Args:
        text (str): The text to analyze for real numbers.

    Yields:
        Generator[float, Any, Any]:  generator yielding the real
        numbers found in the text.
    """
    pattern = r'\b\d+\.\d+\b'
    for i in re.findall(pattern, text):
        yield float(i)

def sum_profit(text: str, func: Callable) -> float:
    """Calculate the sum of real numbers extracted from the text
    using the provided function.

    Args:
        text (str): The text to analyze.
        func (Callable): The function used to extract real numbers from the text.

    Returns:
        float: The total sum of the real numbers found in the text.
    """
    total = sum(func(text))
    return total


if __name__ == "__main__":
    TEXT = "Загальний дохід працівника складається з декількох частин: " \
    "1000.01 як основний дохід, доповнений додатковими надходженнями " \
    "27.45 і 324.00 доларів."
    total_income = sum_profit(TEXT, generator_numbers)
    print(f"Total income: {total_income}")
