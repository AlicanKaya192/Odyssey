## Belge yorumları

| Yazım | Neyi anlatır |
|---|---|
| `///` | Altındaki öğeyi |
| `//!` | İçinde bulunduğu modülü ya da crate'i |

Markdown yazılır. Yaygın başlıklar: `# Examples`, `# Errors`, `# Panics`.

```rust
/// Parses a price in cents.
///
/// # Errors
///
/// Returns an error if the text is not a number.
///
/// # Examples
///
/// ```
/// assert_eq!(shop::cents("12"), Ok(12));
/// ```
pub fn cents(text: &str) -> Result<u32, String> {
    text.parse().map_err(|_| String::from("not a number"))
}
```

| Komut | İş |
|---|---|
| `cargo doc --open` | Belge sitesini üret, aç |
| `cargo test --doc` | Yalnızca belge testleri |

Belgedeki kod blokları derlenir ve çalıştırılır, belge eskimez. `no_run`, `ignore`, `should_panic` etiketleri koda yazılabilir.

## Test yazmamak için bahaneler

| Bahane | Gerçek |
|---|---|
| "Derleyici yakalıyor" | Tür yanlışını yakalar, mantık yanlışını yakalamaz |
| "Elle denedim" | Bir sonraki değişiklikte yine deneyecek misin? |
| "Küçük fonksiyon" | Küçükse test de küçük |
