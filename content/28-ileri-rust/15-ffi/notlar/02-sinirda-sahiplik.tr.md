## Tek kural: Kim ayırdıysa o siler

Rust ile C farklı bellek ayırıcıları kullanabilir. Birinin ayırdığını öbürünün silmesi tanımsız davranıştır.

| Bellek nereden | Nasıl silinir |
|---|---|
| Rust `Box::into_raw` | Rust `Box::from_raw`, senin verdiğin `_free` ile |
| Rust `CString::into_raw` | Rust `CString::from_raw` |
| C `malloc` | C `free` |
| C kütüphanesi `xyz_new` | Kütüphanenin `xyz_free`'si |

Belgesi olmayan bir C fonksiyonu işaretçi döndürüyorsa ilk soru şudur: Bunu kim silecek? `getenv`'in sonucunu silmek yanlıştır, sahibi çalışma kitaplığıdır.

## Sınırda hata

C'de `Result` yoktur. Hata genelde dönüş değeriyle söylenir:

| Kalıp | Örnek |
|---|---|
| Sıfır başarı, negatif hata | `0`, `-1` |
| Boş işaretçi hata | `fopen` |
| Ayrı hata çıktısı | `int f(int *out)` |

Rust'a bakan sarmalayıcı bunu `Result`'a çevirir, C'ye bakan fonksiyon da `Result`'ı koda çevirir. `Result` ya da `Option<&T>` gibi Rust türlerini sınırdan geçirmeyi plansız yapma; `Option<&T>` ve `Option<Box<T>>` boş işaretçiyle aynı düzendedir, ötekiler için bu söz yoktur.

## Kol ve yaşam süresi

| Soru | Neden |
|---|---|
| Fonksiyon aynı anda iki koldan çağrılabilir mi? | C kütüphanesi söz vermiyorsa kilit gerekir |
| Geri çağrı hangi kolda çalışır? | Değer `Send` olmalı olabilir |
| C işaretçiyi saklıyor mu? | Saklıyorsa değerin yaşam süresi senin sorumluluğun |
| Tutamaç iki kez silinirse? | Çift silme, tanımsız davranış |

Tutamaç türüne `Send` ve `Sync` kendiliğinden gelmez, çünkü ham işaretçiler ikisini de kaldırır. Söz verebiliyorsan `unsafe impl` yazılır.

## Araçlar

| Araç | Yönü | İşi |
|---|---|---|
| `bindgen` | C → Rust | Başlıktan `extern` bildirimi üretir |
| `cbindgen` | Rust → C | Koddan C başlığı üretir |
| `cc` crate'i | C → Rust | `build.rs`'te C kaynağını derler |
| `libc` crate'i | C → Rust | C kitaplığı bildirimleri hazır |
| `pyo3` | Python ↔ Rust | Python modülü yazmak |

Bu patikada kurulu değiller, adlarını bilmen yeter.

## Bağlama

| İhtiyaç | Yazım |
|---|---|
| Kütüphaneyi belirtmek | `#[link(name = "z")]` |
| `build.rs`'ten | `cargo:rustc-link-lib=z` |
| Arama yolu | `cargo:rustc-link-search=yol` |

## Değişken sayıda argüman

`printf` gibi fonksiyonlar `fn printf(format: *const c_char, ...) -> c_int;` diye bildirilir. Denetim yoktur: Biçim metniyle argümanlar tutmazsa tanımsız davranış olur. Ayrıca bazı C kitaplıklarında bu fonksiyonlar başlık içinde tanımlıdır ve bağlanamaz. Mümkünse kullanma.
