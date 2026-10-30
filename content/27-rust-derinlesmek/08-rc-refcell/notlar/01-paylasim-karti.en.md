## Which one?

| Need | Type | Check |
|---|---|---|
| One owner, heap | `Box<T>` | Compile time |
| Many owners, reading | `Rc<T>` | Compile time |
| One owner, changing through `&self` | `RefCell<T>` | Run time |
| Changing a small `Copy` value | `Cell<T>` | None, and no panic |
| Many owners and changing | `Rc<RefCell<T>>` | Run time |
| A non-owning link | `Weak<T>` | `upgrade` |

## Forms

| Job | Written |
|---|---|
| Create | `Rc::new(x)`, `RefCell::new(x)` |
| Share | `Rc::clone(&a)` |
| Counter | `Rc::strong_count(&a)` |
| A weak link | `Rc::downgrade(&a)` |
| Weak to strong | `weak.upgrade()` |
| Read | `cell.borrow()` |
| Write | `cell.borrow_mut()` |
| Together | `shared.borrow_mut().push(1)` |

## Cell

A `Copy` type needs no borrow: the value is taken and put, and no panic happens.

```rust
use std::cell::Cell;

fn main() {
    let hits = Cell::new(0);
    hits.set(hits.get() + 1);
    hits.set(hits.get() + 1);
    println!("{}", hits.get());
}
```

```text
2
```

## Errors

| Symptom | Cause |
|---|---|
| `already borrowed: BorrowMutError` | Two `borrow_mut` at once |
| `already mutably borrowed` | Reading while writing |
| `E0594`, `E0596` | Trying to change `Rc` contents |
| `Rc<...> cannot be sent` | Sending to a thread: `Arc` |
| Memory grows, `drop` does not run | A reference cycle: `Weak` |
