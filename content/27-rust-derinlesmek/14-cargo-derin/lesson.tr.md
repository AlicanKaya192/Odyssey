# Workspace ve Feature'lar

Proje büyüyünce tek crate yetmez. Bu bölüm Cargo'nun büyük proje araçlarını anlatıyor: Birkaç crate'i tek çatıda toplamak, isteğe bağlı özellikler, derleme profilleri ve derleme betiği.

## Kütüphane ve program birlikte

Temeller'de `src/main.rs` ya da `src/lib.rs` gördük. İkisi aynı pakette durabilir: İş kütüphanede, program yalnızca ince bir kabuk. Böylece testler iş mantığına doğrudan ulaşır.

```text
src/lib.rs        the work
src/main.rs       program shop
src/bin/report.rs program report

$ cargo run --bin shop
total 7

$ cargo run --bin report
report: 2 items
report total 7

$ cargo run
error: `cargo run` could not determine which binary to run. Use the `--bin` option to
specify a binary, or the `default-run` manifest key.
available binaries: report, shop
```

`src/bin/` altındaki her dosya ayrı bir program olur. `cargo run --bin report` hangisinin çalışacağını seçer.

## Workspace: Tek çatı

Birbirine bağlı birkaç crate için kökte bir `Cargo.toml` yeter:

```toml
[workspace]
resolver = "3"
members = ["app", "calc"]

```

Üyelerin yalnızca kendi `Cargo.toml`'ı var; birbirine `path` ile bağlanırlar:

```toml
# app/Cargo.toml
[package]
name = "app"
version = "0.1.0"
edition = "2024"

[dependencies]
calc = { path = "../calc" }

```

Çalışınca:

```text
app/Cargo.toml   calc/Cargo.toml
app/src/main.rs  calc/src/lib.rs

$ cargo run -p app
42

$ cargo test -p calc --quiet
running 1 test
.
test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in
0.00s


running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in
0.00s
```

| Workspace ne verir | Sonuç |
|---|---|
| Tek `target/` klasörü | Aynı şey iki kez derlenmez |
| Tek `Cargo.lock` | Herkes aynı sürümü kullanır |
| `cargo test --workspace` | Hepsini birden sınar |
| `-p ad` | Tek üyeyle çalışır |

Sık kullanılan sürümleri kökte tek yere yazabilirsin: `[workspace.dependencies]`, üyede `serde.workspace = true`. Böylece sürüm yükseltmek tek satırlık iş olur.

## Feature: İsteğe bağlı kod

`feature`, derlemeye isteğe bağlı kod katar. Kullanmayan bedelini ödemez:

```toml
[package]
name = "shop"
version = "0.1.0"
edition = "2024"

[features]
default = ["color"]
color = []
shout = []

```

Kodda `#[cfg(feature = "...")]` ile seçilir:

```rust
fn greet() -> String {
    let text = String::from("hello");

    #[cfg(feature = "shout")]
    let text = text.to_uppercase();

    #[cfg(feature = "color")]
    let text = format!("[color] {text}");

    text
}

fn main() {
    println!("{}", greet());
}

```

Aynı kod, üç farklı derleme:

```text
$ cargo run
[color] hello

$ cargo run --features shout
[color] HELLO

$ cargo run --no-default-features
hello
```

| Komut | Anlamı |
|---|---|
| `cargo run` | `default` listesindekiler açık |
| `cargo run --features shout` | Üstüne `shout` da açık |
| `cargo run --no-default-features` | Hiçbiri açık değil |
| `cargo run --all-features` | Hepsi açık |

Kural: Feature **ekler**, çıkarmaz. İki bağımlılık aynı crate'i farklı feature'larla isterse Cargo ikisini birleştirir. Biri açıkken öteki kırılıyorsa tasarım yanlıştır.

Testte de aynı: `cargo test --all-features`. Kapalı olan kod derlenmediği için içindeki hatayı derleyici göremez.

## Koşullu derleme

`#[cfg(...)]` yalnızca feature için değil:

```rust
fn main() {
    #[cfg(target_os = "windows")]
    println!("windows build");

    #[cfg(not(target_os = "windows"))]
    println!("other build");

    if cfg!(debug_assertions) {
        println!("debug checks on");
    } else {
        println!("debug checks off");
    }
}
```

```text
windows build
debug checks on
```

`#[cfg]` kodu derlemeden çıkarır. `cfg!` makrosu ise yalnızca `true` ya da `false` verir; iki kol da derlenir. `debug_assertions`, `cargo build`'de açık, `--release`'te kapalıdır.

## Profiller

`dev` hızlı derler, `release` hızlı çalışır. Ayarları `Cargo.toml`'da değişir. Kendi profilini de tanımlayabilirsin; `inherits` hangisinden başlayacağını söyler:

```toml
[profile.small]
inherits = "release"
opt-level = "z"
lto = true
codegen-units = 1
strip = true
panic = "abort"

```

Aynı küçük programın üç profildeki boyutu (bu bilgisayarda ölçüldü):

```text
cargo build                   176 KB
cargo build --release         132 KB
cargo build --profile small   111 KB
```

| Ayar | Etkisi |
|---|---|
| `opt-level` | 0 iyileştirme yok, 3 en hızlı, `"z"` en küçük |
| `lto` | Crate'ler arası iyileştirme, derleme yavaşlar |
| `codegen-units = 1` | Daha iyi kod, daha yavaş derleme |
| `strip` | Hata ayıklama bilgisini atar |
| `panic = "abort"` | Yığın açılmaz, program küçülür |

## Derleme betiği

Kök klasördeki `build.rs`, crate'ten **önce** derlenip çalışır. Çıktısı derlemeye bilgi verir:

```rust
// build.rs
fn main() {
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rustc-env=BUILD_TAG=v7");
}

// src/main.rs
fn main() {
    println!("tag {}", env!("BUILD_TAG"));
}

```

```text
$ cargo run
tag v7
```

Tek kural: `build.rs` her derlemede çalışabilir, kısa ve yan etkisiz olmalı. İnternete çıkan ya da kaynak klasörüne yazan derleme betiği başkasının bilgisayarında sorun çıkarır; üreteceğin dosya `OUT_DIR`'e gider.

## Özet

- İş kütüphanede, `main.rs` ince; `src/bin/` birden çok program.
- Workspace: Tek `target/`, tek `Cargo.lock`, `-p ad`.
- Feature ekler; `#[cfg(feature = "...")]` kodu seçer.
- `#[cfg]` kodu çıkarır, `cfg!` yalnızca değer verir.
- Profiller boyut ve hız arasında seçim yaptırır.
- `build.rs` crate'ten önce çalışır; kısa tut.
