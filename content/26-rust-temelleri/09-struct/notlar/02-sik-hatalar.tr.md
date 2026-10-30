## Alan eksik

```rust
struct User {
    name: String,
    age: u32,
}

fn main() {
    let user = User { name: String::from("Ada") };
    println!("{}", user.age);
}
```

```text
error[E0063]: missing field `age` in initializer of `User`
 --> main.rs:7:16
  |
7 |     let user = User { name: String::from("Ada") };
  |                ^^^^ missing `age`
```

Rust varsayılan değer uydurmaz: Her alan verilmelidir.

## Metot yok

`E0599` genellikle metodu yanlış türde çağırdığını gösterir ya da `impl` bloğunu yazmadığını:

```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let rect = Rectangle { width: 3, height: 4 };
    println!("{}", rect.area());
}
```

```text
error[E0599]: no method named `area` found for struct `Rectangle` in the current scope
 --> main.rs:9:25
  |
2 | struct Rectangle {
  | ---------------- method `area` not found for this struct
...
9 |     println!("{}", rect.area());
  |                         ^^^^ method not found in `Rectangle`
```

## &self ile değiştirmek

```rust
struct Counter {
    value: u32,
}

impl Counter {
    fn add(&self) {
        self.value += 1;
    }
}

fn main() {
    let counter = Counter { value: 0 };
    counter.add();
}
```

```text
error[E0594]: cannot assign to `self.value`, which is behind a `&` reference
 --> main.rs:7:9
  |
7 |         self.value += 1;
  |         ^^^^^^^^^^^^^^^ `self` is a `&` reference, so it cannot be written to
  |
help: consider changing this to be a mutable reference
  |
6 |     fn add(&mut self) {
  |             +++
```

Çözüm imzayı `&mut self` yapmak. Çağıran değişken de `mut` olmalıdır.

## Metotta sahiplik yanlışı

| Belirti | Sebep | Çözüm |
|---|---|---|
| Metottan sonra değer kullanılamıyor | `self` aldı | `&self` yap |
| `cannot move out of self.name` | `&self` ile alanı döndürüyorsun | `&self.name` ya da `.clone()` döndür |
| `cannot borrow as mutable` | Değişken `mut` değil | `let mut` yaz |
| `E0507` | Ödünç alınan değerin içinden taşımak | `.clone()` ya da `&` |

Son satırın örneği:

```rust
struct User {
    name: String,
}

impl User {
    fn name(&self) -> String {
        self.name
    }
}

fn main() {
    let user = User { name: String::from("Ada") };
    println!("{}", user.name());
}
```

```text
error[E0507]: cannot move out of `self.name` which is behind a shared reference
 --> main.rs:7:9
  |
7 |         self.name
  |         ^^^^^^^^^ move occurs because `self.name` has type `String`, which does not
  implement the `Copy` trait
  |
help: consider cloning the value if the performance cost is acceptable
  |
7 |         self.name.clone()
  |                  ++++++++
```

Dönüş türü `&str` yaparak ödünç vermek en iyisi: `fn name(&self) -> &str { &self.name }`.
