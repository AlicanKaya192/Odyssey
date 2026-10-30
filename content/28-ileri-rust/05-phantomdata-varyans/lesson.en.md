# PhantomData and Variance

This section answers two questions: how is a generic parameter that appears in no field held? And why can `&'static str` stand in for `&'a str`, while `&mut &'static str` cannot?

## An unused parameter

Rust wants to see every generic parameter of a struct in its fields:

```rust
struct Id<T> {
    value: u32,
}

fn main() {}
```

```text
error[E0392]: type parameter `T` is never used
 --> main.rs:1:11
  |
1 | struct Id<T> {
  |           ^ unused type parameter
  |
  = help: consider removing `T`, referring to it in a field, or using a marker such as
    `PhantomData`
  = help: if you intended `T` to be a const parameter, use `const T: /* Type */` instead
```

`PhantomData<T>` says "act as if there were a `T` of this type". It is zero bytes and absent at run time:

```rust
use std::marker::PhantomData;

struct User;
struct Order;

struct Id<T> {
    value: u32,
    _marker: PhantomData<fn() -> T>,
}

impl<T> Id<T> {
    fn new(value: u32) -> Self {
        Id { value, _marker: PhantomData }
    }
}

fn main() {
    let user: Id<User> = Id::new(7);
    let order: Id<Order> = Id::new(7);
    println!("{} {}", user.value, order.value);
    println!("{}", size_of::<Id<User>>());
    println!("{}", size_of::<PhantomData<String>>());
}
```

```text
7 7
4
0
```

`Id<User>` and `Id<Order>` are now different types; one does not stand in for the other. At run time both are plain `u32`:

```rust
use std::marker::PhantomData;

struct User;
struct Order;

struct Id<T> {
    value: u32,
    _marker: PhantomData<fn() -> T>,
}

fn load_user(id: Id<User>) -> u32 {
    id.value
}

fn main() {
    let order: Id<Order> = Id { value: 7, _marker: PhantomData };
    load_user(order);
}
```

```text
error[E0308]: mismatched types
  --> main.rs:17:15
   |
17 |     load_user(order);
   |     --------- ^^^^^ expected `Id<User>`, found `Id<Order>`
   |     |
   |     arguments to this function are incorrect
   |
   = note: expected struct `Id<User>`
              found struct `Id<Order>`
note: function defined here
  --> main.rs:11:4
   |
11 | fn load_user(id: Id<User>) -> u32 {
   |    ^^^^^^^^^ ------------
```

## Telling the compiler about ownership

The compiler does not see ownership behind a raw pointer. `PhantomData` says it:

| Written | What it says |
|---|---|
| `PhantomData<T>` | I own a `T` |
| `PhantomData<&'a T>` | I borrowed a `T` for `'a` |
| `PhantomData<&'a mut T>` | I borrowed it to change for `'a` |

The second is the most common. A slice iterator holds a raw pointer, but must act as if it borrowed the list:

```rust
use std::marker::PhantomData;

struct Iter<'a, T> {
    ptr: *const T,
    left: usize,
    _borrow: PhantomData<&'a T>,
}

fn iter_of<T>(list: &[T]) -> Iter<'_, T> {
    Iter { ptr: list.as_ptr(), left: list.len(), _borrow: PhantomData }
}

impl<'a, T> Iterator for Iter<'a, T> {
    type Item = &'a T;

    fn next(&mut self) -> Option<&'a T> {
        if self.left == 0 {
            return None;
        }
        // SAFETY: left items remain from ptr, and the list is borrowed for 'a.
        let item = unsafe { &*self.ptr };
        self.ptr = unsafe { self.ptr.add(1) };
        self.left -= 1;
        Some(item)
    }
}

fn main() {
    let list = vec![1, 2, 3];
    let total: i32 = iter_of(&list).sum();
    println!("{total}");
}
```

```text
6
```

Without `PhantomData`, `'a` would appear in no field and it would not compile. Now the list cannot be deleted while `Iter` lives.

## Variance: why does `&'static` shorten?

A longer-living reference can be given in place of a shorter one. This is called **subtyping**: `'static` is a subtype of `'a`.

