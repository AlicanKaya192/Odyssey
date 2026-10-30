## The guard pattern

If something is to be done at a job's start and end, leave the end to `Drop`. It runs even on an early return or a panic:

```rust
struct Timer {
    label: &'static str,
}

impl Timer {
    fn start(label: &'static str) -> Timer {
        println!("start {label}");
        Timer { label }
    }
}

impl Drop for Timer {
    fn drop(&mut self) {
        println!("stop {}", self.label);
    }
}

fn work(fail: bool) -> Result<i32, String> {
    let _t = Timer::start("work");
    if fail {
        return Err(String::from("failed"));
    }
    Ok(1)
}

fn main() {
    println!("{:?}", work(true));
    println!("{:?}", work(false));
}
```

```text
start work
stop work
Err("failed")
start work
stop work
Ok(1)
```

That is why a `Mutex` lock (section 11) and an open file are not closed by hand.

## Option::take

To take a field's value out, leaving `None` in the field:

```rust
struct Slot {
    item: Option<String>,
}

impl Slot {
    fn remove(&mut self) -> Option<String> {
        self.item.take()
    }
}

fn main() {
    let mut s = Slot { item: Some(String::from("key")) };
    println!("{:?}", s.remove());
    println!("{:?}", s.remove());
    let mut text = String::from("old");
    let old = std::mem::replace(&mut text, String::from("new"));
    println!("{old} {text}");
}
```

```text
Some("key")
None
old new
```

`std::mem::replace` and `std::mem::take` do the same with another value. It is the way to take ownership from within `&mut self`.

## A tree example

Nodes with left and right children want `Box` too:

```rust
#[derive(Debug)]
struct Node {
    value: i32,
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
}

fn leaf(value: i32) -> Option<Box<Node>> {
    Some(Box::new(Node { value, left: None, right: None }))
}

fn total(node: &Option<Box<Node>>) -> i32 {
    match node {
        Some(n) => n.value + total(&n.left) + total(&n.right),
        None => 0,
    }
}

fn main() {
    let root = Some(Box::new(Node { value: 1, left: leaf(2), right: leaf(3) }));
    println!("{}", total(&root));
}
```

```text
6
```

`Option<Box<Node>>` is the most common tree field in Rust.
