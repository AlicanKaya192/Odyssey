## Üretmek

| Yazım | Sonuç |
|---|---|
| `&x as *const T` | Referanstan |
| `&raw const x` | Ara referans yok |
| `&raw mut x` | Ara referans yok, değişken |
| `list.as_ptr()` | Dilimin başı |
| `list.as_mut_ptr()` | Dilimin başı, değişken |
| `ptr::null()`, `ptr::null_mut()` | Boş |
| `Box::into_raw(b)` | Sahipliği bırakır |
| `NonNull::new(p)` | `Option<NonNull<T>>` |

## Kullanmak

| Yazım | İş | Şartı |
|---|---|---|
| `*p` | Oku | Geçerli, hizalı, canlı |
| `*p = v` | Eskiyi düşür, yaz | Eski değer geçerli |
| `p.add(i)` | `i` öğe ileri | Aynı bellek parçasında |
| `p.is_null()` | Boş mu | Şart yok, güvenli |
| `p.as_ref()` | `Option<&T>` | Boş değilse geçerli olmalı |
| `ptr::read(p)` | Bit bit oku | Sonra iki sahip olmasın |
| `ptr::write(p, v)` | Düşürmeden yaz | Eski değer sızabilir |
| `ptr::copy(a, b, n)` | `n` öğe, çakışabilir | Bellek işlemi gibi |
| `ptr::swap(a, b)` | İkisini değiştir | Geçerli olmalı |

## Referansa dönmek

```rust
let r: &i32 = unsafe { &*p };
let m: &mut i32 = unsafe { &mut *q };
```

Bu en sık yazılan dönüşümdür. Sonuçtaki referansın ömrü **uydurulur**: Derleyici işaretçiden ömür çıkaramaz, istediğin ömrü verir. Değerden uzun yaşamamasını sen sağlarsın.

## Türler arası

| Yazım | Anlamı |
|---|---|
| `p as *const u8` | Başka tür gibi bak |
| `p as usize` | Sayıya çevir (adres) |
| `p.cast::<u8>()` | Daha okunaklı `as` |
