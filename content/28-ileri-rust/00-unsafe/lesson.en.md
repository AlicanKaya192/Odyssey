# What unsafe Means

The compiler accepts a program only if it can prove it. Some correct programs cannot be proved. That is why basic types like `Vec` and `Mutex` use `unsafe` inside. This module opens that layer.

`unsafe` does not mean "turn the rules off". It means **"I guarantee this part is correct, not the compiler"**.

## Five powers

An `unsafe` block allows only these five jobs:

| Power | Example |
|---|---|
| Reading or writing through a raw pointer | `*p` |
| Calling an `unsafe fn` | `v.get_unchecked(0)` |
| Reaching a `static mut` variable | `COUNT += 1` |
| Implementing an `unsafe trait` | `unsafe impl Send for T {}` |
| Reading a `union` field | `u.number` |

A raw pointer is written `*const T` or `*mut T`. **Creating** one is safe; **reading** what it points to is not:

```rust
fn main() {
    let value = 5;
    let p = &value as *const i32;

    // SAFETY: p comes from a reference to value, which is alive here.
    let read = unsafe { *p };
    println!("{read}");
}
```

```text
5
```

Without the block it does not compile:

```rust
fn main() {
    let value = 5;
    let p = &value as *const i32;
    let read = *p;
    println!("{read}");
}
```

```text
error[E0133]: dereference of raw pointer is unsafe and requires unsafe block
 --> main.rs:4:16
  |
4 |     let read = *p;
  |                ^^ dereference of raw pointer
  |
  = note: raw pointers may be null, dangling or unaligned; they can violate aliasing
    rules and cause data races: all of these are undefined behavior
```

## What does unsafe not turn off?

Type checks, ownership and borrow rules also hold inside `unsafe`:

```rust
fn main() {
    let mut n = 1;
    unsafe {
        let a = &mut n;
        let b = &mut n;
        *a += 1;
        *b += 1;
    }
    println!("{n}");
}
```

```text
warning: unnecessary `unsafe` block
 --> main.rs:3:5
  |
3 |     unsafe {
  |     ^^^^^^ unnecessary `unsafe` block
  |
  = note: `#[warn(unused_unsafe)]` (part of `#[warn(unused)]`) on by default

error[E0499]: cannot borrow `n` as mutable more than once at a time
 --> main.rs:5:17
  |
4 |         let a = &mut n;
  |                 ------ first mutable borrow occurs here
5 |         let b = &mut n;
  |                 ^^^^^^ second mutable borrow occurs here
6 |         *a += 1;
  |         ------- first borrow later used here
```

`unsafe` adds new powers; it does not remove existing checks. Using pointers steps outside the checks, because a raw pointer has no lifetime.

## Undefined behavior

If you break a rule inside `unsafe`, the result is not an **error** but **undefined behavior**: the language promises nothing about what the program does.

| Done | Why it is undefined |
|---|---|
| Reading null or freed memory | The pointer is not valid |
| Reaching out of bounds | It reads other data |
| Two `&mut` at the same time | The compiler optimizes assuming there is one |
| Writing `2` into a `bool` | The type can only be 0 and 1 |
| A data race | The result varies by branch |

The most dangerous part: **the program may appear to work.** A test passing today can fail tomorrow when the compiler version changes. So `unsafe` is not verified by trying, but **by reasoning**.

Three ways to do the same job:

```rust
fn main() {
    let list = [10, 20, 30];

    println!("{:?}", list.get(1));
    println!("{:?}", list.get(10));
    println!("{}", list[1]);

    // SAFETY: 1 is smaller than the length 3.
    let value = unsafe { *list.get_unchecked(1) };
    println!("{value}");
}
```

```text
Some(20)
None
20
20
```

| Written | Out of bounds |
|---|---|
| `list.get(10)` | `None` |
| `list[10]` | A panic |
| `list.get_unchecked(10)` | Undefined behavior |

We do not run the third out of bounds here: its result cannot be told. Its only advantage is skipping the bounds check, and in most programs the compiler removes that check anyway.

## A safe abstraction

This is `unsafe`'s real place: `unsafe` inside, a safe function outside. Let us split a slice into two `&mut` parts. It cannot be written in safe code:

```rust
fn split_pair(list: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
    let len = list.len();
    (&mut list[..mid], &mut list[mid..len])
}

fn main() {
    let mut list = [1, 2];
    split_pair(&mut list, 1);
}
```

```text
error[E0499]: cannot borrow `*list` as mutable more than once at a time
 --> main.rs:3:29
  |
