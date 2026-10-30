# Testler, Clippy ve rustfmt

Rust'ın araçları programla birlikte gelir: Test çalıştırıcısı `cargo test`, kod denetleyicisi `cargo clippy`, biçimleyici `cargo fmt`. Bir Rust projesinde bu üçünü çalıştırmak alışkanlıktır.

## Test düzeni

Temeller'in bitirme bölümünde `#[test]` ve `assert_eq!` gördük. Biraz daha:

```rust
fn divide(a: i32, b: i32) -> i32 {
    if b == 0 {
        panic!("division by zero");
    }
    a / b
}

fn parse(text: &str) -> Result<i32, String> {
    text.parse().map_err(|_| String::from("bad"))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn divides() {
        assert_eq!(divide(6, 3), 2, "six over three");
    }

    #[test]
    #[should_panic(expected = "division by zero")]
    fn zero_panics() {
        divide(1, 0);
    }

    #[test]
    fn parses() -> Result<(), String> {
        assert_eq!(parse("7")?, 7);
        Ok(())
    }

    #[test]
    #[ignore]
    fn slow_one() {
        assert!(true);
    }
}

fn main() {}

```

```text
running 4 tests
test tests::divides ... ok
test tests::parses ... ok
test tests::slow_one ... ignored
test tests::zero_panics - should panic ... ok

test result: ok. 3 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out; finished in
0.00s
```

| Yazım | Anlamı |
|---|---|
| `assert!(k, "mesaj {}", x)` | Düşerse mesaj da yazılır |
| `#[should_panic(expected = "...")]` | Panik **beklenir**, metin geçmeli |
| `-> Result<(), String>` | `?` kullanılabilir, `Err` düşürür |
| `#[ignore]` | Normalde atlanır, `cargo test -- --ignored` |

## Birim ve bütünleşme testi

| Tür | Yer | Görür |
|---|---|---|
| Birim | Aynı dosyada `mod tests` | Gizli olanı da |
| Bütünleşme | `tests/` klasörü | Yalnızca `pub` |
| Belge | `///` içindeki kod | Yalnızca `pub` |

Gerçek bir projede hepsi birlikte çalışır:

```text
    Finished `test` profile [unoptimized + debuginfo] target(s)
     Running unittests src\lib.rs (target/debug/deps/shop)

running 1 test
test tests::doubles ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in
0.00s

     Running tests\outside.rs (target/debug/deps/outside)

running 1 test
test from_outside ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in
0.00s

   Doc-tests shop

running 1 test
test src\lib.rs - double (line 3) ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in
0.00s
```

Çıktıda üç bölüm var: `src/lib.rs` birim testleri, `tests/` bütünleşme testi ve `Doc-tests`. Belge testi, belgedeki örneğin **gerçekten çalıştığını** garanti eder:

```rust
/// Doubles a number.
///
/// ```
/// assert_eq!(shop::double(2), 4);
/// ```
pub fn double(n: i32) -> i32 {
    n * 2
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn doubles() {
        assert_eq!(double(3), 6);
    }
}

```

`///` belge yorumudur; `cargo doc` onlardan site üretir.

## Komutlar

| Komut | İş |
|---|---|
| `cargo test` | Hepsi |
| `cargo test parse` | Adında `parse` geçenler |
| `cargo test --lib` | Yalnızca birim |
| `cargo test --test cli` | `tests/cli.rs` |
| `cargo test -- --nocapture` | `println!` çıktısını göster |
| `cargo test -- --test-threads=1` | Sırayla |

Testler varsayılan olarak **aynı anda** çalışır. Aynı dosyaya dokunan testler birbirini bozar.

## Clippy: Fazladan göz

Derleyici yanlış kodu durdurur. `cargo clippy` ise doğru ama kötü kodu söyler, üstelik nasıl düzeltileceğini de:

```rust
pub fn total(list: &Vec<i32>) -> i32 {
    let mut sum = 0;
    for i in 0..list.len() {
        sum += list[i];
    }
    return sum;
}

```

```text
warning: unneeded `return` statement
 --> src\lib.rs:6:5
  |
6 |     return sum;
  |     ^^^^^^^^^^
  |
  = help: for further information visit
    https://rust-lang.github.io/rust-clippy/rust-1.99.0/index.html#needless_return
  = note: `#[warn(clippy::needless_return)]` on by default
help: remove `return`
  |
6 -     return sum;
6 +     sum
  |

warning: writing `&Vec` instead of `&[_]` involves a new object where a slice will do
 --> src\lib.rs:1:20
  |
1 | pub fn total(list: &Vec<i32>) -> i32 {
  |                    ^^^^^^^^^
  |
  = help: for further information visit
    https://rust-lang.github.io/rust-clippy/rust-1.99.0/index.html#ptr_arg
  = note: `#[warn(clippy::ptr_arg)]` on by default
help: change this to
  |
1 - pub fn total(list: &Vec<i32>) -> i32 {
1 + pub fn total(list: &[i32]) -> i32 {
  |

warning: the loop variable `i` is only used to index `list`
 --> src\lib.rs:3:14
  |
3 |     for i in 0..list.len() {
  |              ^^^^^^^^^^^^^
  |
  = help: for further information visit
    https://rust-lang.github.io/rust-clippy/rust-1.99.0/index.html#needless_range_loop
  = note: `#[warn(clippy::needless_range_loop)]` on by default
help: consider using an iterator
  |
3 -     for i in 0..list.len() {
3 +     for <item> in &list {
  |

warning: `shop` (lib) generated 3 warnings (run `cargo clippy --fix --lib -p shop -- `
to apply 1 suggestion)
    Finished `dev` profile [unoptimized + debuginfo] target(s)
```

Clippy'nin yüzlerce kuralı var (lint). Çoğu önerisi öğreticidir. Hepsi kabul edilmek zorunda değildir: Tek bir yerde kapatmak için `#[allow(clippy::needless_range_loop)]`.

CI'da uyarıyı hataya çevirmek yaygındır: `cargo clippy -- -D warnings`.

## rustfmt: Tek biçim

`cargo fmt` kodu tek bir biçime getirir, tartışma biter:

```text
before:
pub fn add( a:i32,b:i32 )->i32{
a+b
}

after cargo fmt:
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

`cargo fmt --check` değiştirmez, yalnızca denetler; CI için. Ayarlar `rustfmt.toml`'da, ama varsayılan biçim neredeyse her Rust projesinde aynıdır.

## Örnek akış

Kaydetmeden önce, tek satırda:

```text
cargo fmt && cargo clippy && cargo test
```

## Özet

- `#[should_panic]`, `Result` dönen test, `#[ignore]`.
- Birim aynı dosyada, bütünleşme `tests/`, belge testi `///` içinde.
- `cargo test isim`, `--lib`, `-- --nocapture`. Testler aynı anda çalışır.
- `cargo clippy` kötü kodu söyler; `cargo fmt` biçimi tek yapar.
