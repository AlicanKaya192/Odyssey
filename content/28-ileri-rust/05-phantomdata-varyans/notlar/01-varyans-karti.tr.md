## Tablo

| Tür | `'a` için | `T` için |
|---|---|---|
| `&'a T` | Kovaryant | Kovaryant |
| `&'a mut T` | Kovaryant | **Değişmez** |
| `Box<T>`, `Vec<T>`, `Rc<T>` | - | Kovaryant |
| `Cell<T>`, `RefCell<T>`, `Mutex<T>` | - | **Değişmez** |
| `*const T`, `NonNull<T>` | - | Kovaryant |
| `*mut T` | - | **Değişmez** |
| `fn(T)` | - | Kontravaryant |
| `fn() -> T` | - | Kovaryant |

## Kısa kural

| Soru | Cevap |
|---|---|
| Tür içeriği yalnızca okuyor mu? | Kovaryant olabilir |
| Tür içine yazabiliyor mu? | Değişmez olmalı |
| Tür `T`'yi yalnızca alıyor mu? | Kontravaryant |

## Struct'ta birleşme

Bir parametre birkaç alanda geçiyorsa en katı olan kazanır:

```rust
struct Pair<'a, T> {
    read: &'a T,        // covariant in T
    cell: Cell<T>,      // invariant in T
}
// Pair is invariant in T.
```

## Hata nasıl görünür?

Varyans hatası kendini açıkça söylemez. Şunları görürsen akla varyans gelsin:

- `does not live long enough`, ama değer yeterince uzun görünüyor.
- `lifetime may not live long enough`, `requires that 'a must outlive 'static` gibi.
- Notta `&mut` ya da `Cell` geçiyorsa neredeyse kesin.

Çözüm çoğu zaman kodun doğru olmadığını kabul etmektir: Derleyici gerçek bir sallanan referansı önlüyor.
