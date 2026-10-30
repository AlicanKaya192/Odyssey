# Vec and HashMap

An array's size was fixed. In real programs you usually do not know in advance how many elements will come. **Collections** live on the heap and can grow and shrink. The two most used are `Vec` and `HashMap`.

## Vec: a growing list

```rust
fn main() {
    let mut list: Vec<i32> = Vec::new();
    list.push(10);
    list.push(20);
    println!("{:?}", list);
    let ready = vec![1, 2, 3];
    println!("{}", ready.len());
    println!("{:?}", list.pop());
    println!("{:?}", list);
}
```

```text
[10, 20]
3
Some(20)
[10]
```

`Vec<i32>` means "a list of `i32`". The `vec![...]` macro creates one with ready values. `push` adds to the end, and `pop` removes from the end and returns an `Option`, since the list may be empty.

## Reaching an element

There are two ways, and the difference matters:

```rust
fn main() {
    let v = vec![10, 20, 30];
    println!("{}", v[0]);
    println!("{:?}", v.get(0));
    println!("{:?}", v.get(9));
}
```

```text
10
Some(10)
None
```

| Written | Out of bounds | When |
|---|---|---|
| `v[9]` | **Panic** | If you are sure it is in bounds |
| `v.get(9)` | `None` | If it may be absent |

## Walking

The three forms we saw in the previous section find their real meaning here:

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    for n in &v {
        print!("{n} ");
    }
    println!();
    for n in &mut v {
        *n += 10;
    }
    println!("{:?}", v);
    for n in v {
        print!("{n} ");
    }
    println!();
}
```

```text
1 2 3
[11, 12, 13]
11 12 13
```

| Written | Type of `n` | `v` afterwards |
|---|---|---|
| `for n in &v` | `&T` | Usable |
| `for n in &mut v` | `&mut T` | Usable, changed |
| `for n in v` | `T` | **Moved** |

## How does a Vec grow?

A `Vec`, like a `String`, holds three parts: address, length and capacity. When capacity fills, a larger room is taken and all elements move there. Let us measure:

```rust
fn main() {
    let mut v: Vec<i32> = Vec::new();
    let mut last = v.capacity();
    let mut moves = 0;
    for n in 0..1000 {
        v.push(n);
        if v.capacity() != last {
            last = v.capacity();
            moves += 1;
            print!("{last} ");
        }
    }
    println!();
    println!("{moves} moves");
}
```

```text
4 8 16 32 64 128 256 512 1024
9 moves
```

Capacity grows by doubling, so over 1000 `push` calls only a few moves happen. If you know the size in advance, `Vec::with_capacity(n)` prevents these moves as well.

This is the real reason behind the `E0502` example of an earlier section: `push` may move the memory.

## Common methods

```rust
fn main() {
    let mut v = vec![3, 1, 2, 3];
    println!("{}", v.contains(&2));
    v.sort();
    println!("{:?}", v);
    v.dedup();
    println!("{:?}", v);
    v.insert(0, 9);
    println!("{:?}", v);
    v.remove(1);
    println!("{:?}", v);
    v.retain(|n| *n != 2);
    println!("{:?}", v);
    println!("{:?} {:?}", v.first(), v.last());
}
```

```text
true
[1, 2, 3, 3]
[1, 2, 3]
[9, 1, 2, 3]
[9, 2, 3]
[9, 3]
Some(9) Some(3)
```

All of a slice's methods work on a `Vec` too (`len`, `contains`, `sort`, `iter`, `first`...), because `&Vec<T>` turns into `&[T]` by itself.

## HashMap: from key to value

A `HashMap` holds values under a **key**: from user name to age, from word to its count. A key is used instead of a position.

```rust
use std::collections::HashMap;

