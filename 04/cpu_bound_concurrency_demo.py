import time
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from typing import Iterable, Callable


def cpu_bound(number: int) -> int:
    """A deliberately heavy CPU-bound calculation.

    Computes the sum of squares from 0 up to ``number``.
    """

    return sum(i * i for i in range(number))


def sync_calculate(numbers: Iterable[int]) -> None:
    for n in numbers:
        cpu_bound(n)


def process_pool_calculate(numbers: Iterable[int]) -> None:
    with ProcessPoolExecutor() as executor:
        # Force evaluation so work is actually done before timing stops.
        list(executor.map(cpu_bound, numbers))


def multiprocessing_pool_calculate(numbers: Iterable[int]) -> None:
    with multiprocessing.Pool() as pool:
        list(pool.map(cpu_bound, numbers))


def benchmark(label: str, func: Callable[[Iterable[int]], None], numbers: Iterable[int]) -> None:
    start = time.perf_counter()
    func(numbers)
    elapsed = time.perf_counter() - start
    print(f"{label:30s}: {elapsed:.2f} seconds")


def main() -> None:
    # Same shape as the example from the blog post:
    # a list of fairly large integers to make the CPU work visible.
    numbers = [10_000_000 + x for x in range(20)]

    print("CPU-bound concurrency comparison (no asyncio)")
    print("-" * 60)
    benchmark("Synchronous (single process)", sync_calculate, numbers)
    benchmark("ProcessPoolExecutor", process_pool_calculate, numbers)
    benchmark("multiprocessing.Pool", multiprocessing_pool_calculate, numbers)
    print("\nNote: asyncio is great for I/O-bound work, but for heavy CPU-bound\n"
          "tasks like this, multi-processing is usually the right tool.")


if __name__ == "__main__":
    main()
