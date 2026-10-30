## A counter maker

Each closure carries its own state:

```rust
fn counter(start: u32) -> impl FnMut() -> u32 {
    let mut count = start;
    move || {
        count += 1;
        count
    }
}

fn main() {
    let mut a = counter(0);
    let mut b = counter(100);
    println!("{} {} {}", a(), a(), b());
}
```

```text
1 2 101
```

An `FnMut` is returned, and `count` lives inside the closure. The two counters are independent. The caller must define the variable `mut`.

## A callback

To give the caller a word in the middle of a job:

```rust
fn process(items: &[i32], mut report: impl FnMut(i32)) -> i32 {
    let mut total = 0;
    for item in items {
        total += item;
        report(total);
    }
    total
}

fn main() {
    let mut seen = Vec::new();
    let total = process(&[1, 2, 3], |t| seen.push(t));
    println!("{total} {:?}", seen);
}
```

```text
6 [1, 3, 6]
```

## Composition

A function joining two functions:

```rust
fn compose<A, B, C>(f: impl Fn(A) -> B, g: impl Fn(B) -> C) -> impl Fn(A) -> C {
    move |x| g(f(x))
}

fn main() {
    let len_doubled = compose(|s: &str| s.len(), |n| n * 2);
    println!("{}", len_doubled("rust"));
}
```

```text
8
```

## Small habits

| Bad | Good |
|---|---|
| <code>&#124;x&#124; foo(x)</code> | `foo` |
| <code>&#124;x&#124; x.len()</code> | `str::len` (if the type is known) |
| `.clone()` so it can pass into a closure | Try a borrow first |
| A closure with a long body | Write a named function |

If a closure goes over five lines it should be a function: the name tells what it does.
