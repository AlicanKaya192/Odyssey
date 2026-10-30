## Şimdi ne yapabilirsin?

Bu modülü bitiren biri standart kütüphaneyle gerçek bir araç yazabilir: Kendi hata türü olan, testli, Clippy'den temiz geçen, işi kollara bölen bir program.

## Küçük proje fikirleri

| Proje | Hangi konular |
|---|---|
| Dosyada kelime sayan araç, her dosya bir kolda | `thread::scope`, `Mutex`, hata türü |
| Sınırlı boyutlu önbellek | Generic, `HashMap`, testler |
| Basit bir ifade hesaplayıcı | `enum`, `Box`, özyineleme, iterator |
| Eklenti gibi çalışan kurallar | `Box<dyn Trait>`, kapanış |

Biri için yaz, `cargo clippy` ve testlerle bitir. Okumak yetmez.

## Sıradaki modül: İleri Rust

Buraya kadar güvenli Rust'ı kullandın. İleri modül, kullandığın şeylerin nasıl yapıldığını açıyor:

| Konu | Soru |
|---|---|
| `unsafe` | Derleyicinin kanıtlayamadığını kim garanti eder? |
| Bellek düzeni, kendi `Vec`'in | `Vec` nasıl yazılır? |
| Varyans, `PhantomData` | Ömürler türlerle nasıl etkileşir? |
| Atomikler, kendi kilidin | `Mutex` nasıl yazılır? |
| `async`, `Future`, `Pin` | Tek kolda binlerce iş nasıl döner? |
| Makrolar | Kod yazan kod |
| FFI, `no_std` | C ile konuşmak, işletim sistemi olmadan çalışmak |

## Bu noktada okunacaklar

- **The Rust Programming Language**: Ücretsiz resmî kitap, modülle aynı konular.
- **Rust Atomics and Locks**: Kilit ve atomik işlemler için.
- `std` belgesi: `cargo doc --open` kendi projenin belgesini de yanında üretir.
