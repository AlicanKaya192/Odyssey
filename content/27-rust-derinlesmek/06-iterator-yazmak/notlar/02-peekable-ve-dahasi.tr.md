## Peekable: Bakıp almamak

Sıradakine bakmak ama tüketmemek gerekince `.peekable()`. Ayrıştırıcılarda çok kullanılır:

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

## Kendi uyarlayıcın

Başka bir iterator'ı saran generic struct da iterator olabilir:

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

`I: Iterator<Item = i32>`: Herhangi bir sayı iterator'ı. `map` ve `filter` de böyle yazılmıştır.

## Bir trait ile metot eklemek

Uyarlayıcını zincire takmak için trait yazılır:

```rust
trait EveryOtherExt: Iterator + Sized {
    fn every_other(self) -> EveryOther<Self> {
        EveryOther { inner: self }
    }
}

impl<I: Iterator> EveryOtherExt for I {}
```

Kapsayıcı impl sayesinde her iterator `.every_other()` kazanır. Rust'ta `Ext` son ekiyle sık görülür.
