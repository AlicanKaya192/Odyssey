## Peekable: looking without taking

When you need to look at the next without consuming it, `.peekable()`. It is used a lot in parsers:

```rust
fn read_numbers(text: &str) -> Vec<u32> {
    let mut out = Vec::new();
    let mut chars = text.chars().peekable();
    while let Some(c) = chars.next() {
        if let Some(digit) = c.to_digit(10) {
            let mut value = digit;
            while let Some(d) = chars.peek().and_then(|p| p.to_digit(10)) {
                value = value * 10 + d;
                chars.next();
            }
            out.push(value);
        }
    }
    out
}

fn main() {
    println!("{:?}", read_numbers("a12 b3,450"));
}
```

```text
[12, 3, 450]
```

## Your own adapter

A generic struct wrapping another iterator can be an iterator too:

```rust
struct EveryOther<I> {
    inner: I,
}

impl<I: Iterator> Iterator for EveryOther<I> {
    type Item = I::Item;

    fn next(&mut self) -> Option<I::Item> {
        let item = self.inner.next();
        self.inner.next();
        item
    }
}

fn main() {
    let it = EveryOther { inner: 1..6 };
    println!("{:?}", it.collect::<Vec<i32>>());
}
```

```text
[1, 3, 5]
```

`I: Iterator<Item = i32>`: any number iterator. `map` and `filter` are written like this too.

## Adding a method with a trait

To hook your adapter into a chain, a trait is written:

```rust
trait EveryOtherExt: Iterator + Sized {
    fn every_other(self) -> EveryOther<Self> {
        EveryOther { inner: self }
    }
}

impl<I: Iterator> EveryOtherExt for I {}
```

Thanks to a blanket impl, every iterator gains `.every_other()`. In Rust the `Ext` suffix is common.
