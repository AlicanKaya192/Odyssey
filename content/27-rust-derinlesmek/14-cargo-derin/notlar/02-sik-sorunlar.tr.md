## Sık karşılaşılanlar

| Belirti | Sebep | Çözüm |
|---|---|---|
| `could not determine which binary to run` | Birden çok program var | `--bin ad` ya da `default-run` |
| `cargo run` kökte çalışmıyor | Workspace'te birden çok program var | `-p ad` |
| Üyede `use core::...` bulunamıyor | `[dependencies]`'te `path` yok | `core = { path = "../core" }` |
| Kapalı feature'daki hata görünmüyor | O kod derlenmedi | `--all-features` ile de derle |
| Feature açınca başka yer bozuldu | Feature ekleyici değil | İki yolu ayrı yap, birbirini silmesin |
| Derleme betiği her seferinde çalışıyor | `rerun-if-changed` yok | Satırı ekle |
| `env!` derlenmiyor: `not defined` | Değer verilmemiş | `build.rs`'i ve yazımını kontrol et |

## Ne zaman workspace?

| Durum | Karar |
|---|---|
| Tek program, birkaç modül | Workspace gerekmez, modül yeter |
| Kütüphane + program | Tek paket yeter (`lib.rs` + `main.rs`) |
| Birbirinden ayrı yayınlanan parçalar | Workspace |
| Derleme süresi uzadı, parçalar bağımsız | Workspace: Değişmeyen üye yeniden derlenmez |

Baştan bölme. Modülle başla; sınır netleşince crate'e çıkar. Modülden crate'e geçmek sonradan kolaydır, yanlış sınırı geri almak zordur.

## Feature adları

| İyi | Neden |
|---|---|
| `json`, `tls` | Ne eklediğini söylüyor |
| `no-std` yerine `std` | Feature ekler; `std` varsayılanda açık olur |

Ters adlar (`no-color`) kuralı bozar: İki bağımlılıktan biri isterse herkes için kapanır.
