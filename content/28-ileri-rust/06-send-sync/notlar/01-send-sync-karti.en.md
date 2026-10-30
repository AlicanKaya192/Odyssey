## Decision questions

| Question | If yes |
|---|---|
| Does the type hold only data it owns? | `Send` with `T: Send` |
| Does nothing change through `&self`? | `Sync` with `T: Sync` |
| Does it change through `&self`, with a lock or atomic? | `Sync` with `T: Send` |
| Does it change through `&self` without a lock? | It **cannot** be `Sync` |
| Is a shared counter not atomic? | It **cannot** be `Send` |

## The standard template

```rust
// SAFETY: MyVec owns its items, like Vec.
unsafe impl<T: Send> Send for MyVec<T> {}
// SAFETY: &MyVec only gives &T, so sharing it shares only &T.
unsafe impl<T: Sync> Sync for MyVec<T> {}
```

`T: Send` for `Send`, `T: Sync` for `Sync`. This pair is right for nearly all owning types.

## Trying it

```rust
fn assert_send<T: Send>() {}
fn assert_sync<T: Sync>() {}

fn main() {
    assert_send::<MyVec<i32>>();
    assert_sync::<MyVec<i32>>();
}
```

If it compiles, the promise exists. No test is enough for a wrong `unsafe impl`; write the reasoning in the `// SAFETY:` comment.

## A trap in closure capture

Closures now capture individual fields. Even if a `SendPtr` wrapper is `Send`:

```rust
let p = SendPtr(raw);
thread::spawn(move || unsafe { *p.0 = 1 });
```

`p.0` is captured, not `p`. `p.0` is a raw pointer and not `Send`, so it does not compile. The fix is calling a method like `p.get()`: a method makes the whole `p` captured.
