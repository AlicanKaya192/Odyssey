## When derive is not enough

Derived equality looks at all fields. If you want to look only at the identity, you write it by hand:

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

**Careful:** `Hash` must also be written by hand and look at the same fields. If `a == b` then `hash(a) == hash(b)` must hold, or a `HashMap` breaks.

## Writing Ord by hand

`std::cmp::Ordering` is one of three values: `Less`, `Equal`, `Greater`.

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

`.then_with(...)` moves to the next field on a tie. `.reverse()` flips the order.

## Do not give needless abilities

| Question | Decision |
|---|---|
| Small and cheap to copy? | Consider `Copy` |
| Will it be printed? | Always `Debug` |
| Will it be compared? | `PartialEq` |
| Will it be a key? | `Eq`, `Hash` |

Removing `Copy` later breaks the code using it, so add it with care.