fn main() {
    let mut ages: HashMap<String, u32> = HashMap::new();
    ages.insert(String::from("Ada"), 36);
    ages.insert(String::from("Linus"), 55);
    ages.insert(String::from("Ada"), 37);
    println!("{:?}", ages.get("Ada"));
    println!("{:?}", ages.get("Grace"));
    println!("{}", ages.len());
    println!("{}", ages.contains_key("Linus"));
}
```

```text
Some(37)
None
2
true
```

`HashMap` does not come automatically; you need `use std::collections::HashMap;`. `insert` adds (overwriting if the key exists), and `get` returns an `Option<&V>`.

## No order

A `HashMap` **keeps no particular order.** What is more, the order may change on each run, because Rust uses a random seed against attacks. If you need order, use `BTreeMap` or sort the keys:

```rust
use std::collections::{BTreeMap, HashMap};

fn main() {
    let mut map = HashMap::new();
    map.insert("b", 2);
    map.insert("c", 3);
    map.insert("a", 1);
    let mut keys: Vec<_> = map.keys().collect();
    keys.sort();
    println!("{:?}", keys);

    let mut sorted = BTreeMap::new();
    sorted.insert("b", 2);
    sorted.insert("a", 1);
    println!("{:?}", sorted);
}
```

```text
["a", "b", "c"]
{"a": 1, "b": 2}
```

In this section's exercises, if you print `HashMap` output, sort it first or the output will be random.

## Ownership and HashMap

`insert` takes ownership of the key and the value:

```rust
use std::collections::HashMap;

fn main() {
    let key = String::from("Ada");
    let mut ages = HashMap::new();
    ages.insert(key, 36);
    println!("{key}");
}
```

```text
error[E0382]: borrow of moved value: `key`
 --> main.rs:7:16
  |
4 |     let key = String::from("Ada");
  |         --- move occurs because `key` has type `String`, which does not implement
  the `Copy` trait
5 |     let mut ages = HashMap::new();
6 |     ages.insert(key, 36);
  |                 --- value moved here
7 |     println!("{key}");
  |                ^^^ value borrowed here after move
  |
help: consider cloning the value if the performance cost is acceptable
  |
6 |     ages.insert(key.clone(), 36);
  |                    ++++++++
```

## entry: add if absent, update if present

The most common job is counting. `entry` is exactly for this:

```rust
use std::collections::BTreeMap;

fn main() {
    let text = "the cat and the dog and the bird";
    let mut counts = BTreeMap::new();
    for word in text.split_whitespace() {
        let count = counts.entry(word).or_insert(0);
        *count += 1;
    }
    println!("{:?}", counts);
}
```

```text
{"and": 2, "bird": 1, "cat": 1, "dog": 1, "the": 3}
```

`.entry(word)` gives the key's place. `.or_insert(0)` puts 0 if absent and gives a `&mut` to the value. `*count += 1` then increases it. These three parts are the pattern you will see most in Rust.

We used the word as a `&str` key: no copy is needed while `text` lives.

## Other collections

| Type | For |
|---|---|
| `Vec<T>` | An ordered list; the default choice |
| `VecDeque<T>` | Fast adding and removing at both ends (a queue) |
| `HashMap<K, V>` | From key to value |
| `BTreeMap<K, V>` | A map sorted by key |
| `HashSet<T>` | A set with no repeats |
| `BTreeSet<T>` | A sorted set with no repeats |

```rust
use std::collections::HashSet;

fn main() {
    let words = ["a", "b", "a", "c", "b"];
    let mut seen = HashSet::new();
    for word in words {
        if !seen.insert(word) {
            println!("again: {word}");
        }
    }
    println!("{}", seen.len());
}
```

```text
again: a
again: b
3
```

## Summary

- `Vec<T>` is a growing list: `push`, `pop`; `v[i]` may panic, `v.get(i)` gives `Option`.
- `for x in &v` borrows, `for x in v` consumes.
- Capacity grows by doubling; `push` may move memory.
- `HashMap` keeps no order; sort before printing or use `BTreeMap`.
- `insert` takes ownership. `entry(k).or_insert(v)` is the counting pattern.
