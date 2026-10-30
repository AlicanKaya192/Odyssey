## Koruyucu (guard) kalıbı

Bir işin başında ve sonunda bir şey yapılacaksa, sonunu `Drop`'a bırak. Erken dönüşte ya da panikte bile çalışır:

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

Bu yüzden `Mutex` kilidi (bölüm 11) ve açık dosya elle kapatılmaz.

## Option::take

Alandaki değeri dışarı almak için, alana `None` bırakarak:

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

`std::mem::replace` ve `std::mem::take` aynı işi başka değerle yapar. `&mut self` içinden sahiplik almanın yoludur.

## Ağaç örneği

Sol ve sağ çocuğu olan düğümler de `Box` ister:

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

`Option<Box<Node>>` Rust'ta en sık görülen ağaç alanıdır.