1 | fn split_pair(list: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
  |                     - let's call the lifetime of this reference `'1`
2 |     let len = list.len();
3 |     (&mut list[..mid], &mut list[mid..len])
  |     ------------------------^^^^-----------
  |     |     |                 |
  |     |     |                 second mutable borrow occurs here
  |     |     first mutable borrow occurs here
  |     returning this value requires that `*list` is borrowed for `'1`
  |
  = help: use `.split_at_mut(position)` to obtain two mutable non-overlapping sub-slices
```

The compiler does not know the two parts do not overlap. We do:

```rust
use std::slice;

fn split_pair(list: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
    assert!(mid <= list.len());
    let len = list.len();
    let p = list.as_mut_ptr();

    // SAFETY: mid <= len was checked, so both parts are in bounds.
    // The parts do not overlap, so the two &mut do not alias.
    unsafe {
        (
            slice::from_raw_parts_mut(p, mid),
            slice::from_raw_parts_mut(p.add(mid), len - mid),
        )
    }
}

fn main() {
    let mut list = [1, 2, 3, 4];
    let (a, b) = split_pair(&mut list, 1);
    a[0] = 10;
    b[0] = 20;
    println!("{list:?}");
}
```

```text
[10, 20, 3, 4]
```

Look at three things:

1. **The condition is checked first.** Thanks to `assert!`, a bad `mid` is a panic, not undefined behavior.
2. **The `// SAFETY:` comment** writes why it is correct. This comment is like part of the code; if you cannot write it, the code is probably wrong.
3. **The function is not `unsafe`.** The caller cannot produce undefined behavior with any input. This is the measure of a good safe abstraction.

The standard library's `split_at_mut` is written exactly like this.

## unsafe fn

If a function cannot check a condition itself, it puts the condition on the caller. The function then becomes `unsafe fn`, and a `# Safety` heading goes in its documentation:

```rust
/// Returns the first item without checking.
///
/// # Safety
///
/// `list` must not be empty.
unsafe fn first_unchecked(list: &[i32]) -> i32 {
    // SAFETY: the caller guarantees the list is not empty.
    unsafe { *list.get_unchecked(0) }
}

fn first_or_zero(list: &[i32]) -> i32 {
    if list.is_empty() {
        return 0;
    }
    // SAFETY: the empty case returned just above.
    unsafe { first_unchecked(list) }
}

fn main() {
    println!("{}", first_or_zero(&[7, 8]));
    println!("{}", first_or_zero(&[]));
}
```

```text
7
0
```

In Rust 2024 an `unsafe fn` body does not count as `unsafe` by itself, so a block is written inside too. Without it the compiler warns:

```rust
/// # Safety
/// `list` must not be empty.
unsafe fn first_unchecked(list: &[i32]) -> i32 {
    *list.get_unchecked(0)
}

fn main() {
    // SAFETY: the list has an item.
    println!("{}", unsafe { first_unchecked(&[1]) });
}

```

```text
warning[E0133]: call to unsafe function `core::slice::<impl [T]>::get_unchecked` is
unsafe and requires unsafe block
 --> main.rs:4:6
  |
4 |     *list.get_unchecked(0)
  |      ^^^^^^^^^^^^^^^^^^^^^ call to unsafe function
  |
  = note: consult the function's documentation for information on how to avoid undefined
    behavior
note: an unsafe function restricts its caller, but its body is safe by default
 --> main.rs:3:1
  |
3 | unsafe fn first_unchecked(list: &[i32]) -> i32 {
  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  = note: for more information, see
    <https://doc.rust-lang.org/edition-guide/rust-2024/unsafe-op-in-unsafe-fn.html>
  = note: `#[warn(unsafe_op_in_unsafe_fn)]` (part of `#[warn(rust_2024_compatibility)]`)
    on by default


For more information about this error, try `rustc --explain E0133`.
```

So it stays visible which line in the body is dangerous.

## When?

| Case | Decision |
|---|---|
| There is a safe way | Do not write `unsafe` |
| For speed | Measure first; often there is no difference |
| You are writing a basic data structure | It may be needed; keep it small |
| You are calling a C library | Needed (the FFI section) |

The less `unsafe` a project has, the fewer places there are to check.

## Summary

- `unsafe`: five powers, and you guarantee instead of the compiler.
- Borrow rules also work inside `unsafe`.
- Breaking a rule gives undefined behavior: appearing to work is no proof.
- `unsafe` inside, a safe function outside; the `// SAFETY:` comment is a required habit.
- `unsafe fn` puts the condition on the caller, documented with `# Safety`.
