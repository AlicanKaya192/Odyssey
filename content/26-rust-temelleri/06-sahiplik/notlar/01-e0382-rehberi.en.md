When you see `E0382` there are four ways out. Think through them in order.

## 1. Is a move needed at all?

Often a function does not need to own the value; reading it is enough. The solution is borrowing (`&name`), the subject of the next section.

## 2. Can you change the order?

Move the value after its last use:

```rust
fn take(text: String) {
    println!("took {text}");
}

fn main() {
    let name = String::from("Ada");
    println!("{name}");
    take(name);
}
```

```text
Ada
took Ada
```

## 3. Do you really need two independent copies?

Write `.clone()`. Since its cost is visible there is no shame in it; but take a second look at a `.clone()` inside a loop.

## 4. Did it move in a loop?

A classic trap. A value moved on the first round is gone on the second:

```rust
fn take(text: String) {
    println!("{text}");
}

fn main() {
    let name = String::from("Ada");
    for _ in 0..2 {
        take(name);
    }
}
```

```text
error[E0382]: use of moved value: `name`
 --> main.rs:8:14
  |
6 |     let name = String::from("Ada");
  |         ---- move occurs because `name` has type `String`, which does not implement
  the `Copy` trait
7 |     for _ in 0..2 {
  |     ------------- inside of this loop
8 |         take(name);
  |              ^^^^ value moved here, in previous iteration of loop
  |
note: consider changing this parameter type in function `take` to borrow instead if
owning the value isn't necessary
 --> main.rs:1:15
  |
1 | fn take(text: String) {
  |    ----       ^^^^^^ this parameter takes ownership of the value
  |    |
  |    in this function
help: consider cloning the value if the performance cost is acceptable
  |
8 |         take(name.clone());
  |                  ++++++++
```

The message says `value moved here, in previous iteration of loop`. The fix is again `.clone()` or borrowing.

## Partial moves

If a part of a tuple or struct moves, that part cannot be used but other parts can:

```rust
fn main() {
    let pair = (String::from("key"), 7);
    let key = pair.0;
    println!("{key} {}", pair.1);
}
```

```text
key 7
```

`pair.0` moved, but `pair.1` is a number and `Copy`. `pair` as a whole can no longer be used; `pair.1` can.

## Reading the message

| Part of the message | Meaning |
|---|---|
| `move occurs because ... does not implement the Copy trait` | This type is moved, not copied |
| `value moved here` | The line where ownership went |
| `value used here after move` | The later use |
| `consider cloning` | A quick suggestion; it may not be the best |
