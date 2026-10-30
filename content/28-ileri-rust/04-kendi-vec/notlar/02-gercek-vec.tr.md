## Bu sürümün eksikleri

| Eksik | Gerçek Vec ne yapar | Neden |
|---|---|---|
| ZST | Bellek ayırmaz, `cap` en büyük değer | `Vec<()>` sayaç gibi çalışır |
| `Send` / `Sync` | `unsafe impl` var | `NonNull` kendiliğinden vermez |
| Varyans | `PhantomData<T>` ile doğru | Sonraki bölüm |
| `Vec::with_capacity` | Var | Baştan ayırma |
| `Drain`, `extend` | Panik güvenli | Koruyucu kalıbıyla |

## RawVec neden ayrı?

Gerçek `Vec`, belleği yöneten `RawVec` ile öğeleri yöneten `Vec`'e bölünür. `RawVec` öğelerin dolu olduğunu bilmez, yalnızca bellek ayırıp geri verir. Sorumlulukları ayırmak `unsafe`'in nerede olduğunu daraltır: `IntoIter` da `RawVec` kullanarak aynı kodu paylaşır.

## Büyüme neden ikiye katlıyor?

| Yöntem | 1000 `push`'ta kopya sayısı |
|---|---|
| Her seferinde +1 | Yaklaşık 500 000 |
| İkiye katlama | 1000'den az |

İkiye katlama, ortalama `push` başına sabit iş demektir. Bedeli, kapasitenin yarısının boş kalabilmesi. Boyutu baştan biliyorsan `with_capacity` hepsini önler.

## Kendi yapını yazmalı mısın?

Neredeyse hiçbir zaman. Bu bölümün amacı `Vec`'in nasıl çalıştığını görmek ve `unsafe`'i küçük bir yerde kullanmaktır. Gerçek projede önce `Vec`, `VecDeque`, `HashMap`; yetmezse iyi denenmiş bir crate.
