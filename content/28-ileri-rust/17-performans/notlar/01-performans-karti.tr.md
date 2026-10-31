## Derleme ayarları

`Cargo.toml` içinde `[profile.release]` altına:

| Ayar | Etkisi | Bedeli |
|---|---|---|
| `opt-level = 3` | En yüksek hız (release varsayılanı) | Yok |
| `opt-level = "s"` | Küçük dosya | Biraz yavaş |
| `lto = "fat"` | Crate'ler arası eniyileme | Derleme çok uzar |
| `lto = "thin"` | Benzer kazanç, daha ucuz | Derleme uzar |
| `codegen-units = 1` | Daha iyi eniyileme | Derleme uzar |
| `panic = "abort"` | Küçük dosya, yığın açma kodu yok | `catch_unwind` çalışmaz |
| `strip = true` | Sembolleri atar, küçük dosya | Yığın dökümü zayıflar |
| `debug = true` | Profiler için sembol | Dosya büyür |

Hangisinin ne kazandırdığı projeye bağlıdır; aç ve ölç.

## Ayırma azaltmak

| Yerine | Şunu dene |
|---|---|
| `Vec::new()` + `push` | `Vec::with_capacity(n)` |
| Döngüde `format!` | `clear()` + `write!` |
| `s.clone()` | `&s` ya da `&str` |
| `String` parametre | `&str` parametre |
| `Vec<T>` parametre | `&[T]` parametre |
| Bazen değişen metin | `Cow<str>` |
| Kısa ömürlü `Vec` | Dışarıdan verilen `&mut Vec`, tekrar kullanım |
| `collect` sonra gezmek | Doğrudan iterator zinciri |

## Bellek düzeni

| Durum | Yap |
|---|---|
| Büyük varyantlı `enum` | Büyüğü `Box`'a al |
| Çok öğe, az alan kullanımı | Ayrı diziler (SoA) |
| İç içe `Vec<Vec<T>>` tablo | Tek `Vec<T>`, `satır * genişlik + sütun` |
| Çok küçük liste | Dizi, doğrusal arama çoğu zaman yeter |
| Bağlı liste | Genelde `Vec` ya da `VecDeque` daha hızlı |

## Veri yapısı seçimi

| İhtiyaç | Tür |
|---|---|
| Sıralı erişim, sona ekleme | `Vec` |
| İki uçtan ekleme | `VecDeque` |
| Anahtarla arama | `HashMap` |
| Sıralı anahtar, aralık | `BTreeMap` |
| En büyüğü almak | `BinaryHeap` |

## inline ne zaman?

Derleyici crate içinde kendi karar verir. `#[inline]` çoğunlukla crate'ler arası küçük fonksiyonlarda anlamlıdır. Her yere yazmak derlemeyi uzatır ve dosyayı büyütebilir; ölçmeden ekleme.