```rust
fn longer<'a>(a: &'a str, b: &'a str) -> &'a str {
    if a.len() > b.len() { a } else { b }
}

fn main() {
    let forever: &'static str = "long text";
    let local = String::from("short");
    println!("{}", longer(forever, &local));
}
```

```text
long text
```

So when is this allowed? **Variance** says whether a wrapping type keeps this relation:

| Type | Variance in `T` | Meaning |
|---|---|---|
| `&'a T`, `Box<T>`, `Vec<T>` | Covariant | `T` may shorten |
| `&'a mut T`, `Cell<T>`, `RefCell<T>` | Invariant | `T` must stay exact |
| `fn(T)` | Contravariant | The reverse direction |

## Why is `&mut T` invariant?

Because if shortening were allowed, we could write a short-lived value into a long-lived slot:

```rust
fn set<'a>(slot: &mut &'a str, value: &'a str) {
    *slot = value;
}

fn main() {
    let mut s: &'static str = "start";
    {
        let local = String::from("short");
        set(&mut s, &local);
    }
    println!("{s}");
}
```

```text
error[E0597]: `local` does not live long enough
  --> main.rs:9:21
   |
 6 |     let mut s: &'static str = "start";
   |                ------------ type annotation requires that `local` is borrowed for
   `'static`
 7 |     {
 8 |         let local = String::from("short");
   |             ----- binding `local` declared here
 9 |         set(&mut s, &local);
   |                     ^^^^^^ borrowed value does not live long enough
10 |     }
   |     - `local` dropped here while still borrowed
```

`s` promises `'static`. If `set` saw it as `&'a str`, it would write the short-lived text inside. Invariance stops exactly this error. There is no such danger in `&T`, which only reads, so it is covariant.

## Variance in your own type

Fields decide variance. `*mut T` is invariant, and `*const T` and `NonNull<T>` are covariant. This is one more reason we chose `NonNull` in `MyVec` in the previous section:

```rust
use std::ptr::NonNull;

struct MyVec<T> {
    ptr: NonNull<T>,
    len: usize,
}

fn shorten<'a>(list: MyVec<&'static str>) -> MyVec<&'a str> {
    list
}
```

With `*mut T` the same function does not compile:

```rust
struct MyVec<T> {
    ptr: *mut T,
    len: usize,
}

fn shorten<'a>(list: MyVec<&'static str>) -> MyVec<&'a str> {
    list
}

fn main() {}
```

```text
error: lifetime may not live long enough
 --> main.rs:7:5
  |
6 | fn shorten<'a>(list: MyVec<&'static str>) -> MyVec<&'a str> {
  |            -- lifetime `'a` defined here
7 |     list
  |     ^^^^ returning this value requires that `'a` must outlive `'static`
  |
  = note: requirement occurs because of the type `MyVec<&str>`, which makes the generic
    argument `&str` invariant
  = note: the struct `MyVec<T>` is invariant over the parameter `T`
  = help: see <https://doc.rust-lang.org/nomicon/subtyping.html> for more information
    about variance
```

A `Vec<&'static str>` should stand in for `Vec<&'a str>`: it does in the standard `Vec`, and ours should too. `NonNull` gives covariance, and because we change the value inside, we keep it safe in `unsafe` with `&mut self`.

## Choosing PhantomData

| Wish | Written |
|---|---|
| I own `T` | `PhantomData<T>` |
| I borrowed for `'a` | `PhantomData<&'a T>` |
| Not an owner, only a label | `PhantomData<fn() -> T>` |
| Make it invariant | `PhantomData<Cell<T>>` |

The third is the best for labels like `Id<T>`: even if `T` is not `Send`, the label can pass between branches.

## Summary

- `PhantomData<T>` is zero bytes; it acts like a field for a generic parameter.
- The same bits, different types: `Id<User>` and `Id<Order>`.
- `&'a T` is covariant, `&'a mut T` invariant. Invariance prevents dangling references.
- `NonNull` is covariant, `*mut T` invariant.
- `PhantomData<&'a T>` ties a lifetime to a raw pointer.
