# Project 4 – Asyncio and Concurrency

## What This Project Shows
- Simulated I/O-bound work with `asyncio` coroutines and `asyncio.gather`
- Comparison of synchronous vs asynchronous execution time
- CPU-bound workloads where process-based parallelism (not asyncio) is a better fit

## Files
- `asyncio_io_demo.py` – compares sequential "I/O" (sleep) with concurrent asyncio tasks
- `cpu_bound_concurrency_demo.py` – benchmarks single-process vs `ProcessPoolExecutor` vs `multiprocessing.Pool`

## Run The Examples
From the project root (virtualenv activated):

```bash
python 04/asyncio_io_demo.py
```

Use these as a starting point to experiment with different task counts, delays,
and input sizes to see how concurrency affects performance on your machine.

