# Your Own Iterator

In the previous section we used ready iterators. Now we write `Iterator` for our own type. The reward is large: **writing a single `next`** brings `map`, `filter`, `sum`, `take` and dozens of methods for free.

## The smallest example

```rust
struct Counter {
    count: u32,
}

impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<u32> {
        if self.count >= 3 {
            return None;
        }
        self.count += 1;
        Some(self.count)
    }
}

fn main() {
    let mut c = Counter { count: 0 };
    println!("{:?}", c.next());
    println!("{:?}", c.next());
    println!("{:?}", c.next());
    println!("{:?}", c.next());
}
```

```text
Some(1)
Some(2)
Some(3)
None
```

The parts:

| Part | Meaning |
|---|---|
| `type Item = u32;` | Which type of elements come out (an associated type) |
| `fn next(&mut self)` | Give the next, move the state on |
| `None` | Finished |

The state is held inside the struct: the iterator itself remembers "where it left off".

## Free methods

We wrote only `next`, but:

```rust
struct Counter {
    count: u32,
}

impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<u32> {
        if self.count >= 3 {
            return None;
        }
        self.count += 1;
        Some(self.count)
    }
}

fn main() {
    let total: u32 = Counter { count: 0 }.sum();
    let list: Vec<u32> = Counter { count: 0 }.map(|x| x * 10).collect();
    let odd = Counter { count: 0 }.filter(|x| x % 2 == 1).count();
    println!("{total} {:?} {odd}", list);
    for n in (Counter { count: 1 }) {
        print!("{n} ");
    }
    println!();
}
```

```text
6 [10, 20, 30] 2
2 3
```

The default methods of the `Iterator` trait call `next`. `for` uses the same way.

## An endless iterator

`next` may never return `None`. Thanks to laziness that is no problem; we cut with `take`:

```rust
struct Fibonacci {
    a: u64,
    b: u64,
}

impl Iterator for Fibonacci {
    type Item = u64;

    fn next(&mut self) -> Option<u64> {
        let out = self.a;
        self.a = self.b;
        self.b += out;
        Some(out)
    }
}

fn main() {
    let first: Vec<u64> = Fibonacci { a: 0, b: 1 }.take(8).collect();
    println!("{:?}", first);
    let big = Fibonacci { a: 0, b: 1 }.find(|n| *n > 100);
    println!("{:?}", big);
}
```

```text
[0, 1, 1, 2, 3, 5, 8, 13]
Some(144)
```

If you call `collect` or `sum` without `take`, the program runs forever, because a consumer waits for the end.

## A lending iterator

An iterator giving references to a collection's elements cannot outlive the collection. A lifetime mark is really needed here:

```rust
struct Pairs<'a, T> {
    items: &'a [T],
    position: usize,
}

impl<'a, T> Iterator for Pairs<'a, T> {
    type Item = (&'a T, &'a T);

    fn next(&mut self) -> Option<Self::Item> {
        if self.position + 1 >= self.items.len() {
            return None;
        }
        let pair = (&self.items[self.position], &self.items[self.position + 1]);
        self.position += 1;
        Some(pair)
    }
}

fn main() {
    let list = [1, 2, 3];
    let mut it = Pairs { items: &list, position: 0 };
    let a = it.next();
    let b = it.next();
    println!("{:?} {:?} {:?}", a, b, it.next());
}
```

```text
Some((1, 2)) Some((2, 3)) None
```

`type Item = &'a T`: the returned reference depends on the **slice**, not on `self`. So `next` can be called twice and two references held at once.

## into_iter: so it works with for

To be able to write `for x in object`, `IntoIterator` is needed. The standard pattern is offering three forms for a collection. The most common is `&Collection`:

```rust
struct Shelf {
    books: Vec<String>,
}

impl<'a> IntoIterator for &'a Shelf {
    type Item = &'a String;
    type IntoIter = std::slice::Iter<'a, String>;

    fn into_iter(self) -> Self::IntoIter {
        self.books.iter()
    }
}

fn main() {
    let shelf = Shelf { books: vec![String::from("Dune"), String::from("Emma")] };
    for book in &shelf {
        println!("{book}");
    }
    println!("{}", shelf.books.len());
}
```

```text
Dune
Emma
2
```

`impl<'a> IntoIterator for &'a Shelf`: "`&Shelf` can turn into an iterator." So `for book in &shelf` works and `shelf` stays usable after.

## Producing with ready tools

You do not need to write a struct for every iterator:

```rust
use std::iter;

fn main() {
    let a: Vec<i32> = iter::repeat(7).take(2).collect();
    let mut n = 0;
    let b: Vec<i32> = iter::from_fn(|| {
        n += 1;
        if n < 4 { Some(n) } else { None }
    })
    .collect();
    let step = |x: &u32| if *x < 50 { Some(x * 3) } else { None };
    let c: Vec<u32> = iter::successors(Some(1), step).collect();
    let d: Vec<i32> = (0..10).step_by(4).collect();
    println!("{:?} {:?} {:?} {:?}", a, b, c, d);
}
```

```text
[7, 7] [1, 2, 3] [1, 3, 9, 27, 81] [0, 4, 8]
```

| Tool | What it produces |
|---|---|
| `std::iter::repeat(x)` | Endless `x` |
| `std::iter::once(x)` | A single element |
| `std::iter::from_fn(f)` | Until `f` says `None` |
| `std::iter::successors(a, f)` | Each element from the previous |
| `(0..n)`, `(0..).step_by(k)` | Ranges |

## Returning an iterator

To return a chain from a function you need not write its type name:

```rust
fn evens(list: &[i32]) -> impl Iterator<Item = i32> + '_ {
    list.iter().copied().filter(|x| x % 2 == 0)
}

fn main() {
    let list = [1, 2, 3, 4];
    let total: i32 = evens(&list).map(|x| x * 10).sum();
    println!("{total}");
}
```

```text
60
```

`impl Iterator<Item = i32> + '_`: `'_` means "tied to the input", because the returned iterator holds the slice by borrow.

## Summary

- `impl Iterator for S`, `type Item`, `fn next(&mut self) -> Option<Item>`.
- A single `next` earns all adapters and consumers.
- An endless iterator is safe thanks to laziness; cut with `take`.
- A lending iterator wants `struct S<'a>` and `type Item = &'a T`.
- `IntoIterator for &'a S` opens the form `for x in &s`.
- `from_fn`, `successors`, `repeat` produce iterators with no struct.
- `-> impl Iterator<Item = T>` returns a chain.
