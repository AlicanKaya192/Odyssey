## Forms

| Job | Written |
|---|---|
| Shared data | `Arc::new(Mutex::new(v))` |
| Share | `Arc::clone(&shared)` |
| Write | `*shared.lock().unwrap() += 1` |
| Many readers | `Arc::new(RwLock::new(v))` |
| Read | `lock.read().unwrap()` |
| Write | `lock.write().unwrap()` |
| Atomic | `AtomicU32::new(0)` |
| Increase | `n.fetch_add(1, Ordering::SeqCst)` |
| Once only | `OnceLock` |

## Which one?

| Job | Choice |
|---|---|
| Data goes to one branch | `move` |
| Several branches read, inside a scope | `&T` |
| Several branches read, long-lived | `Arc<T>` |
| Several branches write | `Arc<Mutex<T>>` |
| Much reading, little writing | `Arc<RwLock<T>>` |
| A single number | `AtomicU32` |
| Gathering results | A channel |

## Counterparts of Rc

| One branch | Many branches |
|---|---|
| `Rc<T>` | `Arc<T>` |
| `RefCell<T>` | `Mutex<T>`, `RwLock<T>` |
| `Cell<u32>` | `AtomicU32` |

## Scoped branches need no Arc

```rust
use std::sync::Mutex;
use std::thread;

fn main() {
    let total = Mutex::new(0);
    thread::scope(|s| {
        for n in 1..=3 {
            let total = &total;
            s.spawn(move || {
                *total.lock().unwrap() += n;
            });
        }
    });
    println!("{}", total.lock().unwrap());
}
```

```text
6
```

Since `thread::scope` allows borrowing, `Arc` is not needed and `Mutex` is enough.
