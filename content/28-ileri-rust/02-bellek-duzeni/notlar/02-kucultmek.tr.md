## Bellek nerede gider?

Bir tür milyonlarca kez tutuluyorsa birkaç bayt fark eder. Önce ölç: `size_of::<T>()` derlerken bellidir.

| Yol | Örnek | Kazanç |
|---|---|---|
| Küçük tamsayı | `u64` yerine `u32` | Alan başına 4 bayt |
| Enum'u küçültmek | Büyük kolu `Box`'a al | Bütün enum küçülür |
| `Box<str>`, `Box<[T]>` | `String`, `Vec` yerine | Kapasite alanı yok (24 yerine 16 bayt) |
| Boş değerli tür | `Option<NonZeroU32>` | Etiket yok |

## Enum'da en büyük kol

Enum, **en büyük kolu** kadar yer tutar. Bir kol 200 bayt ise hepsi 200 bayttır:

```rust
enum Event {
    Click(u8),
    Report([u8; 200]),
}
```

Büyük kolu kutuya almak bütün değerleri küçültür: `Report(Box<[u8; 200]>)`. Bu durumda enum 16 bayt olur, ama büyük kol için öbek ayırması eklenir. Clippy `large_enum_variant` ile uyarır.

## Sıfır boyutlu türler

`()` ve alansız struct yer tutmaz, bu yüzden tür olarak bilgi taşıyabilirler:

| Kullanım | Örnek |
|---|---|
| Yalnızca anahtar saklamak | `HashSet<T>` içeride `HashMap<T, ()>` |
| Tür düzeyinde durum | `struct Open; struct Closed;` |
| Sahiplik işareti | `PhantomData<T>` (ileride) |

## Ölç, sonra küçült

Bellek küçültmek okunabilirliği düşürür. Bir `Vec<Item>`'ın toplam boyutu `len * size_of::<Item>()`: Sayı küçükse uğraşma.
