## Yazımlar

| İş | Yazım |
|---|---|
| Fonksiyon | `fn f<T>(x: T) -> T` |
| İki parametre | `fn f<A, B>(a: A, b: B)` |
| Kısıt | `fn f<T: PartialOrd>(x: &T)` |
| İki kısıt | `fn f<T: PartialOrd + Copy>(x: T)` |
| Struct | `struct S<T> { x: T }` |
| Enum | `enum E<T> { A(T), B }` |
| Metotlar | `impl<T> S<T> { ... }` |
| Yalnızca bir tür | `impl S<f64> { ... }` |
| Sabit | `fn f<const N: usize>(a: [i32; N])` |
| Tür vermek | `f::<i32>(1)`, `Vec::<i32>::new()` |

## Ad gelenekleri

| Ad | Kullanım |
|---|---|
| `T`, `U` | Herhangi bir tür |
| `K`, `V` | Anahtar, değer (`HashMap<K, V>`) |
| `E` | Hata (`Result<T, E>`) |
| `N` | Sabit sayı |

Anlamlı olunca uzun ad da yazılır: `Item`, `Output`.

## Sık kısıtlar

| Kısıt | Ne sağlar |
|---|---|
| `PartialOrd` | `<`, `>` |
| `PartialEq` | `==`, `!=` |
| `Copy` | Atamada kopyalanır |
| `Clone` | `.clone()` |
| `Debug` | `{:?}` |
| `Display` | `{}` |

## Hatalar

| Kod | Anlamı | Çözüm |
|---|---|---|
| `E0369` | `T` üzerinde işleç yok | Kısıt ekle |
| `E0599` | `T` üzerinde metot yok | Kısıt ekle |
| `E0308` | Aynı `T` farklı türlerle | İkinci parametre |
| `E0282` | Tür çıkarılamadı | Turbofish ya da ek yazım |
| `E0107` | Yanlış sayıda tür parametresi | Sayıyı düzelt |
