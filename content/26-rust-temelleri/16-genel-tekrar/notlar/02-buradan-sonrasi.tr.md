## Şu an ne yapabiliyorsun?

- Rust kurup Cargo ile proje açmak.
- Sahiplik ve ödünç alma hatalarını okuyup düzeltmek.
- Struct, enum ve `match` ile veriyi modellemek.
- `Vec`, `HashMap` ve metinle çalışmak.
- Hataları `Result` ve `?` ile yönetmek.
- Modüllere ayrılmış, test edilmiş küçük bir araç yazmak.

## Sıradaki modül: Rust'ta Derinleşmek

| Konu | Neden |
|---|---|
| Generic türler ve özellikler | Aynı kodu birçok türle kullanmak |
| Ömürler | Referans döndürmek |
| Closure ve iterator'lar | Kısa ve hızlı veri işleme |
| Akıllı işaretçiler | `Box`, `Rc`, `RefCell` |
| Eşzamanlılık | `thread`, kanal, `Arc`, `Mutex` |

## Kendi başına deneyebileceklerin

Küçük ama gerçek şeyler yaz:

| Proje | Pekiştirdiği |
|---|---|
| Sayı tahmin oyunu | Girdi, döngü, `match` |
| Yapılacaklar listesi (dosyaya kaydeden) | Struct, dosya, `Result` |
| CSV özetleyici | Metin, `HashMap`, hata |
| Kelime frekansı aracı | `entry`, sıralama |

## Kaynaklar

Resmî kitap "The Rust Programming Language" ücretsizdir ve `rustup doc --book` komutu bilgisayarındaki kopyasını açar. Standart kütüphane belgeleri `rustup doc --std` ile. İkisi de internetsiz çalışır.

## Takılınca

1. Hata metnini sonuna kadar oku.
2. `rustc --explain E0382` o hatayı örnekle anlatır.
3. Küçült: Hatayı gösteren en kısa kodu yaz. Çoğu zaman çözüm burada görünür.
