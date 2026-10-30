## Bellek çağrıları

| Çağrı | İş | Şartı |
|---|---|---|
| `Layout::new::<T>()` | Tek `T` | Yok |
| `Layout::array::<T>(n)` | `n` tane `T` | Taşarsa `Err` |
| `alloc::alloc(layout)` | Bellek al | Boyut sıfır olamaz |
| `alloc::realloc(p, old, size)` | Büyüt | `p` aynı düzenle ayrıldı |
| `alloc::dealloc(p, layout)` | Geri ver | `p` aynı düzenle ayrıldı |
| `handle_alloc_error(layout)` | Bellek bitti | Çıkar, dönmez |

`alloc` boş işaretçi döndürebilir: Bellek biterse. Denetlemek şart.

## Yerleri taşımak

| Çağrı | İş |
|---|---|
| `ptr::write(p, v)` | Yaz, eskiyi düşürme |
| `ptr::read(p)` | Sahipliği çıkar |
| `ptr::copy(a, b, n)` | `n` öğe taşı, çakışabilir |
| `ptr::copy_nonoverlapping(a, b, n)` | Daha hızlı, çakışamaz |

`insert` şöyle kaydırır:

```rust
unsafe {
    let p = self.ptr.as_ptr().add(index);
    ptr::copy(p, p.add(1), self.len - index);
    ptr::write(p, value);
}
self.len += 1;
```

`remove` tersi: Önce değeri `read`, sonra kalanları bir öne `copy`, en son `len -= 1`.

## Kontrol listesi

| Soru | Yanlış olursa |
|---|---|
| Her `alloc`'un tek `dealloc`'u var mı? | Sızıntı ya da iki kez silme |
| `dealloc` aynı `Layout` ile mi? | Tanımsız davranış |
| Her dolu öğe tek kez mi düşüyor? | Sızıntı ya da iki kez silme |
| `realloc`'tan sonra eski işaretçi kaldı mı? | Tanımsız davranış |
| `len` yazmadan önce mi arttı? | Panikte tanımsız davranış |
