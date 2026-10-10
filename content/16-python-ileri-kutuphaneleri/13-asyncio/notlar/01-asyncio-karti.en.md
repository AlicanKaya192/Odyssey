## Basics

| Code | What it does |
|---|---|
| `async def f(): ...` | a coroutine function |
| `await f()` | run and wait (only inside `async def`) |
| `asyncio.run(main())` | set up the event loop, run, close |
| `await asyncio.sleep(s)` | free the loop while waiting |

## Running together

| Code | What it does |
|---|---|
| `await asyncio.gather(a(), b())` | wait for all; results in the given order |
| `gather(..., return_exceptions=True)` | put the error in place of the result |
| `task = asyncio.create_task(f())` | start right away |
| `async with asyncio.TaskGroup() as g:` | a task group; if one fails, the others are cancelled |
| `except* ValueError as eg:` | catch from inside an `ExceptionGroup` |
| `for c in asyncio.as_completed(items):` | the first done comes first |

## Limits

| Code | What it does |
|---|---|
| `async with asyncio.timeout(1):` | a time limit; `TimeoutError` when it runs out |
| `await asyncio.wait_for(f(), timeout=1)` | a time limit for one job |
| `asyncio.Semaphore(3)` + `async with` | at most 3 at a time |
| `await asyncio.to_thread(f, x)` | run a blocking function in a thread |
| `asyncio.Queue()`; `await q.get()` | an async queue |

## Errors

| Symptom | Cause |
|---|---|
| `RuntimeWarning: coroutine ... was never awaited` | a forgotten `await` |
| `gather` is used but it takes the sum of the waits | `time.sleep` or synchronous I/O inside `async def` |
| `SyntaxError: 'await' outside async function` | `await` in an ordinary function |
| `RuntimeError: asyncio.run() cannot be called from a running event loop` | `asyncio.run` called inside an already running loop (in Jupyter, use `await main()` directly) |
