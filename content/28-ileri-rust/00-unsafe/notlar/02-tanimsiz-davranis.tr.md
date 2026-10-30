## Tanımsız davranış ne değildir?

| Sanılan | Gerçek |
|---|---|
| Program çöker | Çökmeyebilir, hiçbir şey göstermeyebilir |
| Rastgele bir değer okunur | Derleyici kodu tamamen silebilir |
| Yalnızca o satırı etkiler | Önceki satırlar bile değişebilir |
| Debug modda görünür | Yalnızca `--release`'te ortaya çıkabilir |

Derleyici, tanımsız davranışın **hiç olmadığını varsayarak** iyileştirir. "Bu dal olsaydı tanımsız olurdu, demek ki hiç çalışmıyor" diye o dalı silebilir. Bu yüzden sonuç tahmin edilemez.

## Kurallar listesi

Şunlar her zaman tanımsız davranıştır:

| Kural | Örnek |
|---|---|
| Geçersiz işaretçiyi okumak | Boş, silinmiş, sınır dışı |
| Hizasız okumak | `u32`'yi tek adresten `*p` ile |
| Takma ad kuralını bozmak | Canlı `&mut` varken başka yoldan değiştirmek |
| Geçersiz değer üretmek | `bool` 2, olmayan `enum` kolu, UTF-8 olmayan `str` |
| Veri yarışı | Kilitsiz iki kol, biri yazıyor |
| `&T` arkasındakini değiştirmek | `UnsafeCell` olmadan |

## Nasıl yakalanır?

| Araç | Ne yapar | Sınırı |
|---|---|---|
| Testler | Bazı hataları gösterir | Geçmesi kanıt değil |
| Miri | Programı yorumlar, çoğu kuralı denetler | Nightly gerekir, yavaş, FFI'yi çalıştırmaz |
| Sanitizer'lar | Bellek hatalarını çalışırken yakalar | Nightly, yalnızca geçilen yol |
| İnceleme | `// SAFETY:` yorumlarını okumak | İnsan gücü |

Bu patikada Miri ve sanitizer'lar kurulu değil, adlarını bilmen yeter. Gerçek bir `unsafe` crate yazarsan Miri'yi CI'a koy.

## Kısa kural

Bir `unsafe` bloğunun doğruluğunu yalnızca **tek bir çalıştırmayla** gösterdiysen hiçbir şey göstermedin. Gerekçe yaz, sonra kurallar listesiyle karşılaştır.
