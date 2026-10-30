## Bütün desen yazımları

| Desen | Örnek | Tutar |
|---|---|---|
| Sabit | `5`, `'a'`, `"hi"` | Tam bu değer |
| Değişken | `x` | Her şeyi, `x`'e bağlar |
| Joker | `_` | Her şeyi, bağlamaz |
| Veya | <code>1 &#124; 2</code> | Biri |
| Aralık | `1..=9`, `'a'..='z'` | Aralıktaki |
| Demet | `(a, 0)` | Şekle uyan |
| Struct | `Point { x, .. }` | Alanları açar |
| Enum | `Some(x)` | Seçeneği açar |
| Dizi, dilim | `[first, .., last]` | Şekle uyan |
| Referans | `&x` | Referansı çözer |
| Bağlama | `n @ 1..=9` | Hem sınar hem bağlar |

## Örnekler

```rust
fn describe(values: &[i32]) -> String {
    match values {
        [] => String::from("empty"),
        [one] => format!("one {one}"),
        [first, .., last] => format!("{first} to {last}"),
    }
}

fn total(values: &[i32]) -> i32 {
    match values {
        [] => 0,
        [first, rest @ ..] => first + total(rest),
    }
}

fn main() {
    println!("{}", describe(&[]));
    println!("{}", describe(&[7]));
    println!("{}", describe(&[1, 2, 3]));
    println!("{}", total(&[1, 2, 3]));
}
```

```text
empty
one 7
1 to 3
6
```

`[first, rest @ ..]` listeyi başına ve kalanına ayırır; özyinelemeli işlemlerde çok güzel durur.

## @ bağlaması

```rust
fn main() {
    let age = 15;
    match age {
        child @ 0..=12 => println!("child {child}"),
        teen @ 13..=19 => println!("teen {teen}"),
        adult => println!("adult {adult}"),
    }
}
```

```text
teen 15
```

## Desenler yalnızca match'te değil

| Yer | Örnek |
|---|---|
| `let` | `let (a, b) = pair;` |
| Fonksiyon parametresi | `fn f((a, b): (i32, i32))` |
| `for` | `for (i, x) in list.iter().enumerate()` |
| `if let`, `while let` | `if let Some(x) = y` |

`let` ve parametrelerde desen **her zaman tutmalıdır** (`let Some(x) = y;` kabul edilmez, `let else` gerekir).
