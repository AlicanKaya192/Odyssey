An enum and `match` together are the cleanest way to build a **state machine**. Think of an order: which event is valid in which state?

```rust
#[derive(Debug, Clone, Copy)]
enum State {
    Pending,
    Paid,
    Shipped,
}

#[derive(Clone, Copy)]
enum Event {
    Pay,
    Ship,
    Cancel,
}

impl State {
    fn next(self, event: Event) -> State {
        match (self, event) {
            (State::Pending, Event::Pay) => State::Paid,
            (State::Paid, Event::Ship) => State::Shipped,
            (State::Paid, Event::Cancel) => State::Pending,
            (state, _) => state,
        }
    }
}

fn main() {
    let mut state = State::Pending;
    for event in [Event::Ship, Event::Pay, Event::Ship, Event::Cancel] {
        state = state.next(event);
        println!("{:?}", state);
    }
}
```

```text
Pending
Paid
Shipped
Shipped
```

Things to notice:

- All transitions are read in one place.
- Writing `match` on a `(state, event)` tuple is like a two-dimensional table.
- Invalid transitions are in the `_` arm: the state does not change.
- A method taking `self` consumes the old state; there cannot be two states at once.

## When to use _?

Here `_` is used on purpose: "every other event is invalid" is a single rule. But when a new state is added the compiler no longer asks about that arm. The decision is:

| Question | Choice |
|---|---|
| Should this `match` be looked at when a variant is added? | Yes: write out the variants |
| Does a new variant also fall in the same "rest" group? | `_` |

## All values, not infinity

`match` must be exhaustive on numbers too. If you write arms covering all values from 0 to 255 for a `u8`, `_` is not needed:

```rust
fn kind(n: u8) -> &'static str {
    match n {
        0..=99 => "small",
        100..=255 => "big",
    }
}

fn main() {
    println!("{} {}", kind(5), kind(200));
}
```

```text
small big
```
