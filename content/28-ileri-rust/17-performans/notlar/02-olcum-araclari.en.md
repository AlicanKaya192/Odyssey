## Measurement mistakes

| Mistake | Result | Cure |
|---|---|---|
| Measuring in debug | A meaningless number | `--release` |
| Not using the result | The work is removed | `black_box` |
| One run | Noise | Many repeats, the median |
| Counting the first run | A cold cache | A warm-up round |
| Very small data | It fits in the cache | The real size |
| Very short time | Clock resolution | Enough repeats |
| Other work running | Fluctuation | A quiet machine |
| `println!` where measured | I/O is measured | Move it out of the loop |

## Tools

| Tool | What for |
|---|---|
| `Instant` | Rough measuring, your own code |
| `criterion` | Statistical, comparative benchmarks |
| `hyperfine` | The time of a whole program |
| `flamegraph`, `perf` | Where time goes |
| `dhat` | Where allocations are |
| `cargo build --timings` | Where compiling takes long |
| `cargo bloat` | What grows the file |

They are not installed in this path; knowing their names is enough. For a profiler, write `debug = true` in `[profile.release]`; otherwise symbol names do not show.

## Counters instead of time

Time is noisy. For many questions a counter gives a more honest answer:

| Question | Counter |
|---|---|
| Did allocations drop? | A `GlobalAlloc` counter |
| Did the algorithm improve? | The number of comparisons |
| Did the cache hit? | The `perf stat` cache miss count |

That is also why the exercises in Odyssey do not look at time: the result is the same on every machine.

## When comparing

1. First take a baseline measurement and keep it.
2. Change one thing.
3. Measure again with the same data.
4. Is the difference bigger than the noise? If not, there is no improvement.
5. If the code got more complex, is the gain worth it?

## When to stop?

The target must be clear: "this request returns in under 100 ms" is measurable; "make it faster" is not. Stop when you reach the target. Parallelism is a last resort too; first measure that one branch is really saturated. Concurrency bugs and complexity are a cost as well.
