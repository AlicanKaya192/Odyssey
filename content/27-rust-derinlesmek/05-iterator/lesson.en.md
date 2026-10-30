# Iterators

Walking a list with `for` and gathering something is the most written code in Rust. An **iterator** splits this job into parts: filter, transform, gather. The code shortens, its intent reads clearly, and no speed is lost.

## What is an iterator?

Anything you can ask "give me the next element". The trait's core is one method:

```text
trait Iterator {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
}
```

`next` returns `Some(element)` while there are elements, and `None` at the end:

```rust
fn main() {
    let list = vec![10, 20];
    let mut it = list.iter();
    println!("{:?}", it.next());
    println!("{:?}", it.next());
    println!("{:?}", it.next());
}
```

```text
Some(10)
Some(20)
None
```

`let mut` is needed because `next` changes the iterator's position.

## Three ways of walking

Ownership decides here too:

```rust
fn main() {
    let mut v = vec![1, 2];
    for x in v.iter() {
        print!("{x} ");
    }
    for x in v.iter_mut() {
        *x *= 10;
    }
    println!("{:?}", v);
    for x in v.into_iter() {
        print!("{x} ");
    }
    println!();
}
```

```text
1 2 [10, 20]
10 20
```

| Method | Element type | The list afterwards |
|---|---|---|
| `.iter()` | `&T` | Stays |
| `.iter_mut()` | `&mut T` | Stays, may have changed |
| `.into_iter()` | `T` | Consumed |

The forms `for x in &v`, `for x in &mut v` and `for x in v` are short forms of these.

## Laziness

`map` and `filter` alone do **nothing.** They only set up "what to do". The work starts when someone asks for an element:

```rust
fn main() {
    let list = vec![1, 2];
    let _ignored = list.iter().map(|x| println!("first map {x}"));
    println!("nothing ran yet");
    let out: Vec<i32> = list
        .iter()
        .map(|x| {
            println!("second map {x}");
            x * 2
        })
        .collect();
    println!("{:?}", out);
}
```

```text
nothing ran yet
second map 1
second map 2
[2, 4]
```

The first `map` never ran: the output has lines only after `collect`. The compiler warns too: "iterator adapters are lazy". There are two kinds of methods:

| Kind | Example | What it returns |
|---|---|---|
| **Adapter** | `map`, `filter`, `take`, `rev` | A new iterator, lazy |
| **Consumer** | `collect`, `sum`, `count`, `max`, `for` | A result; starts the work |

One element passes the whole chain in one go. The whole list does not pass `map` first and then `filter`:

```rust
fn main() {
    let out: Vec<i32> = [1, 2, 3, 4]
        .iter()
        .map(|x| {
            println!("map {x}");
            x * 2
        })
        .filter(|x| {
            println!("filter {x}");
            *x > 2
        })
        .take(1)
        .collect();
    println!("{:?}", out);
}
```

```text
map 1
filter 2
map 2
filter 4
[4]
```

When `take(1)` was satisfied, the rest were never looked at. That is why an iterator chain does no needless work.

## The most common adapters

```rust
fn main() {
    let v = vec![1, 2, 3, 4];
    let doubled: Vec<i32> = v.iter().map(|x| x * 2).collect();
    let big: Vec<&i32> = v.iter().filter(|x| **x > 2).collect();
    let some: Vec<&i32> = v.iter().skip(1).take(2).collect();
    println!("{:?} {:?} {:?}", doubled, big, some);
    for (i, x) in v.iter().enumerate().rev().take(1) {
        println!("{i} {x}");
    }
    let pairs: Vec<(i32, char)> = vec![1, 2].into_iter().zip("ab".chars()).collect();
    println!("{:?}", pairs);
    let flat: Vec<char> = ["ab", "c"].iter().flat_map(|s| s.chars()).collect();
    println!("{:?}", flat);
}
```

```text
[2, 4, 6, 8] [3, 4] [2, 3]
3 4
[(1, 'a'), (2, 'b')]
['a', 'b', 'c']
```

