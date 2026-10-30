## State at the type level

One of the nicest uses of `PhantomData` is **writing a value's state into its type** (typestate). A call in the wrong order does not compile:

```rust
use std::marker::PhantomData;

struct Open;
struct Closed;

struct Door<State> {
    name: String,
    _state: PhantomData<State>,
}

impl Door<Closed> {
    fn open(self) -> Door<Open> {
        Door { name: self.name, _state: PhantomData }
    }
}

impl Door<Open> {
    fn walk_through(&self) -> String {
        format!("through {}", self.name)
    }
}
```

There is **no** `walk_through` method on `Door<Closed>`. No run-time check is needed, and no error message either.

## When is it good?

| Case | Decision |
|---|---|
| Ordered work: connect, authenticate, query | Good |
| The builder pattern: no `build` before required fields are filled | Good |
| The state comes from a file or the network | Bad: the type must be known at compile time |
| Many states | Bad: code explodes, use an `enum` |

## The price

Zero: `PhantomData` is absent at run time. A method takes `self` and returns a new type; the old value cannot be used, because it has moved. Ownership helps here too: a door cannot be "both open and closed".

It is very common outside the standard library; it often appears in web clients and driver code.
