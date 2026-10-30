## A panic can come from anywhere

`T::clone`, `T::drop`, a closure given by the user: all can panic. Code managing memory by hand must keep the program in a valid state at each of these points.

| Level | Promise |
|---|---|
| Leaks may happen | Only a resource loss; no undefined behavior |
| The invariant holds | The structure stays usable |
| Full rollback | As if nothing happened |

Undefined behavior is accepted at **no** level. A leak is acceptable.

## A common error

```rust
// Wrong order: the length grows before the value is written.
self.len += 1;
let value = make_value();
ptr::write(self.ptr.add(self.len - 1), value);
```

If `make_value` panics, the length has grown but the place is empty. Dropping the structure tries to drop the empty place too: undefined behavior. The right order is producing the value first, then writing, and raising the length **last**.

## The guard pattern

Hold a value to undo half-done work; its `Drop` cleans up. On success, silence the guard with `mem::forget`:

```rust
struct Guard<'a> {
    list: &'a mut Vec<i32>,
    original_len: usize,
}

impl Drop for Guard<'_> {
    fn drop(&mut self) {
        self.list.truncate(self.original_len);
    }
}
```

## The rule

In manual memory work ask yourself: "If this line panics, what happens when the structure drops?" If the answer is "I do not know", the order is wrong.
