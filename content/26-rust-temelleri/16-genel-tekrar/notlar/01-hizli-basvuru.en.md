## Forms

| Job | Written |
|---|---|
| Immutable, mutable | `let x = 1;`, `let mut x = 1;` |
| Constant | `const MAX: u32 = 10;` |
| Function | `fn add(a: i32, b: i32) -> i32 { a + b }` |
| Condition | `if a > 0 { .. } else { .. }` |
| Loops | `loop`, `while k`, `for x in 0..3` |
| Struct | `struct P { x: i32 }`, `impl P { fn f(&self) {} }` |
| Enum | `enum E { A, B(i32) }` |
| Pattern | `match v { E::A => .., E::B(n) => .. }` |
| Single pattern | `if let Some(x) = v { .. }` |
| List | `vec![1, 2]`, `v.push(3)`, `v.get(0)` |
| Map | `HashMap::new()`, `m.insert(k, v)`, `m.entry(k).or_insert(0)` |
| Text | `String::from("a")`, `&s[0..1]`, `s.len()` |
| Error | `Ok(v)`, `Err(e)`, `f()?` |
| Module | `mod a;`, `pub fn`, `use a::b;` |
| Test | `#[test]`, `assert_eq!(a, b)` |

## Ownership rules

1. Each value has an owner.
2. Only one owner at a time.
3. When the owner leaves scope, the value is deleted.

## Borrowing rules

1. At one time either many `&T` or a single `&mut T`.
2. A reference must always be valid.

## Common errors

| Code | Meaning | Usual fix |
|---|---|---|
| `E0382` | A moved value was used | Borrow or `clone` |
| `E0499` | Two `&mut` | End one of them |
| `E0502` | `&mut` while `&` exists | Narrow the scope |
| `E0505` | Moved while borrowed | Change the order |
| `E0384` | Assigned twice to a non-`mut` | Add `mut` |
| `E0596` | `&mut` from a non-`mut` | Add `mut` |
| `E0308` | Types do not match | Fix the type |
| `E0004` | `match` is missing an arm | Add the arm |
| `E0106` | A lifetime is missing | Return an owned value |
| `E0277` | A trait is missing | Read the error text |
| `E0603` | A private name | Add `pub` |

## Cargo

| Command | Job |
|---|---|
| `cargo new name` | A new project |
| `cargo run` | Build and run |
| `cargo check` | Check only |
| `cargo test` | Tests |
| `cargo build --release` | An optimized build |
| `cargo fmt`, `cargo clippy` | Formatting, suggestions |
