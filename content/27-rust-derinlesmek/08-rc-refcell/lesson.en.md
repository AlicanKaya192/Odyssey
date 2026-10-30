# Rc, RefCell and Sharing

The ownership rule says "a single owner". Usually that is right, but sometimes a value really has several owners: like two edges reaching the same node in a graph. The borrowing rule also says "a single writer at a time" and checks it at compile time. Sometimes the compiler cannot prove correct code. The two types of this section **safely bend** these two rules.

## The problem: two owners

```rust
fn main() {
    let a = String::from("shared");
    let list = vec![a];
    let other = vec![a];
    println!("{} {}", list.len(), other.len());
}
```

```text
error[E0382]: use of moved value: `a`
 --> main.rs:4:22
  |
2 |     let a = String::from("shared");
  |         - move occurs because `a` has type `String`, which does not implement the
  `Copy` trait
3 |     let list = vec![a];
  |                     - value moved here
4 |     let other = vec![a];
  |                      ^ value used here after move
  |
help: consider cloning the value if the performance cost is acceptable
  |
3 |     let list = vec![a.clone()];
  |                      ++++++++
```

`list` took `a`, and `other` cannot. The only fix would be borrowing, but lifetimes get complicated quickly.

## Rc: counted ownership

`Rc<T>` (reference counted) holds a value on the heap and **counts how many owners it has.** When the counter reaches zero, the value is deleted.

```rust
use std::rc::Rc;

fn main() {
    let a = Rc::new(String::from("shared"));
    let b = Rc::clone(&a);
    let c = Rc::clone(&a);
    println!("{a} {b} {c}");
    println!("{}", a.len());
}
```

```text
shared shared shared
6
```

<figure class="fig"><svg viewBox="0 0 640 226" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">stack</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">heap</text><g><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">a</text><text class="dim" x="110" y="71" font-size="12.5">Rc</text></g><g><rect class="box" x="20" y="102" width="230" height="44" rx="8"/><text class="ink" x="34" y="129" font-size="14" font-weight="600">b</text><text class="dim" x="110" y="129" font-size="12.5">Rc</text></g><g><rect class="box" x="20" y="160" width="230" height="44" rx="8"/><text class="ink" x="34" y="187" font-size="14" font-weight="600">c</text><text class="dim" x="110" y="187" font-size="12.5">Rc</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">sayaç 3, &quot;shared&quot;</text></g><path class="curve" d="M250 66 C320 66 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/><path class="curve" d="M250 124 C320 124 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/><path class="curve" d="M250 182 C320 182 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/></svg><figcaption>Three owners, one value. When the last goes, the value is deleted.</figcaption></figure>

`Rc::clone(&a)` does not copy the value; it only increases the counter. So the custom is to write `Rc::clone(&a)` rather than `a.clone()`: it reads as "this is not an expensive copy".

Let us watch the counter:

```rust
use std::rc::Rc;

fn main() {
    let a = Rc::new(5);
    println!("{}", Rc::strong_count(&a));
    let b = Rc::clone(&a);
    println!("{}", Rc::strong_count(&a));
    {
        let _c = Rc::clone(&a);
        println!("{}", Rc::strong_count(&a));
    }
    println!("{}", Rc::strong_count(&a));
    drop(b);
    println!("{}", Rc::strong_count(&a));
}
```

```text
1
2
3
2
1
```

## Rc only reads

Since `Rc` gives several owners, it does not let you change the contents. If it could, the borrowing rule would break:

```rust
use std::rc::Rc;

fn main() {
    let a = Rc::new(vec![1]);
    a.push(2);
    println!("{:?}", a);
}
```

```text
error[E0596]: cannot borrow data in an `Rc` as mutable
 --> main.rs:5:5
  |
5 |     a.push(2);
  |     ^ cannot borrow as mutable
  |
  = help: trait `DerefMut` is required to modify through a dereference, but it is not
    implemented for `Rc<Vec<i32>>`
```

To share and change, a second part is needed.

## RefCell: checking at run time

`RefCell<T>` provides **interior mutability**: it allows changing through `&self`. The rules are the same; only the check happens at run time rather than at compile time:

