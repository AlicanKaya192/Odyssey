## Karşılaştırma

| Özellik | `&T` / `&mut T` | `*const T` / `*mut T` |
|---|---|---|
| Boş olabilir mi? | Hayır | Evet |
| Hizalı mı? | Her zaman | Söz yok |
| Ömür denetimi | Var | Yok |
| Takma ad denetimi | Var | Yok |
| Okumak | Güvenli | `unsafe` |
| `Copy` mi? | `&T` evet, `&mut T` hayır | İkisi de evet |
| `Send` / `Sync` | Türe göre | Hayır |

## Yaygın hatalar

| Hata | Neden yanlış |
|---|---|
| Yerel değişkenin işaretçisini döndürmek | İşlev bitince değer yok |
| `Vec`'e `push` sonrası eski `as_ptr` | Yeniden ayırma adresi değiştirir |
| `&mut` canlıyken işaretçiyle yazmak | Takma ad kuralı |
| `*p as u8` gibi hizasız bakış | Hizalı olmayabilir |

İkinci hata en sinsi olanı:

```rust
let mut list = vec![1];
let p = list.as_ptr();
list.push(2);
// p may point to freed memory now.
```

Burada `p`'yi okumak tanımsız davranış olabilir; kapasite yeterliyse olmayabilir de. Tam bu yüzden deneyerek öğrenilemez.

## Kural

Ham işaretçiyi mümkün olan en kısa süre tut. Çalışan bir `&T`'n varsa onu kullan; işaretçiye yalnızca derleyicinin kanıtlayamadığı noktada in, sonra hemen referansa dön.
