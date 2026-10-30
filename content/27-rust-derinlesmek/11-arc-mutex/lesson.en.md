# Arc and Mutex

A channel moves data. Sometimes, though, many branches need to reach **the same data**: a shared counter, a shared cache. For this there are two parts: `Arc` for several owners and `Mutex` for one access at a time.

## Mutex: one branch at a time

A `Mutex` (mutual exclusion) guards the data inside with a lock. The **only way** to reach the data is taking the lock, so forgetting the lock does not compile:

```rust
use std::sync::Mutex;

fn main() {
    let value = Mutex::new(5);
    {
        let mut guard = value.lock().unwrap();
        *guard += 1;
    }
    println!("{:?}", value.lock().unwrap());
}
```

```text
6
```

| Part | Meaning |
|---|---|
| `Mutex::new(5)` | The guarded value |
| `.lock()` | Waits for the lock and returns `Result` |
| `unwrap` | If the lock is not poisoned (below) |
| The guard | The value is reached with `*guard` |

**The lock opens by itself at scope end**: the `Drop` of `MutexGuard`. RAII gives safety here: you cannot forget to release the lock.

## The problem: several branches

```rust
use std::sync::Mutex;
use std::thread;

fn main() {
    let counter = Mutex::new(0);
    let a = thread::spawn(move || *counter.lock().unwrap() += 1);
    let b = thread::spawn(move || *counter.lock().unwrap() += 1);
    a.join().unwrap();
    b.join().unwrap();
}
```

```text
error[E0382]: use of moved value: `counter`
 --> main.rs:7:27
  |
5 |     let counter = Mutex::new(0);
  |         ------- move occurs because `counter` has type `std::sync::Mutex<i32>`,
  which does not implement the `Copy` trait
6 |     let a = thread::spawn(move || *counter.lock().unwrap() += 1);
  |                           -------  ------- variable moved due to use in closure
  |                           |
  |                           value moved into closure here
7 |     let b = thread::spawn(move || *counter.lock().unwrap() += 1);
  |                           ^^^^^^^  ------- use occurs due to use in closure
  |                           |
  |                           value used here after move
```

Ownership went to the first branch and the second cannot have it. Several owners are needed. If we try `Rc`, it is not `Send`. The fix is `Arc`.

## Arc: an atomic counter

`Arc<T>` (atomic reference counted) is the same as `Rc`, but since it updates the counter with the processor's atomic operations it is safe across threads. The price is a little slowness, which is why `Rc` still exists.

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = Vec::new();
    for _ in 0..4 {
        let counter = Arc::clone(&counter);
        handles.push(thread::spawn(move || {
            for _ in 0..1000 {
                *counter.lock().unwrap() += 1;
            }
        }));
    }
    for h in handles {
        h.join().unwrap();
    }
    println!("{}", counter.lock().unwrap());
}
```

```text
4000
```

Always the same result: 4 branches, each increasing 1000 times. Without the lock it would not compile.

<figure class="fig"><svg viewBox="0 0 640 226" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">stack</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">heap</text><g><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">counter</text><text class="dim" x="110" y="71" font-size="12.5">Arc</text></g><g><rect class="box" x="20" y="102" width="230" height="44" rx="8"/><text class="ink" x="34" y="129" font-size="14" font-weight="600">counter</text><text class="dim" x="110" y="129" font-size="12.5">Arc</text></g><g><rect class="box" x="20" y="160" width="230" height="44" rx="8"/><text class="ink" x="34" y="187" font-size="14" font-weight="600">counter</text><text class="dim" x="110" y="187" font-size="12.5">Arc</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">3, Mutex(0)</text></g><path class="curve" d="M250 66 C320 66 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/><path class="curve" d="M250 124 C320 124 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/><path class="curve" d="M250 182 C320 182 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/></svg><figcaption>Each branch has its own Arc, and all point to the same Mutex.</figcaption></figure>

## Do the calculation outside

While the lock is held, the others wait. So keep the lock **as short as you can**:

```rust
use std::sync::Mutex;

fn expensive(n: u64) -> u64 {
    (1..=n).sum()
}

fn main() {
    let results = Mutex::new(Vec::new());
    let value = expensive(1000);
    {
        let mut list = results.lock().unwrap();
        list.push(value);
    }
    println!("{:?}", results.lock().unwrap());
}
```

```text
[500500]
```

Do the expensive calculation before the lock, and lock only while writing the result. Putting it in a block releases the guard early.

## RwLock: many readers

If it is mostly read, `RwLock` allows many readers at once, and a writer stays alone:

```rust
use std::sync::RwLock;

fn main() {
    let config = RwLock::new(String::from("v1"));
    {
        let a = config.read().unwrap();
        let b = config.read().unwrap();
        println!("{a} {b}");
    }
    config.write().unwrap().push_str("-new");
    println!("{}", config.read().unwrap());
}
```

```text
v1 v1
v1-new
```

The run-time counterpart of the borrowing rule. With much writing, `Mutex` may be faster.

## Atomics

A single number needs no lock:

```rust
use std::sync::atomic::{AtomicU32, Ordering};
use std::thread;

fn main() {
    let hits = AtomicU32::new(0);
    thread::scope(|s| {
        for _ in 0..4 {
            s.spawn(|| {
                for _ in 0..1000 {
                    hits.fetch_add(1, Ordering::SeqCst);
                }
            });
        }
    });
    println!("{}", hits.load(Ordering::SeqCst));
}
```

```text
4000
```

`Ordering::SeqCst` is the strongest and clearest option. We will see the others in the Advanced module. For now the rule: if unsure, `SeqCst`.

## Poisoning

If a branch holding a lock panics, the `Mutex` is **poisoned**: the data may be half done, so the next `lock()` gives `Err`:

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let shared = Arc::new(Mutex::new(1));
    let copy = Arc::clone(&shared);
    let _ = thread::spawn(move || {
        let _guard = copy.lock().unwrap();
        panic!("oops");
    })
    .join();
    println!("{}", shared.is_poisoned());
    println!("{}", shared.lock().is_err());
}
```

```text
true
true
```

`unwrap` is usually the right choice: let the panic spread. If you want to use the data anyway, you take it with `into_inner`.

## A deadlock

If two branches take two locks in reverse order, both wait forever. This is called a **deadlock**. **Rust does not stop this.** A data race does not compile; a deadlock does.

| Prevention | |
|---|---|
| Take locks in the same order everywhere | The safest |
| Take no other lock while holding one | If possible |
| Keep the lock short | Always |

A branch locking the same `Mutex` twice also hangs or panics.

## Summary

- `Mutex<T>`: data is reached only by the lock; the lock opens when `MutexGuard` drops.
- `Arc<T>`: several owners across branches. `Arc<Mutex<T>>` is the standard pair.
- Keep the lock short; do the calculation outside.
- `RwLock` for many readers; types such as `AtomicU32` for a single number.
- A panic poisons the lock. Rust does not stop a deadlock: keep the order yourself.