| Method | Job |
|---|---|
| `map(f)` | Transform |
| `filter(f)` | Keep those passing (takes `&Item`) |
| `take(n)`, `skip(n)` | The first `n`, skip the first `n` |
| `enumerate()` | `(position, element)` |
| `zip(other)` | The two side by side |
| `rev()` | Reverse |
| `chain(other)` | One after the other |
| `flat_map(f)` | Flatten lists |

Why does `filter` want `**n`? `.iter()` gives `&i32`, and `filter` adds one more reference: `&&i32`. You usually open it with a pattern: `|&&n| n > 1`.

## The most common consumers

```rust
fn main() {
    let v = vec![3, 8, 5];
    println!("{}", v.iter().sum::<i32>());
    println!("{}", v.iter().count());
    println!("{:?} {:?}", v.iter().max(), v.iter().min());
    println!("{:?}", v.iter().find(|x| **x > 4));
    println!("{:?}", v.iter().position(|x| *x == 5));
    println!("{} {}", v.iter().any(|x| *x > 7), v.iter().all(|x| *x > 7));
}
```

```text
16
3
Some(8) Some(3)
Some(8)
Some(2)
true false
```

`find` gives the first match, `position` its position, and `any` and `all` a `bool`. `max` and `min` return `Option`, because the list may be empty.

## collect

`collect` gathers into the collection you want; you name the target type:

```rust
use std::collections::{HashMap, HashSet};

fn main() {
    let list: Vec<i32> = (1..4).collect();
    let text: String = "abc".chars().rev().collect();
    let unique: HashSet<i32> = [1, 1, 2].into_iter().collect();
    let map: HashMap<&str, i32> = [("a", 1)].into_iter().collect();
    println!("{:?} {text} {} {:?}", list, unique.len(), map.get("a"));
    let good: Result<Vec<i32>, _> = ["1", "2"].iter().map(|s| s.parse::<i32>()).collect();
    let bad: Result<Vec<i32>, _> = ["1", "x"].iter().map(|s| s.parse::<i32>()).collect();
    println!("{:?} {}", good, bad.is_err());
}
```

```text
[1, 2, 3] cba 2 Some(1)
Ok([1, 2]) true
```

`Result<Vec<_>, _>` is especially strong: if even one fails, the first error comes back.

## fold

The mother of all consumers. A starting value and the question "how do I join the new value":

```rust
fn main() {
    let v = [1, 2, 3];
    let total = v.iter().fold(0, |sum, x| sum + x);
    let text = v.iter().fold(String::new(), |acc, x| format!("{acc}{x}-"));
    println!("{total} {text}");
}
```

```text
6 1-2-3-
```

`sum` is really like `fold(0, |a, b| a + b)`. If a ready method exists use it; `fold` is for special gathering.

## Loop or iterator?

```rust
fn with_loop(v: &[i32]) -> i32 {
    let mut total = 0;
    for x in v {
        if x % 2 == 0 {
            total += x * x;
        }
    }
    total
}

fn with_iter(v: &[i32]) -> i32 {
    v.iter().filter(|x| **x % 2 == 0).map(|x| x * x).sum()
}

fn main() {
    let v = [1, 2, 3, 4];
    println!("{} {}", with_loop(&v), with_iter(&v));
}
```

```text
20 20
```

The two give the same result, and once compiled their speeds are the same. This is Rust's promise of a zero-cost abstraction: the high-level form runs as fast as a hand-written loop. Array bound checks often disappear too.

For transforming and gathering, an iterator reads better. For a complex early exit and updating several variables, `for` is clearer. Do not force it.

## Summary

- `next` gives `Some` or `None`. `iter`, `iter_mut`, `into_iter` choose ownership.
- Adapters are lazy and a consumer starts the work. Elements pass the chain one by one.
- `map`, `filter`, `take`, `enumerate`, `zip`, `rev`, `chain`, `flat_map`.
- `collect`, `sum`, `count`, `max`, `find`, `any`, `all`, `fold`.
- `collect` wants a target type, and `Result<Vec<_>, _>` stops at the first error.
- An iterator is as fast as a hand-written loop.
