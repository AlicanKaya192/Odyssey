## Kalıp

```text
#[derive(Debug, Clone, PartialEq)]
struct Tur {
    alan: AlanTuru,
}

impl Tur {
    fn new(alan: AlanTuru) -> Self { Self { alan } }
    fn oku(&self) -> X { ... }
    fn degistir(&mut self) { ... }
    fn tuket(self) -> Y { ... }
}
```

## Sık derive'lar

| Ad | Sağladığı |
|---|---|
| `Debug` | `{:?}` ile yazdırma |
| `Clone` | `.clone()` |
| `Copy` | Atamada kopya (yalnızca bütün alanlar `Copy` ise) |
| `PartialEq` | `==` |
| `Default` | Varsayılan değer |

```rust
#[derive(Debug, Clone, Copy, PartialEq, Default)]
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let a = Point { x: 1, y: 2 };
    let b = a;
    println!("{:?} {:?}", a, b);
    println!("{}", a == b);
    println!("{:?}", Point::default());
}
```

```text
Point { x: 1, y: 2 } Point { x: 1, y: 2 }
true
Point { x: 0, y: 0 }
```

## Görünürlük

Şimdilik her şey aynı dosyada olduğu için fark etmez. Modüller konusunda (`14`) `pub` kelimesini göreceğiz: Alanlar varsayılan olarak modül dışına kapalıdır.

## Alan mı, metot mu?

| Soru | Cevap |
|---|---|
| Değer kaydediliyor mu? | Alan |
| Başka alanlardan hesaplanıyor mu? | Metot (`area`) |
| Kuralı korunmalı mı? | Özel alan + metot |

Alanla aynı adda metot yazılabilir: `rect.width` alan, `rect.width()` metot. Bu, salt okunur erişim sağlamanın yaygın yoludur.
