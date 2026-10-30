## The plugin pattern

So new behavior can be added without touching existing code:

```rust
trait Filter {
    fn apply(&self, text: &str) -> String;
}

struct Upper;
struct Trim;

impl Filter for Upper {
    fn apply(&self, text: &str) -> String {
        text.to_uppercase()
    }
}

impl Filter for Trim {
    fn apply(&self, text: &str) -> String {
        text.trim().to_string()
    }
}

fn run(filters: &[Box<dyn Filter>], text: &str) -> String {
    let mut out = text.to_string();
    for f in filters {
        out = f.apply(&out);
    }
    out
}

fn main() {
    let filters: Vec<Box<dyn Filter>> = vec![Box::new(Trim), Box::new(Upper)];
    println!("{}", run(&filters, "  hi "));
}
```

```text
HI
```

`run` does not know which filters exist. A new `struct` and an `impl Filter` is enough.

## The state pattern

In a state machine each state is its own type:

```rust
trait State {
    fn next(self: Box<Self>) -> Box<dyn State>;
    fn name(&self) -> &str;
}

struct Draft;
struct Published;

impl State for Draft {
    fn next(self: Box<Self>) -> Box<dyn State> {
        Box::new(Published)
    }

    fn name(&self) -> &str {
        "draft"
    }
}

impl State for Published {
    fn next(self: Box<Self>) -> Box<dyn State> {
        self
    }

    fn name(&self) -> &str {
        "published"
    }
}

fn main() {
    let mut s: Box<dyn State> = Box::new(Draft);
    println!("{}", s.name());
    s = s.next();
    println!("{}", s.name());
}
```

```text
draft
published
```

`self: Box<Self>` lets the method consume the box: a transition destroys the old state.

In Rust the same job is usually shorter with an enum. This pattern is used if others will add states.

## A short table

| Rule | |
|---|---|
| Try generics first | Zero cost |
| Fixed choices | `enum` |
| Open-ended choices | `dyn` |
| When deciding | One step per call is usually unimportant |
