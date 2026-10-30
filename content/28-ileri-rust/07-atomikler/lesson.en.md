# Atomics and Memory Ordering

An atomic operation is one whose middle another branch cannot see. It gives lock-free sharing for basic types. The module's hardest part is here: in what order operations appear.

## Why is it needed?

`x += 1` is not one operation: read, add, write. If two branches do it at once, one overwrites the other's increase. `fetch_add` does this in one step:

```rust
use std::sync::atomic::{AtomicU32, Ordering};
use std::thread;

static HITS: AtomicU32 = AtomicU32::new(0);

fn main() {
    thread::scope(|s| {
        for _ in 0..4 {
            s.spawn(|| {
                for _ in 0..1000 {
                    HITS.fetch_add(1, Ordering::SeqCst);
                }
            });
        }
    });
    println!("{}", HITS.load(Ordering::SeqCst));
}
```

```text
4000
```

The result is the same on every run. Without a `Mutex`, because a lock is too much for one number.

## Operations

| Call | Job |
|---|---|
| `load(o)` | Read |
| `store(v, o)` | Write |
| `fetch_add(v, o)` | Add, return the **old** |
| `swap(v, o)` | Write, return the old |
| `compare_exchange(old, new, s, f)` | Write if it is the old |
| `fetch_update(...)` | Change in a loop with a closure |

`compare_exchange` is the base of lock-free structures. It says "change if the value is still what I expect", and reports the result with `Result`:

```rust
use std::sync::atomic::{AtomicU32, Ordering};

fn main() {
    let value = AtomicU32::new(5);
    println!("{:?}", value.compare_exchange(5, 6, Ordering::SeqCst, Ordering::SeqCst));
    println!("{:?}", value.compare_exchange(5, 7, Ordering::SeqCst, Ordering::SeqCst));
    println!("{}", value.load(Ordering::SeqCst));
}
```

```text
Ok(5)
Err(6)
6
```

So things an increase cannot do can be written. Like a counter holding the largest value:

```rust
use std::sync::atomic::{AtomicU32, Ordering};
use std::thread;

fn store_max(slot: &AtomicU32, value: u32) {
    let mut current = slot.load(Ordering::SeqCst);
    while value > current {
        match slot.compare_exchange(current, value, Ordering::SeqCst, Ordering::SeqCst) {
            Ok(_) => return,
            Err(actual) => current = actual,
        }
    }
}

fn main() {
    let best = AtomicU32::new(0);
    thread::scope(|s| {
        for n in [3, 9, 4, 7] {
            let best = &best;
            s.spawn(move || store_max(best, n));
        }
    });
    println!("{}", best.load(Ordering::SeqCst));
}
```

```text
9
```

The loop is required: if another branch changed it after we read, `compare_exchange` fails, and we retry with the new value.

## Memory ordering

Each atomic operation takes an `Ordering`. The processor and compiler may reorder reads and writes that do not change the result on one branch. `Ordering` says how much of that is allowed:

| Ordering | Its promise | Use |
|---|---|---|
| `Relaxed` | Only that operation is atomic | An independent counter |
| `Release` | Earlier writes do not pass it | Publishing data |
| `Acquire` | Later reads do not pass it | Taking what is published |
| `AcqRel` | Both | Read-write like `fetch_add` |
| `SeqCst` | All branches see the same order | If unsure |

## Publishing: Release and Acquire

The most important pattern is this. One branch prepares data, then writes a flag with `Release`. If the other branch reads the flag with `Acquire` and sees `true`, it is sure the data is ready:

```rust
use std::sync::atomic::{AtomicBool, AtomicU32, Ordering};
use std::thread;

static DATA: AtomicU32 = AtomicU32::new(0);
static READY: AtomicBool = AtomicBool::new(false);

fn main() {
    thread::scope(|s| {
        s.spawn(|| {
            DATA.store(42, Ordering::Relaxed);
            READY.store(true, Ordering::Release);
        });
        s.spawn(|| {
            while !READY.load(Ordering::Acquire) {
                std::hint::spin_loop();
            }
            println!("{}", DATA.load(Ordering::Relaxed));
        });
    });
}
```

```text
42
```

With `Relaxed` there would be no promise for `DATA`: a branch could see the flag and read the data at its old value. This error does not appear on most machines, and appears on other architectures. That is exactly why ordering is chosen **by reasoning**, not by trying.

## Relaxed is enough for a counter

If a counter protects no other data, no ordering is needed. The result is still correct, because `fetch_add` is atomic:

```rust
use std::sync::atomic::{AtomicU64, Ordering};
use std::thread;

fn main() {
    let total = AtomicU64::new(0);
    thread::scope(|s| {
        for _ in 0..8 {
            s.spawn(|| {
                for _ in 0..10_000 {
                    total.fetch_add(1, Ordering::Relaxed);
                }
            });
        }
    });
    println!("{}", total.load(Ordering::Relaxed));
}
```

```text
80000
```

## What to choose?

| Case | Choice |
|---|---|
| An independent counter, statistics | `Relaxed` |
| A "this data is ready" flag | `Release` / `Acquire` |
| A lock | `Acquire` / `Release` |
| I am unsure | `SeqCst` |

`SeqCst` is always correct, but it does not mean "faster than locks". In most programs the difference cannot be measured; be correct first.

## Cache lines

Atomics look cheap, but if two branches write to the same cache line, processors grab the line from each other. Even when the variables differ. This is called **false sharing**, and `#[repr(align(64))]` separates the variables:

```rust
use std::sync::atomic::AtomicU64;

struct Together {
    a: AtomicU64,
    b: AtomicU64,
}

#[repr(align(64))]
struct OnItsOwnLine(AtomicU64);

struct Apart {
    a: OnItsOwnLine,
    b: OnItsOwnLine,
}

fn main() {
    println!("{}", size_of::<Together>());
    println!("{}", size_of::<Apart>());
}
```

```text
16
128
```

## Summary

- An atomic operation does not split: `fetch_add`, `compare_exchange`.
- A `compare_exchange` loop is the base of lock-free structures.
- `Relaxed`: only that value. `Release`/`Acquire`: publishing data.
- `SeqCst` when unsure, but correctness before speed.
- An ordering error may not appear in tests; choose by reasoning.
