## Her gün kullanılanlar

| Komut | Ne yapar |
|---|---|
| `cargo new ad` | Yeni proje klasörü açar |
| `cargo init` | Var olan klasörü proje yapar |
| `cargo run` | Derler ve çalıştırır |
| `cargo build` | Derler, `target/debug/` |
| `cargo build --release` | İyileştirerek derler, `target/release/` |
| `cargo check` | Yalnızca denetler, program üretmez |
| `cargo test` | Testleri çalıştırır |
| `cargo fmt` | Kodu standart biçime sokar |
| `cargo clippy` | Yaygın hataları ve kötü kalıpları bulur |
| `cargo doc --open` | Projenin belgelerini üretip açar |
| `cargo add ad` | `Cargo.toml`'a paket ekler |
| `cargo update` | `Cargo.lock`'taki sürümleri günceller |
| `cargo clean` | `target` klasörünü siler |

## Programa argüman vermek

`cargo run` ile program arasındaki argümanları `--` ayırır:

```bash
cargo run -- first second
```

`--` öncesi Cargo'ya, sonrası senin programına gider.

## Hangi dosyalar Git'e gider?

| Dosya | Git'e girer mi | Neden |
|---|---|---|
| `src/` | Evet | Kaynak kod |
| `Cargo.toml` | Evet | Projenin tarifi |
| `Cargo.lock` | Program ise evet | Herkes aynı sürümleri alsın |
| `target/` | Hayır | Yeniden üretilebilir ve çok büyür |

`cargo new` bunu bilir ve `target` klasörünü `.gitignore` dosyasına kendisi yazar.

## target neden bu kadar büyük?

Her derleme ara dosyalar bırakır. Birkaç projede gigabaytları bulabilir. Silmek güvenlidir:
`cargo clean` yeter, sonraki derleme biraz uzun sürer.
