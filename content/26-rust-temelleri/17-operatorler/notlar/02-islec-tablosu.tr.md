## Öncelik sırası

Üstteki önce yapılır. Aynı satırdakiler soldan sağa çalışır; atama sağdan sola.

| Sıra | İşleçler |
|---|---|
| 1 | Metot çağrısı `x.pow(2)`, dizi erişimi `a[0]` |
| 2 | Tek taraflı `-x`, `!x` |
| 3 | `as` |
| 4 | `*` `/` `%` |
| 5 | `+` `-` |
| 6 | `<<` `>>` |
| 7 | `&` |
| 8 | `^` |
| 9 | <code>&#124;</code> |
| 10 | `==` `!=` `<` `>` `<=` `>=` |
| 11 | `&&` |
| 12 | <code>&#124;&#124;</code> |
| 13 | `=` `+=` `-=` `*=` `/=` `%=` |

Ezberleme. Şüphen varsa parantez yaz.

## Bit işleçleri

Bu işleçler sayının ikilik yazılışına bakar, bit bit çalışır. Başlangıçta nadiren gerekir; `^`'nin neden üs olmadığını
anlaman için burada.

```rust
fn main() {
    println!("{}", 12 & 10);
    println!("{}", 12 | 10);
    println!("{}", 12 ^ 10);
    println!("{}", 1 << 3);
    println!("{}", 16 >> 2);
    println!("{}", !0_u8);
}
```

```text
8
14
6
8
4
255
```

| İşleç | Ne yapar | Örnek |
|---|---|---|
| `&` | İki bit de 1 ise 1 | `12 & 10` = 8 |
| <code>&#124;</code> | Biri 1 ise 1 | <code>12 &#124; 10</code> = 14 |
| `^` | Yalnızca biri 1 ise 1 | `12 ^ 10` = 6 |
| `<<` | Sola kaydırır (2 ile çarpmak gibi) | `1 << 3` = 8 |
| `>>` | Sağa kaydırır (2'ye bölmek gibi) | `16 >> 2` = 4 |
| `!` | Bitleri ters çevirir | `!0_u8` = 255 |

## `&` ve `&&` aynı değil

`bool` değerlerde `&` da çalışır ama kısa devre **yapmaz**: İki tarafı da hesaplar. Bu yüzden derslerdeki güvenli
yazım tek `&` ile panikler:

```rust
fn main() {
    let items = "".len();
    println!("{}", (items != 0) & (10 / items > 1));
}
```

```text
thread 'main' panicked at main.rs:3:36:
attempt to divide by zero
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Şart birleştirirken her zaman `&&` ve `||` yaz.
