## A table

| Type | For `'a` | For `T` |
|---|---|---|
| `&'a T` | Covariant | Covariant |
| `&'a mut T` | Covariant | **Invariant** |
| `Box<T>`, `Vec<T>`, `Rc<T>` | - | Covariant |
| `Cell<T>`, `RefCell<T>`, `Mutex<T>` | - | **Invariant** |
| `*const T`, `NonNull<T>` | - | Covariant |
| `*mut T` | - | **Invariant** |
| `fn(T)` | - | Contravariant |
| `fn() -> T` | - | Covariant |

## A short rule

| Question | Answer |
|---|---|
| Does the type only read its contents? | It can be covariant |
| Can the type write inside? | It must be invariant |
| Does the type only take `T`? | Contravariant |

## Merging in a struct

If a parameter appears in several fields, the strictest wins:

```rust
struct Pair<'a, T> {
    read: &'a T,        // covariant in T
    cell: Cell<T>,      // invariant in T
}
// Pair is invariant in T.
```

## What does the error look like?

A variance error does not name itself. If you see these, think of variance:

- `does not live long enough`, though the value seems to live long enough.
- `lifetime may not live long enough`, like `requires that 'a must outlive 'static`.
- If a note mentions `&mut` or `Cell`, it is almost certain.

The fix is usually accepting the code is not correct: the compiler is preventing a real dangling reference.
