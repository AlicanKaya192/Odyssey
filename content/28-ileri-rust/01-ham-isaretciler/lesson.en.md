# Raw Pointers

A reference makes four promises: it is valid, aligned, what it points to is alive, and if `&mut`, it is the only one. A raw pointer makes none. The price of this freedom is that you keep the promises.

## Creating

```rust
fn main() {
    let mut value = 5;

    let a = &raw const value;
    let b = &raw mut value;

    // SAFETY: both pointers show value, which is alive; no reference is in use.
    unsafe {
        *b += 1;
        println!("{}", *a);
    }
}
```

```text
6
```

`&raw const x` and `&raw mut x` give a pointer without producing an intermediate reference. This matters, because `&mut x as *mut _` first produces a `&mut`, and that `&mut`'s rules hold at that moment.

A null pointer can also be created, but it cannot be read. `is_null` checks; `as_ref` gives `None` if it is null:

```rust
use std::ptr;

fn main() {
    let value = 7;
    let good: *const i32 = &value;
    let bad: *const i32 = ptr::null();

    println!("{} {}", good.is_null(), bad.is_null());

    // SAFETY: as_ref checks null; good shows a live value.
    unsafe {
        println!("{:?}", good.as_ref());
        println!("{:?}", bad.as_ref());
    }
}
```

```text
false true
Some(7)
None
```

## Arithmetic

`p.add(i)` moves the pointer `i` **items**, not `i` bytes. The compiler knows the type's size:

```rust
fn sum(list: &[i32]) -> i32 {
    let p = list.as_ptr();
    let mut total = 0;
    for i in 0..list.len() {
        // SAFETY: i < len, so p.add(i) is inside the slice.
        total += unsafe { *p.add(i) };
    }
    total
}

fn main() {
    println!("{}", sum(&[1, 2, 3]));
    println!("{}", size_of::<i32>());
}
```

```text
6
4
```

One past the end of an array can be produced but not read. That is why the loop is safe with `i < len`.

## Reading and writing

Writing `*p` drops the old value. `ptr::write` does not touch the old one:

```rust
use std::ptr;

struct Noisy(&'static str);

impl Drop for Noisy {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn main() {
    let mut a = Noisy("a");
    a = Noisy("b");
    println!("after assignment");

    let mut c = Noisy("c");
    // SAFETY: c is alive and valid; its old value only leaks.
    unsafe { ptr::write(&mut c, Noisy("d")) };
    println!("after write");
}
```

```text
drop a
after assignment
after write
drop d
drop b
```

| Call | What it does | Its trap |
|---|---|---|
| `*p = v` | Drops the old, writes the new | The old value must be valid |
| `ptr::write(p, v)` | Writes without looking at the old | The old value leaks |
| `ptr::read(p)` | Copies bit by bit | There are two owners |

`ptr::read` is especially dangerous: reading a `String` gives the same memory two owners, and if both try to delete it, that is undefined behavior. Its right use is writing over the source at once. This is exactly what `mem::replace` does:

```rust
use std::ptr;

fn take_and_set(slot: &mut String, new: String) -> String {
    // SAFETY: the read value is returned, and the slot is overwritten
    // at once, so there are never two owners at the end.
    unsafe {
        let old = ptr::read(slot);
        ptr::write(slot, new);
        old
    }
}

fn main() {
    let mut name = String::from("old");
    let previous = take_and_set(&mut name, String::from("new"));
    println!("{previous} {name}");
}
```

```text
old new
```

## Box and raw pointers

`Box::into_raw` gives up ownership and gives a pointer. `Box::from_raw` takes ownership back. Structures like linked lists are built this way:

```rust
fn main() {
    let boxed = Box::new(String::from("hi"));
    let p: *mut String = Box::into_raw(boxed);

    // SAFETY: p came from Box::into_raw and nothing else uses it.
    unsafe {
        (*p).push_str(" there");
        let back = Box::from_raw(p);
        println!("{back}");
    }
}
```

```text
hi there
```

| Error | Result |
|---|---|
| `from_raw` is never called | Memory leaks |
| `from_raw` is called twice | Deleted twice, undefined behavior |
| A pointer not from a `Box` | Undefined behavior |

## NonNull

`NonNull<T>` is a `*mut T` promising it is not null. Its real advantage is size: `Option<NonNull<T>>` is the size of a pointer, because it uses the null value for `None`.

```rust
use std::ptr::NonNull;

fn main() {
    println!("{}", size_of::<*const u32>());
    println!("{}", size_of::<NonNull<u32>>());
    println!("{}", size_of::<Option<NonNull<u32>>>());
    println!("{}", size_of::<Option<&u32>>());
    println!("{}", size_of::<Option<u32>>());
}
```

```text
8
8
8
8
8
```

Look at the last line: while `Option<u32>` takes 8 bytes, `Option<&u32>` and `Option<NonNull<u32>>` are the size of the pointer itself. This **niche optimization** is something Rust promises, not a coincidence.

## Alignment

A `u32` lives at addresses that are multiples of four. Reading unaligned with `*p` is undefined behavior; when reading a number from a byte array, `read_unaligned` is needed:

```rust
fn main() {
    println!("{}", align_of::<u8>());
    println!("{}", align_of::<u32>());

    let bytes: [u8; 5] = [9, 1, 0, 0, 0];
    let p = bytes[1..].as_ptr() as *const u32;

    // SAFETY: four bytes are readable from p; read_unaligned allows any address.
    let number = unsafe { p.read_unaligned() };
    println!("{}", u32::from_le(number));
}
```

```text
1
4
1
```

## Summary

- `&raw const` and `&raw mut` produce no intermediate reference.
- `p.add(i)` counts items; reading out of bounds is undefined.
- `*p =` drops the old, `ptr::write` does not, `ptr::read` makes two owners.
- `Box::into_raw` and `from_raw` pair exactly once.
- `NonNull` is not null, and `Option<NonNull<T>>` takes no extra space.
