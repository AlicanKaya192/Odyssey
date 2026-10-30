# Threads and Channels

A **thread** is a separate branch of execution moving forward at the same time inside the same program. It is used to use several cores or to do something else while a job waits.

Writing concurrent programs is hard in most languages: a **data race**, which arises when two branches touch the same data, shows only sometimes, and only on the customer's machine at that. Rust's promise is bold: **a data race does not compile.**

## The first thread

`thread::spawn` takes a closure and runs it on a new branch:

```rust
use std::thread;

fn main() {
    let handle = thread::spawn(|| {
        println!("from the branch");
        21 * 2
    });
    let result = handle.join().unwrap();
    println!("result {result}");
}
```

```text
from the branch
result 42
```

`spawn` returns a **handle** (JoinHandle). `join` waits for the branch to end and gives its result. Since each branch moves at its own speed, the order between them may change on each run, so `join` is called first here.

If `join` is not called, the program ends when `main` ends and the branch is cut off.

## A result and an error

`join` returns a `Result`: `Err` if the branch panicked. A branch's panic does not bring down the program:

```rust
use std::thread;

fn main() {
    let handle = thread::spawn(|| {
        if 1 + 1 == 2 {
            panic!("branch failed");
        }
        5
    });
    let result = handle.join();
    println!("is error: {}", result.is_err());
    println!("main goes on");
}
```

```text
is error: true
main goes on

thread '<unnamed>' panicked at main.rs:6:13:
branch failed
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

## move: giving ownership to the branch

A branch may outlive the function that started it. So the compiler does not allow borrowing:

```rust
use std::thread;

fn main() {
    let list = vec![1, 2, 3];
    let handle = thread::spawn(|| {
        println!("{:?}", list);
    });
    handle.join().unwrap();
}
```

```text
error[E0373]: closure may outlive the current function, but it borrows `list`, which is
owned by the current function
 --> main.rs:5:32
  |
