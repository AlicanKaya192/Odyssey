## Tekrar eden kod

Hata enum'u büyüdükçe `Display` ve `From` yazmak sıkıcılaşır. Rust dünyasında bunun için iki yaygın crate var. **Bu patikada kurulmuyorlar**, aşağıdaki kutular burada çalıştırılmadı; adlarını başka projelerde göreceksin diye yazıyorum.

## thiserror: Kütüphane için

Dersteki enum'u makroyla yazar. Elde edilen, elle yazdığınla aynı türdür:

```rust
#[derive(Debug, thiserror::Error)]
enum AppError {
    #[error("bad number")]
    Parse(#[from] std::num::ParseIntError),

    #[error("age {0} is negative")]
    Negative(i64),
}
```

## anyhow: Uygulama için

`Box<dyn Error>`'ın gelişmişi. Bağlam eklemek tek satır:

```rust
fn read_port(text: &str) -> anyhow::Result<u16> {
    let port = text.parse().context("reading the port")?;
    Ok(port)
}
```

## Önce elle

Makronun ne ürettiğini bilmek için en az bir kez elle yaz. Dersteki her şey standart kütüphaneyle çalışıyor:

| Elle | Crate |
|---|---|
| `impl Display` | `#[error("...")]` |
| `impl From` | `#[from]` |
| `fn source` | `#[source]` |
| `Box<dyn Error>` | `anyhow::Error` |
| `map_err` ile bağlam | `.context("...")` |
