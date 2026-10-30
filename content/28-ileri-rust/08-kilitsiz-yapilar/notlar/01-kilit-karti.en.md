## A lock skeleton

| Part | Written |
|---|---|
| The flag | `locked: AtomicBool` |
| The data | `value: UnsafeCell<T>` |
| The promise | `unsafe impl<T: Send> Sync for Lock<T> {}` |
| Taking | `compare_exchange_weak(false, true, Acquire, Relaxed)` |
| Releasing | `locked.store(false, Release)` |
| Using | `Guard` + `Deref` + `DerefMut` + `Drop` |

## The waiting part

| Written | Meaning |
|---|---|
| `std::hint::spin_loop()` | Telling the processor "I am looping" |
| `thread::yield_now()` | Giving the turn to another branch |
| `thread::park()` | Sleeping, until `unpark` |

## Lock families

| Type | What a waiter does | Suitable work |
|---|---|---|
| Spinlock | Spins | Very short, no kernel |
| `Mutex` | Spins briefly, sleeps | General |
| `RwLock` | Sleeps | Many reads, few writes |
| `Condvar` | Sleeps until a condition holds | Producer and consumer |
| `Barrier` | Sleeps until all arrive | Starting together |

## A checklist

| Question | If wrong |
|---|---|
| Is `Guard` not `Send`? | The lock may open on another branch |
| Does the lock open in a panic? | Everyone waits forever |
| Is there a `T: Send` condition? | `Rc` escapes |
| A lock inside a lock? | Think of deadlock order |

Our `Guard` holds `&SpinLock<T>`, so it is `Send` if `T: Sync`; the real `MutexGuard` is not `Send` because of the operating system lock. A spinlock has no such issue.
