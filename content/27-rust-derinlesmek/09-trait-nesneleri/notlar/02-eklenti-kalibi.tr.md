## Eklenti kalıbı

Yeni davranış, mevcut koda dokunmadan eklenebilsin:

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

`run` hangi süzgeçlerin olduğunu bilmez. Yeni bir `struct` ve `impl Filter` yeter.

## State kalıbı

Durum makinesinde her durum kendi türüdür:

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

`self: Box<Self>` metodun kutuyu tüketmesini sağlar: Geçiş eski durumu yok eder.

Rust'ta aynı iş çoğu zaman enum ile daha kısadır. Durumlar başkasınca eklenecekse bu kalıp kullanılır.

## Kısa tablo

| Kural | |
|---|---|
| Önce generic dene | Sıfır maliyet |
| Sabit seçenekler | `enum` |
| Açık uçlu seçenekler | `dyn` |
| Karar verirken | Çağrı başına bir adım çoğu zaman önemsizdir |
