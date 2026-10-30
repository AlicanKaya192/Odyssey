## Paket ve program seçmek

| Komut | İş |
|---|---|
| `cargo run --bin report` | `src/bin/report.rs`'i çalıştır |
| `cargo run -p app` | Workspace'te `app` üyesini çalıştır |
| `cargo build --workspace` | Bütün üyeleri derle |
| `cargo test -p core` | Tek üyenin testleri |
| `cargo check` | Program üretmeden denetle, en hızlısı |

## Feature

| Komut | İş |
|---|---|
| `--features a,b` | Şunları da aç |
| `--no-default-features` | `default` listesini kapat |
| `--all-features` | Hepsini aç |
| `cargo tree -e features` | Hangi feature kimden geliyor |

## `Cargo.toml` parçaları

```toml
[package]
name = "shop"
version = "0.1.0"
edition = "2024"
default-run = "shop"

[features]
default = ["color"]
color = []
fancy = ["color"]

[dependencies]
core = { path = "../core" }

[profile.release]
strip = true
```

`fancy = ["color"]`: Bir feature başka bir feature'ı da açabilir. `default-run`: Birden çok program varken `cargo run` hangisini çalıştırsın.

## Derleme betiği komutları

`build.rs` bunları `println!` ile yazar:

| Satır | İş |
|---|---|
| `cargo:rustc-env=AD=değer` | Koda `env!("AD")` ile değer verir |
| `cargo:rerun-if-changed=dosya` | Yalnızca bu dosya değişince yeniden çalış |
| `cargo:warning=metin` | Derlemede uyarı göster |

`rerun-if-changed` yazılmazsa betik, paketteki herhangi bir dosya değişince yeniden çalışır.
