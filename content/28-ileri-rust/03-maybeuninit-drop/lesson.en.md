# MaybeUninit and ManuallyDrop

Rust does two things itself: it requires every value to be initialized before use, and it drops the value at scope end. When writing your own data structure, you sometimes must step into both. This section's two types are exactly for that.

## Uninitialized memory

Writing `let x: i32;` and reading it does not compile. This is a good rule, but the empty places in a `Vec`'s capacity are also uninitialized. A type is needed to hold them as "maybe initialized":

```rust
use std::mem::MaybeUninit;

fn main() {
    let mut slot = MaybeUninit::<i32>::uninit();
    slot.write(42);

    // SAFETY: the value was written on the line above.
    let value = unsafe { slot.assume_init() };
    println!("{value}");
}
```

```text
42
```

`MaybeUninit<T>` takes as much space as `T`, but does not promise its contents are valid:

| Call | What it does |
|---|---|
| `MaybeUninit::uninit()` | An empty place |
| `.write(v)` | Writes a value, without dropping the old |
| `.assume_init()` | Says "ready now", returns `T` |
| `.as_ptr()`, `.as_mut_ptr()` | A pointer |

`assume_init` is `unsafe`: reading unwritten memory is undefined behavior.

```rust
use std::mem::{ManuallyDrop, MaybeUninit};

fn main() {
    println!("{}", size_of::<String>());
    println!("{}", size_of::<MaybeUninit<String>>());
    println!("{}", size_of::<ManuallyDrop<String>>());
}
```

```text
24
24
24
```

The same size, no extra flag. **You** track which place is filled.

## Filling an array

Building an array with types that have no initial value is the most common use:

```rust
use std::mem::MaybeUninit;

fn make_names() -> [String; 3] {
    let mut slots: [MaybeUninit<String>; 3] = [const { MaybeUninit::uninit() }; 3];

    for (i, slot) in slots.iter_mut().enumerate() {
        slot.write(format!("item {i}"));
    }

    // SAFETY: the loop wrote every slot, and the two arrays have the same layout.
    unsafe { slots.map(|slot| slot.assume_init()) }
}

fn main() {
    println!("{:?}", make_names());
}
```

```text
["item 0", "item 1", "item 2"]
```

`String` has no zero value, and `[String::new(); 3]` does not compile either. Besides, `array::from_fn` usually does this job safely; we are here to understand `MaybeUninit`.

## The trap: values not dropped

When a `MaybeUninit<T>` drops, it does **not** drop its contents, because it does not know whether it is filled:

```rust
use std::mem::MaybeUninit;

struct Noisy;

impl Drop for Noisy {
    fn drop(&mut self) {
        println!("dropped");
    }
}

fn main() {
    {
        let mut slot = MaybeUninit::<Noisy>::uninit();
        slot.write(Noisy);
        println!("end of first block");
    }
    {
        let mut slot = MaybeUninit::<Noisy>::uninit();
        slot.write(Noisy);
        // SAFETY: the value was written on the line above.
        unsafe { slot.assume_init_drop() };
        println!("end of second block");
    }
}
```

```text
end of first block
dropped
end of second block
```

A value written with `write` leaks if not read by hand. The same at a failure: if a panic happens with the array half done, the filled ones do not drop. This is a leak, not undefined behavior.

## ManuallyDrop

`ManuallyDrop<T>` does the reverse: the value is filled, but it is **not dropped** at scope end. Dropping is up to you:

```rust
use std::mem::ManuallyDrop;

struct Noisy(&'static str);

impl Drop for Noisy {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn main() {
    let mut kept = ManuallyDrop::new(Noisy("kept"));
    let _forgotten = ManuallyDrop::new(Noisy("forgotten"));
    let _normal = Noisy("normal");

    println!("{}", kept.0);
    // SAFETY: kept is not used after this line.
    unsafe { ManuallyDrop::drop(&mut kept) };
    println!("end");
}
```

```text
kept
drop kept
end
drop normal
```

`mem::forget(x)` also prevents dropping; the difference is that `ManuallyDrop` allows reaching the value later.

Why is it needed? To drop a type's parts in a different order, or to move ownership elsewhere by hand. For example, our own `Vec` does not want the main value's `Drop` to run during `into_iter`.

## Half-done work and safety

A panic can happen while moving values by hand: what if your `T::clone` panics? This is the question of **panic safety**. The solution is keeping the state valid at every step:

```rust
use std::panic::{self, AssertUnwindSafe};

struct Guard<'a> {
    list: &'a mut Vec<i32>,
    original_len: usize,
}

impl Drop for Guard<'_> {
    fn drop(&mut self) {
        self.list.truncate(self.original_len);
    }
}

fn extend_all_or_nothing(list: &mut Vec<i32>, make: impl Fn(i32) -> i32) {
    let original_len = list.len();
    let guard = Guard { list, original_len };
    for n in 0..3 {
        let value = make(n);
        guard.list.push(value);
    }
    std::mem::forget(guard);
}

fn main() {
    panic::set_hook(Box::new(|_| {}));
    let mut list = vec![9];

    let _ = panic::catch_unwind(AssertUnwindSafe(|| {
        extend_all_or_nothing(&mut list, |n| if n == 2 { panic!("no") } else { n });
    }));
    println!("{list:?}");

    extend_all_or_nothing(&mut list, |n| n);
    println!("{list:?}");
}
```

```text
[9]
[9, 0, 1, 2]
```

A guard value is dropped in a panic too, and cleans up the half-done work. This pattern is everywhere in the standard library.

## Summary

- `MaybeUninit<T>`: the same size, no promise of validity, no dropping.
- `assume_init` only after writing.
- `ManuallyDrop<T>`: the value is valid, and dropping is yours.
- You track what is filled; a panic may leak.
- A guard value cleans up half-done work.
