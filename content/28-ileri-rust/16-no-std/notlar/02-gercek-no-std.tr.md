## Kütüphaneden programa

Ders boyunca `no_std` kütüphane yazdık. Gerçek bir `no_std` **program** (cihazda çalışan) şunları da ister, çünkü `std`'nin yaptığı işleri artık kimse yapmıyor:

| Eksik | Çözüm |
|---|---|
| Panikte ne olacak | `#[panic_handler]` |
| Program nereden başlıyor | `#![no_main]` ve cihazın başlangıç kodu |
| Bellek ayırıcı (`alloc` kullanılacaksa) | `#[global_allocator]` |
| Hedef | `--target thumbv7em-none-eabihf` gibi |

Bu program masaüstünde çalıştırılamaz; o yüzden Odyssey'de yalnızca kütüphane denedik.

## Panic işleyici

`no_std`'de paniğin ne yapacağına sen karar verirsin:

```rust
#![no_std]

use core::panic::PanicInfo;

#[panic_handler]
fn on_panic(_info: &PanicInfo) -> ! {
    loop {}
}
```

Bu kod derlenir (`cargo build -p tiny` ile ölçtük). Dönüş türü `!`, çünkü panikten sonra devam yoktur. Cihazda genelde hata ışığını yakıp bekler ya da yeniden başlatır.

Dikkat: Kütüphane `panic_handler` yazmaz. Programda yalnızca bir tane olabilir ve `std` zaten bir tane getirir; ikisi birden derlenmez. İşleyici nihai programın işidir.

## Cihaz tarafı

| Kavram | Anlamı |
|---|---|
| Hedef (target) | İşlemci ve ortam üçlüsü; `rustup target add` ile eklenir |
| `none` | Hedef adında işletim sistemi yok demek |
| Bellek haritası | Kodun ve verinin nereye yerleşeceği, bağlayıcı betiğiyle |
| Çevre birimi | Bellek adresine yazarak kontrol edilen donanım |
| `volatile` | Derleyici bu okuma ve yazmayı silmesin diye |

Son satırın aracı `core::ptr::read_volatile` ve `write_volatile`'dır.

## Bilinen adlar

| Crate | İşi |
|---|---|
| `embassy` | Gömülü async çalıştırıcı |
| `heapless` | Sabit kapasiteli `Vec` ve `String` |
| `embedded-hal` | Donanım için ortak trait'ler |
| `cortex-m-rt` | ARM başlangıç kodu |
| `libm` | Kayan nokta matematiği |

Bu patikada kurulu değiller, adlarını bilmen yeter.

## Ne zaman düşünmeli?

Gömülü yazmıyorsan bile kütüphanene `no_std` desteği koymak onu her yerde kullanılabilir yapar ve yanlışlıkla işletim sistemine bağlanmasını önler. Ayrımı en başta yapmak ucuz, sonradan eklemek pahalıdır. Ama uygulama yazıyorsan `std` kullan: Bu bir erdem değil, bir ihtiyaçtır.
