## Which one to choose?

| Situation | Use | Example |
|---|---|---|
| The value never changes | `let` | `let name = "Ada";` |
| The same thing is updated | `let mut` | A total in a loop |
| The value turns into another form | Shadowing | From text to number |
| Constant throughout the program | `const` | `const MAX_USERS: u32 = 100;` |

## Common mistakes

**Forgetting `mut`.** Error code `E0384`. The message gives the fix on the `help:` line.

**A needless `mut`.** The program runs but you get a warning. Clearing warnings is a good habit.

```rust
fn main() {
    let mut name = "Ada";
    println!("{name}");
}
```

```text
Ada
```

You cannot see the warning text above because the program ran successfully and warnings appear while compiling. In
your own project, building it prints `variable does not need to be mutable`.

**Using a variable with no value.** You may write `let x;`, but you cannot read it before giving it a value:

```rust
fn main() {
    let x: i32;
    println!("{x}");
}
```

```text
error[E0381]: used binding `x` isn't initialized
 --> main.rs:3:16
  |
2 |     let x: i32;
  |         - binding declared here but left uninitialized
3 |     println!("{x}");
  |                ^ `x` used here but it isn't initialized
  |
help: consider assigning a value
  |
2 |     let x: i32 = 42;
  |                ++++
```

Rust never lets you read "some random value". This removes a whole class of errors that is very common in C.

## The shadowing trap

A `let` inside a block does not change the outer one; it only covers it:

```rust
fn main() {
    let total = 1;
    {
        let total = total + 10;
        println!("inside: {total}");
    }
    println!("outside: {total}");
}
```

```text
inside: 11
outside: 1
```

If you really want to change the outer value, assign without `let` (`total = total + 1;`), and the outer one must be `mut`.
