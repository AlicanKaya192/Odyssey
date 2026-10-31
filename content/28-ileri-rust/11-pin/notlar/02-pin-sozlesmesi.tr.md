## Söz neyi kapsar?

`Unpin` olmayan bir değer bir kez sabitlendiyse:

| Kural | Anlamı |
|---|---|
| Taşınmaz | `mem::swap`, `mem::replace`, sahipliği alıp başka yere koymak yok |
| Belleği geçersiz olmaz | Düşmeden önce üzerine yazılmaz, bellek serbest bırakılmaz |
| `Drop` çalışır | Sabitlenen değer düşmeden kaybolmaz |

Son satır önemlidir: Sabitlenmiş değerin `mem::forget` ile unutulup belleğinin başkasına verilmesi de sözü bozar. `pin!` ve `Box::pin` bunu kendiliğinden sağlar.

## unsafe nerede devreye girer?

| İşlem | Güvenli mi? | Neden |
|---|---|---|
| `pin!(f)` | Evet | Özgün değişken erişilemez |
| `Box::pin(f)` | Evet | İçerik yığında (heap), kutu tek sahip |
| `Pin::new(&mut t)` | Evet | Yalnızca `Unpin` için |
| `get_mut` | Evet | Yalnızca `Unpin` için |
| `get_unchecked_mut` | Hayır | Derleyici taşımadığını göremez |
| `Pin::new_unchecked` | Hayır | Derleyici sözü denetleyemez |

## Alan sabitlemenin kuralları

Bir alanı sabitlemeye karar verdiysen:

| Kural | Neden |
|---|---|
| O alanı `self`'ten dışarı taşıma | Söz |
| Yapı için `Unpin`'i elle yazma | Yoksa dış kod `get_mut` ile taşır |
| `Drop` içinde alanı taşıma | `drop`, `&mut self` alır, derleyici görmez |
| Düşürmeden belleği yeniden kullanma | Söz |

Sabitlemeyeceğin alanlarda bu kuralların hiçbiri yoktur: `Option::take` ile değeri çıkarabilirsin. `Map` alıştırmasındaki `func` böyledir.

Kısacası her alan için tek soru: Bu alanı `Pin` ile mi, düz `&mut` ile mi vereceğim? İkisini birden yapmak hatadır.

## Neden bu kadar karmaşık?

Başka dillerde çöp toplayıcı nesneleri taşırken referansları günceller. Rust'ta ise taşıma yalnızca bayt kopyasıdır ve hiç çalışma zamanı işi yoktur. Bu seçimin bedeli, kendini gösteren nadir durum için ayrı bir tür sözleşmesidir. Sıradan kullanıcı `async fn` ve `.await` yazar, bu ayrıntıyı derleyici halleder. `Pin` ile yüz yüze gelmek çoğunlukla kendi `Future`'ını elle yazarken olur.

## Elle yazmadan önce

Çoğu zaman sarmalayıcı yerine şunlar yeter:

| İhtiyaç | Daha kolay yol |
|---|---|
| Sırayla iki iş | `async` blok içinde iki `.await` |
| Sonucu dönüştürmek | `async { f(g().await) }` |
| Gerçek projede alan sabitleme | `pin-project` crate'i |
| Bir kapanıştan future | `std::future::poll_fn` |