5 |     let handle = thread::spawn(|| {
  |                                ^^ may outlive borrowed value `list`
6 |         println!("{:?}", list);
  |                          ---- `list` is borrowed here
  |
note: function requires argument type to outlive `'static`
 --> main.rs:5:18
  |
5 |       let handle = thread::spawn(|| {
  |  __________________^
6 | |         println!("{:?}", list);
7 | |     });
  | |______^
help: to force the closure to take ownership of `list` (and any other referenced
variables), use the `move` keyword
  |
5 |     let handle = thread::spawn(move || {
  |                                ++++
```

With `move`, ownership passes to the branch:

```rust
use std::thread;

fn main() {
    let list = vec![1, 2, 3];
    let handle = thread::spawn(move || {
        let total: i32 = list.iter().sum();
        total
    });
    println!("{}", handle.join().unwrap());
}
```

```text
6
```

`list` is now the branch's. If `main` tries to use it, it gets `E0382`. To take a result back, return it from the closure: `join` gives it.

## Several branches

```rust
use std::thread;

fn main() {
    let mut handles = Vec::new();
    for n in 0..4 {
        handles.push(thread::spawn(move || n * n));
    }
    let mut results = Vec::new();
    for h in handles {
        results.push(h.join().unwrap());
    }
    println!("{:?}", results);
}
```

```text
[0, 1, 4, 9]
```

Gathering the handles and joining in order gives the results in the starting order, whichever branch finished first.

## Scoped threads

Branches inside `thread::scope` end before the scope ends. So they **can borrow** a local variable without `move`:

```rust
use std::thread;

fn main() {
    let list = vec![1, 2, 3, 4];
    let (left, right) = list.split_at(2);
    let (a, b) = thread::scope(|s| {
        let x = s.spawn(|| left.iter().sum::<i32>());
        let y = s.spawn(|| right.iter().sum::<i32>());
        (x.join().unwrap(), y.join().unwrap())
    });
    println!("{a} {b}");
    println!("{:?}", list);
}
```

```text
3 7
[1, 2, 3, 4]
```

This is the plainest way for most parallel computations.

## Channels: talking by messages

Sending data rather than sharing it. `mpsc` (multiple producer, single consumer):

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    thread::spawn(move || {
        for n in 1..=3 {
            tx.send(n * 10).unwrap();
        }
    });
    println!("{}", rx.recv().unwrap());
    for value in rx {
        println!("{value}");
    }
}
```

```text
10
20
30
```

| Part | Meaning |
|---|---|
| `tx` | The transmitter, can be `clone`d |
| `rx` | The receiver, a single one |
| `tx.send(v)` | Sends; ownership passes |
| `rx.recv()` | Waits until a message comes |
| `for x in rx` | Until all transmitters close |

Ownership of a sent value passes. Using it after sending does not compile:

```rust
use std::sync::mpsc;

fn main() {
    let (tx, rx) = mpsc::channel();
    let text = String::from("hi");
    tx.send(text).unwrap();
    println!("{text}");
    println!("{}", rx.recv().unwrap());
}
```

```text
error[E0382]: borrow of moved value: `text`
 --> main.rs:7:16
  |
5 |     let text = String::from("hi");
  |         ---- move occurs because `text` has type `String`, which does not implement
  the `Copy` trait
6 |     tx.send(text).unwrap();
  |             ---- value moved here
7 |     println!("{text}");
  |                ^^^^ value borrowed here after move
  |
help: consider cloning the value if the performance cost is acceptable
  |
6 |     tx.send(text.clone()).unwrap();
  |                 ++++++++
```

This is a small example of a data race not compiling: two branches cannot reach the same data at once.

## Several transmitters

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    for id in 0..3 {
        let tx = tx.clone();
        thread::spawn(move || {
            tx.send(id * 100).unwrap();
        });
    }
    drop(tx);
    let mut got: Vec<i32> = rx.iter().collect();
    got.sort();
    println!("{:?}", got);
}
```

```text
[0, 100, 200]
```

**Careful:** if you forget to `drop` the original `tx`, the `for` never ends, because a transmitter is still open.

The order the results come in is unknown; that is why we sort.

## Send and Sync

The compiler checks this with two marker traits:

| Trait | Meaning |
|---|---|
| `Send` | Can be **moved** to another branch |
| `Sync` | Can be **borrowed** from other branches |

Most types provide both automatically. `Rc` does not:

```rust
use std::rc::Rc;
use std::thread;

fn main() {
    let shared = Rc::new(5);
    let handle = thread::spawn(move || {
        println!("{shared}");
    });
    handle.join().unwrap();
}
```

```text
error[E0277]: `Rc<i32>` cannot be sent between threads safely
 --> main.rs:6:32
  |
6 |       let handle = thread::spawn(move || {
  |                    ------------- ^------
  |                    |             |
  |  __________________|_____________within this `{closure@main.rs:6:32: 6:39}`
  | |                  |
  | |                  required by a bound introduced by this call
7 | |         println!("{shared}");
8 | |     });
  | |_____^ `Rc<i32>` cannot be sent between threads safely
  |
  = help: within `{closure@main.rs:6:32: 6:39}`, the trait `Send` is not implemented for
    `Rc<i32>`
note: required because it's used within this closure
 --> main.rs:6:32
  |
6 |     let handle = thread::spawn(move || {
  |                                ^^^^^^^
note: required by a bound in `spawn`
```

The error looks long, but its core says "`Rc` is not `Send`". That is the next section's topic.

## Summary

- `thread::spawn(closure)` opens a branch, and `join` waits and gives the result. The order is unknown.
- A panic brings down only that branch; `join` gives `Err`.
- `move` gives ownership. `thread::scope` allows borrowing.
- `mpsc::channel`: `send` moves ownership and `recv` waits. The `for` ends when all `tx`s close.
- `Send` and `Sync` stop data races at compile time.
