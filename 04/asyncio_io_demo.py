import asyncio
import time


async def fake_io(task_id: int, delay: float = 1.0) -> None:
    """Pretend to do slow I/O by only awaiting asyncio.sleep (like a fake API call)."""
    print(f"[async] task {task_id} started")
    await asyncio.sleep(delay)
    print(f"[async] task {task_id} finished")


def sync_io(count: int = 5, delay: float = 1.0) -> float:
    """Run the same I/O simulation sequentially using time.sleep."""
    print("\n=== Synchronous I/O simulation ===")
    start = time.perf_counter()
    for task_id in range(count):
        print(f"[sync] task {task_id} started")
        time.sleep(delay)
        print(f"[sync] task {task_id} finished")
    elapsed = time.perf_counter() - start
    print(f"Synchronous version took {elapsed:.2f} seconds\n")
    return elapsed


async def async_io(count: int = 5, delay: float = 1.0) -> float:
    """Run the I/O simulation concurrently using asyncio.gather."""
    print("=== Asyncio I/O simulation ===")
    start = time.perf_counter()
    tasks = [asyncio.create_task(fake_io(task_id, delay)) for task_id in range(count)]
    await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - start
    print(f"Asyncio version took {elapsed:.2f} seconds\n")
    return elapsed


def main() -> None:
    # Simulate slow I/O bound work. With count=5 and delay=1.0,
    # synchronous will be ~5s, asyncio should be ~1s on a typical machine.
    sync_io()
    asyncio.run(async_io())


if __name__ == "__main__":
    main()
