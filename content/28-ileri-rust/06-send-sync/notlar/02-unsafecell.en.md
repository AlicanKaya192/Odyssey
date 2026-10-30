## UnsafeCell rules

`UnsafeCell<T>::get(&self)` gives `*mut T`. It tells the compiler "the value here can change through `&`", and optimizations follow this. Still, two rules are yours:

| Rule | If broken |
|---|---|
| There cannot be both a `&mut T` and another reference at once | Undefined behavior |
| Access across branches must be synchronized | A data race |

## What does each type add?

| Type | On top of `UnsafeCell` | Check |
|---|---|---|
| `Cell<T>` | Not giving references | No references, safe |
| `RefCell<T>` | A borrow counter | At run time, a panic |
| `Mutex<T>` | An operating system lock | Across branches, waits |
| `AtomicU32` | Atomic operations | Across branches, no lock |
| `OnceLock<T>` | Writing once | Across branches |

## A forbidden shortcut

Converting `&T` to `*mut T` and writing is **always** undefined behavior without `UnsafeCell`:

```rust
let x = 1;
let r = &x;
let p = r as *const i32 as *mut i32;
// unsafe { *p = 2 };  // undefined behavior, even if it appears to work
```

The compiler assumes `x` does not change and can replace the read with a constant `1`. The write's effect may never appear. That is why a type like `Cell` is needed; it is not simply "turning off optimization".
