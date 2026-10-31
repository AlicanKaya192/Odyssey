## Şimdi ne yapabilirsin?

Bu modülü bitiren biri Rust'ın en alt katmanlarını okuyup yazabilir: Kendi veri yapısını `unsafe` ile kurar, sözünü türe yazar, kilitsiz kodun neden zor olduğunu bilir, bir `async fn`'in altında ne olduğunu açıklayabilir.

## Okumak için iyi kaynaklar

| Kaynak | Konusu |
|---|---|
| The Rustonomicon | `unsafe`, sahiplik, bellek |
| Rust Atomics and Locks | Atomikler, kilitler, işlemci |
| Asynchronous Programming in Rust | `async` ve çalıştırıcılar |
| The Little Book of Rust Macros | Makro teknikleri |
| The Rust Reference | Dilin tam tarifi |

## Küçük proje fikirleri

| Proje | Hangi konular |
|---|---|
| Kendi `HashMap`'in | `unsafe`, `Layout`, `Drop`, testler |
| Çok işçili çalıştırıcı | Atomikler, iş çalma, `Pin` |
| `no_std` bir ayrıştırıcı | `core`, sabit tampon, const generic |
| Bir C kütüphanesine güvenli sarmalayıcı | FFI, sahiplik, `Drop` |
| `#[derive]` yazan bir yardımcı | Procedural makro |

Biri için yaz, test et ve `unsafe` varsa `miri` ile çalıştır. Okumak yetmez.

## Gerçek ekosistem

Bu patikada standart kütüphaneyle kaldık. Gerçek projelerde sık göreceğin crate'ler:

| Crate | İşi |
|---|---|
| `tokio` | Async çalışma ortamı, ağ |
| `serde` | Serileştirme |
| `clap` | Komut satırı |
| `crossbeam` | Eşzamanlılık araçları |
| `rayon` | Veri paralelliği |
| `axum` | Web sunucusu |
| `sqlx` | Veritabanı |

## Ne öğrendin, neyi bırak?

Bu modüldeki tekniklerin çoğu günlük kodda gerekmez. `Mutex` yerine atomik, `Vec` yerine kendi yapın, fonksiyon yerine makro genelde yanlış seçimdir. Kazancın onları her yerde kullanmak değil: Kullanılması gerektiğinde tanımak, kullanıldığı kodu okuyabilmek ve bir hata çıktığında nereye bakacağını bilmektir.