```rust
use std::cell::RefCell;

struct Notes {
    lines: RefCell<Vec<String>>,
}

impl Notes {
    fn add(&self, line: &str) {
        self.lines.borrow_mut().push(line.to_string());
    }
}

fn main() {
    let notes = Notes { lines: RefCell::new(Vec::new()) };
    notes.add("first");
    notes.add("second");
    println!("{:?}", notes.lines.borrow());
}
```

```text
["first", "second"]
```

| Method | What it gives | Equivalent |
|---|---|---|
| `.borrow()` | For reading | `&T` |
| `.borrow_mut()` | For changing | `&mut T` |

If you break the rule, not the compiler but the program stops:

```rust
use std::cell::RefCell;

fn main() {
    let cell = RefCell::new(1);
    let _first = cell.borrow_mut();
    let _second = cell.borrow_mut();
    println!("not reached");
}
```

```text
thread 'main' panicked at main.rs:6:24:
RefCell already borrowed
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

The compiler cannot catch this error; that is the price. `try_borrow_mut` returns a `Result` rather than panicking.

## Rc and RefCell together

The most common pair for several owners **and** changing: `Rc<RefCell<T>>`.

```rust
use std::cell::RefCell;
use std::rc::Rc;

fn main() {
    let list = Rc::new(RefCell::new(vec![1]));
    let a = Rc::clone(&list);
    let b = Rc::clone(&list);
    a.borrow_mut().push(2);
    b.borrow_mut().push(3);
    println!("{:?}", list.borrow());
    println!("{}", Rc::strong_count(&list));
}
```

```text
[1, 2, 3]
3
```

`a` and `b` see the same list. Both can add to it.

## A reference cycle

In one place `Rc` falls short of a garbage collector: if two values hold each other, the counter never reaches zero and **memory leaks.** Rust does not catch this at compile time, because a leak does not count as "unsafe":

```rust
use std::cell::RefCell;
use std::rc::Rc;

struct Node {
    name: &'static str,
    next: RefCell<Option<Rc<Node>>>,
}

impl Drop for Node {
    fn drop(&mut self) {
        println!("dropping {}", self.name);
    }
}

fn main() {
    let a = Rc::new(Node { name: "a", next: RefCell::new(None) });
    let b = Rc::new(Node { name: "b", next: RefCell::new(Some(Rc::clone(&a))) });
    *a.next.borrow_mut() = Some(Rc::clone(&b));
    println!("{} {}", Rc::strong_count(&a), Rc::strong_count(&b));
    println!("main ends");
}
```

```text
2 2
main ends
```

"dropping" was never written: the two nodes keep each other alive.

## Weak: a non-owning link

The fix: making one direction **weak**. `Weak<T>` does not increase the counter, and the value may have been deleted, so `.upgrade()` returns an `Option`:

```rust
use std::cell::RefCell;
use std::rc::{Rc, Weak};

struct Child {
    parent: RefCell<Weak<Parent>>,
}

struct Parent {
    name: String,
}

fn main() {
    let child = Child { parent: RefCell::new(Weak::new()) };
    println!("{}", child.parent.borrow().upgrade().is_none());
    {
        let parent = Rc::new(Parent { name: String::from("root") });
        *child.parent.borrow_mut() = Rc::downgrade(&parent);
        let up = child.parent.borrow().upgrade();
        println!("{}", up.map(|p| p.name.clone()).unwrap_or_default());
        println!("{}", Rc::strong_count(&parent));
    }
    println!("{}", child.parent.borrow().upgrade().is_none());
}
```

```text
true
root
1
true
```

The typical use is a tree: a parent owns its child (`Rc`), and a child only knows its parent (`Weak`).

## A single thread

`Rc` and `RefCell` **cannot be used** across threads: the counter is not atomic. The compiler stops it. Their counterparts are `Arc` and `Mutex` (section 11).

## Summary

- `Rc<T>` gives several owners: `Rc::clone` increases the counter, zero deletes, and the contents are read-only.
- `RefCell<T>` changes through `&self`: `borrow`, `borrow_mut`; a rule violation is a **panic**.
- `Rc<RefCell<T>>` to share and change.
- A cycle leaks; a `Weak` link is not counted, and `upgrade` gives an `Option`.
- Only on a single thread. Most code never needs these: try ownership and borrowing first.
