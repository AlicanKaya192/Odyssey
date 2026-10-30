## repr seçenekleri

| Yazım | Ne yapar | Ne zaman |
|---|---|---|
| Yok | Derleyici seçer, söz yok | Neredeyse her zaman |
| `#[repr(C)]` | Yazılan sıra, C kuralları | FFI, dosya biçimi |
| `#[repr(transparent)]` | Tek alanın düzeni | Tür sarmalayıp çevirmek |
| `#[repr(packed)]` | Boşluk yok | Sabit biçimli baytlar |
| `#[repr(align(64))]` | Hiza büyür | Önbellek satırı |
| `#[repr(u8)]` | Enum etiketi `u8` | Sayıya çevrilen enum |

## Ölçüm

| Çağrı | Verdiği |
|---|---|
| `size_of::<T>()` | Bayt |
| `align_of::<T>()` | Hiza |
| `size_of_val(&x)` | Dilim için gerçek boyut |
| `offset_of!(T, alan)` | Alanın baştan uzaklığı |
| `needs_drop::<T>()` | Silinirken iş var mı |

`size_of` ve `align_of` önsözde; `offset_of!` için `use std::mem::offset_of;`.

## Elle yerleşim kuralı

`repr(C)`'de her alan, kendi hizasının katı olan ilk adrese konur. Sonda, toplam boyut en büyük hizanın katı olana kadar boşluk eklenir.

| Alan | Hiza | Konum |
|---|---|---|
| `a: u8` | 1 | 0 |
| `b: u32` | 4 | 4 (1, 2, 3 boş) |
| `c: u8` | 1 | 8 |
| Son | 4 | 9, 10, 11 boş, boyut 12 |

## Sık hata

Rust düzenine güvenip struct'ı olduğu gibi dosyaya yazmak. Bir sonraki derleyici sürümünde alan sırası değişebilir, dosya okunamaz olur. Baytları elle üret ya da `repr(C)` kullan; boşlukların da başlatılmamış olduğunu unutma.
