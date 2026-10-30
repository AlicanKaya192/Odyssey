## derive yetmeyince

Türetilmiş eşitlik bütün alanlara bakar. Yalnızca kimliğe bakmak istiyorsan elle yazarsın:

```rust
#[derive(Debug)]
struct User {
    id: u32,
    name: String,
}

impl PartialEq for User {
    fn eq(&self, other: &User) -> bool {
        self.id == other.id
    }
}

fn main() {
    let a = User { id: 1, name: String::from("Ada") };
    let b = User { id: 1, name: String::from("Ada L.") };
    println!("{}", a == b);
    println!("{}", a.name == b.name);
}
```

```text
true
false
```

**Dikkat:** `Hash` da elle yazılmalı ve aynı alanlara bakmalı. `a == b` ise `hash(a) == hash(b)` olmak zorundadır, yoksa `HashMap` bozulur.

## Ord'u elle yazmak

`std::cmp::Ordering` üç değerden biridir: `Less`, `Equal`, `Greater`.

```rust
use std::cmp::Ordering;

#[derive(Debug, PartialEq, Eq)]
struct Player {
    score: u32,
    name: String,
}

impl Ord for Player {
    fn cmp(&self, other: &Player) -> Ordering {
        other.score.cmp(&self.score).then_with(|| self.name.cmp(&other.name))
    }
}

impl PartialOrd for Player {
    fn partial_cmp(&self, other: &Player) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn main() {
    let mut list = vec![
        Player { score: 5, name: String::from("b") },
        Player { score: 9, name: String::from("c") },
        Player { score: 5, name: String::from("a") },
    ];
    list.sort();
    for p in &list {
        println!("{} {}", p.score, p.name);
    }
}
```

```text
9 c
5 a
5 b
```

`.then_with(...)` eşitlik durumunda sonraki alana geçer. `.reverse()` sırayı çevirir.

## Gereksiz yetenek verme

| Soru | Karar |
|---|---|
| Küçük ve kopyası ucuz mu? | `Copy` düşün |
| Yazdırılacak mı? | Her zaman `Debug` |
| Karşılaştırılacak mı? | `PartialEq` |
| Anahtar olacak mı? | `Eq`, `Hash` |

`Copy`'yi sonradan kaldırmak onu kullanan kodu bozar, dikkatli ekle.
