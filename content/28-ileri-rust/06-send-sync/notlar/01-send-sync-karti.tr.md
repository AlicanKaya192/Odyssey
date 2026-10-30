## Karar soruları

| Soru | Evet ise |
|---|---|
| Tür yalnızca sahip olduğu veriyi mi tutuyor? | `T: Send` şartıyla `Send` |
| `&self` ile hiçbir şey değişmiyor mu? | `T: Sync` şartıyla `Sync` |
| `&self` ile değişiyor, kilit ya da atomik var mı? | `T: Send` şartıyla `Sync` |
| `&self` ile kilitsiz değişiyor mu? | `Sync` **olamaz** |
| Paylaşılan sayaç atomik değil mi? | `Send` **olamaz** |

## Standart şablon

```rust
// SAFETY: MyVec owns its items, like Vec.
unsafe impl<T: Send> Send for MyVec<T> {}
// SAFETY: &MyVec only gives &T, so sharing it shares only &T.
unsafe impl<T: Sync> Sync for MyVec<T> {}
```

`Send` için `T: Send`, `Sync` için `T: Sync`. Sahip olan türlerin neredeyse hepsinde bu ikili doğrudur.

## Denemek

```rust
fn assert_send<T: Send>() {}
fn assert_sync<T: Sync>() {}

fn main() {
    assert_send::<MyVec<i32>>();
    assert_sync::<MyVec<i32>>();
}
```

Derleniyorsa söz var. Yanlış `unsafe impl` için hiçbir test yetmez; gerekçeyi `// SAFETY:` yorumuna yaz.

## Kapanış yakalamasında tuzak

Kapanış artık tek tek alanları yakalar. `SendPtr` sarmalayıcısı `Send` olsa bile:

```rust
let p = SendPtr(raw);
thread::spawn(move || unsafe { *p.0 = 1 });
```

`p.0` yakalanır, `p` değil. `p.0` ham işaretçidir ve `Send` değildir, derlenmez. Çözüm `p.get()` gibi bir yöntem çağırmaktır: Yöntem bütün `p`'yi yakalatır.
