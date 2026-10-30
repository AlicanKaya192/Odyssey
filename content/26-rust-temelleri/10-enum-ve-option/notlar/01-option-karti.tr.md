## Hangi yolu seçmeli?

| Niyetin | Yaz |
|---|---|
| İki durumu da ele almak | `match` |
| Yalnızca değer varsa bir şey yapmak | `if let Some(x) = ...` |
| Yoksa varsayılan kullanmak | `.unwrap_or(0)` |
| Yoksa hesaplanan varsayılan | <code>.unwrap_or_else(&#124;&#124; ...)</code> |
| Türün varsayılanı | `.unwrap_or_default()` |
| Değeri dönüştürmek | <code>.map(&#124;x&#124; ...)</code> |
| Dönüştürme de `Option` veriyor | <code>.and_then(&#124;x&#124; ...)</code> |
| Sonda düşüp fonksiyondan çıkmak | `?` (`13`. bölüm) |
| "Burada kesin var" | `.expect("neden")` |

## Örnekler

```rust
fn first_digit(text: &str) -> Option<u32> {
    text.chars().next().and_then(|c| c.to_digit(10))
}

fn main() {
    println!("{:?}", first_digit("7up"));
    println!("{:?}", first_digit("abc"));
    println!("{:?}", first_digit(""));
    println!("{}", first_digit("7up").map(|d| d + 1).unwrap_or(0));
    println!("{}", first_digit("x").unwrap_or_default());
}
```

```text
Some(7)
None
None
8
0
```

## Sahiplik ve Option

`Option<String>` üzerinde `match` değeri taşıyabilir. Ödünç almak için `&` ya da `.as_ref()` kullanılır:

```rust
fn main() {
    let name = Some(String::from("Ada"));
    if let Some(text) = &name {
        println!("{text}");
    }
    println!("{:?}", name);
    let length = name.as_ref().map(|t| t.len());
    println!("{:?}", length);
}
```

```text
Ada
Some("Ada")
Some(3)
```

## take ve replace

`Option` değişebilir alanlarda çok kullanılır: `.take()` değeri alır ve yerine `None` bırakır.

```rust
fn main() {
    let mut slot = Some(3);
    let taken = slot.take();
    println!("{:?} {:?}", taken, slot);
    let old = slot.replace(9);
    println!("{:?} {:?}", old, slot);
}
```

```text
Some(3) None
None Some(9)
```

Bu, bağlı liste gibi yapılarda çok işimize yarayacak.

## Sıfır maliyet

`Option<&T>` ve `Option<Box<T>>` gibi türler, işaretçi kadar yer tutar: Derleyici `None`'u boş adres olarak kodlar. Yani `null`'un bedeline sahip ama tehlikesine değil:

```rust
use std::mem::size_of;

fn main() {
    println!("{}", size_of::<&i32>());
    println!("{}", size_of::<Option<&i32>>());
    println!("{}", size_of::<i32>());
    println!("{}", size_of::<Option<i32>>());
}
```

```text
8
8
4
8
```
