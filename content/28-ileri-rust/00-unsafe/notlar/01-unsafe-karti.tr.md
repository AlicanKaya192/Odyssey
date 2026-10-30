## Yazarken sor

| Soru | Cevap hayırsa |
|---|---|
| Güvenli yolu gerçekten yok mu? | `unsafe` yazma |
| İşaretçi geçerli mi, hizalı mı? | Tanımsız davranış |
| Gösterdiği değer türüne uygun mu? | Tanımsız davranış |
| Aynı anda başka `&mut` var mı? | Tanımsız davranış |
| `// SAFETY:` yazabiliyor muyum? | Kod muhtemelen yanlış |

## Yazım

```rust
// SAFETY: i < len was checked just above, so the index is in bounds.
let value = unsafe { *list.get_unchecked(i) };
```

```rust
/// Returns the item at `i`.
///
/// # Safety
///
/// `i` must be smaller than `list.len()`.
unsafe fn item_at(list: &[i32], i: usize) -> i32 {
    // SAFETY: the caller guarantees i is in bounds.
    unsafe { *list.get_unchecked(i) }
}
```

| Yorum | Yeri | Kime |
|---|---|---|
| `// SAFETY:` | `unsafe` bloğunun üstü | Kodu okuyana: Neden doğru |
| `# Safety` | `unsafe fn` belgesi | Çağırana: Ne garanti etmeli |

## Kapsam

`unsafe` bloğunu küçük tut. Güvenlik yalnızca blokta değil, modülün tamamında korunur: Blok dışındaki bir satır, bloğun güvendiği şartı bozabilir. Bu yüzden `unsafe` içeren türün alanları `pub` olmaz.

## Sık kullanılan çağrılar

| Çağrı | Şartı |
|---|---|
| `get_unchecked(i)` | `i < len` |
| `slice::from_raw_parts(p, n)` | `n` öğe geçerli ve canlı |
| `String::from_utf8_unchecked(v)` | `v` geçerli UTF-8 |
| `Box::from_raw(p)` | `p`, `Box::into_raw`'dan geldi |
| `mem::transmute::<A, B>(x)` | Aynı boyut, geçerli bit deseni |

`transmute` en tehlikelisidir; önce `as`, `from_ne_bytes` gibi güvenli yollara bak.
