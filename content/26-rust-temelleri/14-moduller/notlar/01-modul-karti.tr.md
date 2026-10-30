## Komutlar ve yazımlar

| İş | Yazım |
|---|---|
| Satır içi modül | `mod a { ... }` |
| Dosyadan modül | `mod a;` |
| Dışarı açmak | `pub fn`, `pub struct`, `pub mod` |
| Kısa ad | `use a::b;` |
| Birkaç ad | `use a::{b, c};` |
| Yeni adla | `use a::b as c;` |
| Hepsi | `use a::*;` (testler dışında kaçın) |
| Yeniden açmak | `pub use a::b;` |

## Dosya nerede aranır?

| Bulunduğun yer | Yazdığın | Aranan |
|---|---|---|
| `src/main.rs` | `mod net;` | `src/net.rs` |
| `src/net.rs` | `mod tcp;` | `src/net/tcp.rs` |

Bulunamazsa `E0583` alırsın ve hata iki olası yolu da söyler.

## Hata kodları

| Kod | Anlamı |
|---|---|
| `E0603` | Bu ad gizli (`pub` eksik) |
| `E0616` | Struct alanı gizli |
| `E0433` | Yol bulunamadı (`use` ya da `mod` eksik) |
| `E0432` | `use` edilen şey yok |
| `E0583` | Modül dosyası yok |
