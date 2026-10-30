# Our Own Vec

We join everything learned so far in one type. `Vec<T>` is not magic: three fields, a little `unsafe` and a careful order. In the end, `MyVec` will do the most important behaviors of the standard one.

## Three fields

<figure class="fig"><svg viewBox="0 0 640 284" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">stack</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">heap</text><g><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">ptr</text><text class="dim" x="110" y="71" font-size="12.5"></text></g><g><rect class="box" x="20" y="102" width="230" height="44" rx="8"/><text class="ink" x="34" y="129" font-size="14" font-weight="600">cap</text><text class="dim" x="110" y="129" font-size="12.5">4</text></g><g><rect class="box" x="20" y="160" width="230" height="44" rx="8"/><text class="ink" x="34" y="187" font-size="14" font-weight="600">len</text><text class="dim" x="110" y="187" font-size="12.5">2</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">10</text></g><g><rect class="box" x="390" y="102" width="220" height="44" rx="8"/><text class="ink" x="404" y="129" font-size="14">20</text></g><g><rect class="box" x="390" y="160" width="220" height="44" rx="8"/><text class="ink" x="404" y="187" font-size="14">?</text></g><g><rect class="box" x="390" y="218" width="220" height="44" rx="8"/><text class="ink" x="404" y="245" font-size="14">?</text></g><path class="curve" d="M250 66 C320 66 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/></svg><figcaption>The first two places are filled, the last two uninitialized: len 2, cap 4.</figcaption></figure>

| Field | Meaning |
|---|---|
| `ptr` | A pointer to the first item on the heap |
| `cap` | How many items have room |
| `len` | How many items are really filled |

The main rule is this sentence, called an **invariant**: the places in `0..len` are filled and valid, and those in `len..cap` are uninitialized. Every `unsafe` line relies on this sentence.

## Allocating memory

To take memory without `Box` and `Vec`, there is `std::alloc`. `Layout` says how much room you want:

```rust
use std::alloc::{self, Layout};
use std::ptr::{self, NonNull};

struct MyVec<T> {
    ptr: NonNull<T>,
    cap: usize,
    len: usize,
}

impl<T> MyVec<T> {
    fn new() -> Self {
        assert!(size_of::<T>() != 0, "zero-sized types are not handled");
        MyVec { ptr: NonNull::dangling(), cap: 0, len: 0 }
    }

    fn grow(&mut self) {
        let new_cap = if self.cap == 0 { 4 } else { self.cap * 2 };
        let new_layout = Layout::array::<T>(new_cap).unwrap();

        let new_ptr = if self.cap == 0 {
            // SAFETY: T is not zero-sized, so the layout size is not zero.
            unsafe { alloc::alloc(new_layout) }
        } else {
            let old_layout = Layout::array::<T>(self.cap).unwrap();
            let old_ptr = self.ptr.as_ptr().cast::<u8>();
            // SAFETY: old_ptr came from alloc with old_layout.
            unsafe { alloc::realloc(old_ptr, old_layout, new_layout.size()) }
        };

        self.ptr = match NonNull::new(new_ptr.cast::<T>()) {
            Some(p) => p,
            None => alloc::handle_alloc_error(new_layout),
        };
        self.cap = new_cap;
    }
}

```

Look at four things:

1. `NonNull::dangling()`: an empty `Vec` allocates no memory, but `ptr` cannot be null. We put an aligned but invalid address. It is never read, because `len` is 0.
2. Capacity doubles. Reallocating at every `push` would be very slow.
3. `realloc` grows the old place or moves it elsewhere. So the old `ptr` is no longer valid.
4. Allocating size zero is undefined behavior. In this version we reject types like `()` with `assert!`.

## push and pop

```rust
impl<T> MyVec<T> {
    fn push(&mut self, value: T) {
        if self.len == self.cap {
            self.grow();
        }
        // SAFETY: len < cap, so the place is inside the allocation and empty.
        unsafe { ptr::write(self.ptr.as_ptr().add(self.len), value) };
        self.len += 1;
    }

    fn pop(&mut self) -> Option<T> {
        if self.len == 0 {
            return None;
        }
        self.len -= 1;
        // SAFETY: the place was filled, and len no longer covers it.
        Some(unsafe { ptr::read(self.ptr.as_ptr().add(self.len)) })
    }
}

```

The order matters: in `push` writing comes first, and `len` grows **after**. In `pop` `len` shrinks first, and reading comes **after**. So the invariant is true at every moment.

We use `ptr::write`, because `*p = value` would try to drop the old value, and there is no old value there. `ptr::read` takes ownership out; since `len` shrank, that place is not looked at again.

## Drop

So far memory is not given back, and items are not dropped. Both are needed:

```rust
impl<T> Drop for MyVec<T> {
    fn drop(&mut self) {
        while self.pop().is_some() {}
        if self.cap != 0 {
            let layout = Layout::array::<T>(self.cap).unwrap();
            // SAFETY: ptr came from alloc or realloc with this layout.
            unsafe { alloc::dealloc(self.ptr.as_ptr().cast::<u8>(), layout) };
        }
    }
}

struct Noisy(&'static str);

impl Drop for Noisy {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn main() {
    let mut list = MyVec::new();
    list.push(Noisy("a"));
    for name in ["b", "c", "d", "e"] {
        list.push(Noisy(name));
    }
    println!("cap {} len {}", list.cap, list.len);
    let last = list.pop();
    println!("popped");
    drop(last);
    println!("dropping the list");
}
```

```text
cap 8 len 5
popped
drop e
dropping the list
drop d
drop c
drop b
drop a
```

First the items (the `pop` loop), then the memory. If `cap == 0`, nothing was allocated, and there is nothing to give back. Note that no item dropped while capacity grew: `realloc` moves bits, and the number of values stays the same.

## All slice methods through Deref

Writing a single `Deref` gives `iter`, `len`, `sort`, `[i]` and all slice methods for free. This is what `Vec` does too:

```rust
use std::ops::{Deref, DerefMut};
use std::slice;

impl<T> Deref for MyVec<T> {
    type Target = [T];

    fn deref(&self) -> &[T] {
        // SAFETY: the first len places are filled, and ptr is aligned and not null.
        unsafe { slice::from_raw_parts(self.ptr.as_ptr(), self.len) }
    }
}

impl<T> DerefMut for MyVec<T> {
    fn deref_mut(&mut self) -> &mut [T] {
        // SAFETY: as above, and &mut self gives unique access.
        unsafe { slice::from_raw_parts_mut(self.ptr.as_ptr(), self.len) }
    }
}

fn main() {
    let mut list = MyVec::new();
    for n in [3, 1, 2] {
        list.push(n);
    }
    list.sort();
    list[0] = 10;
    println!("{} {:?}", list.len(), list.iter().max());
    println!("{:?}", &list[1..]);
}
```

```text
3 Some(10)
[2, 3]
```

## IntoIterator

An iterator taking ownership is a bit subtle: `MyVec` must not drop, or it deletes the items twice. For this, `ManuallyDrop`:

```rust
use std::mem::ManuallyDrop;

struct IntoIter<T> {
    ptr: NonNull<T>,
    cap: usize,
    start: usize,
    end: usize,
}

impl<T> IntoIterator for MyVec<T> {
    type Item = T;
    type IntoIter = IntoIter<T>;

    fn into_iter(self) -> IntoIter<T> {
        let me = ManuallyDrop::new(self);
        IntoIter { ptr: me.ptr, cap: me.cap, start: 0, end: me.len }
    }
}

impl<T> Iterator for IntoIter<T> {
    type Item = T;

    fn next(&mut self) -> Option<T> {
        if self.start == self.end {
            return None;
        }
        // SAFETY: start..end are filled, and start moves past this place.
        let value = unsafe { ptr::read(self.ptr.as_ptr().add(self.start)) };
        self.start += 1;
        Some(value)
    }
}

impl<T> Drop for IntoIter<T> {
    fn drop(&mut self) {
        for _ in &mut *self {}
        if self.cap != 0 {
            let layout = Layout::array::<T>(self.cap).unwrap();
            // SAFETY: ptr came from MyVec with this layout, and MyVec did not drop.
            unsafe { alloc::dealloc(self.ptr.as_ptr().cast::<u8>(), layout) };
        }
    }
}

fn main() {
    let mut list = MyVec::new();
    for name in ["a", "b", "c"] {
        list.push(Noisy(name));
    }
    for item in list {
        if item.0 == "b" {
            break;
        }
    }
    println!("end");
}
```

```text
drop a
drop b
drop c
end
```

If the iterator is left half way, its own `Drop` drops the remaining items. In the output, `a` is taken in the loop and dropped, `b` is dropped at the loop's break, and `c` while the iterator drops.

## What does the real Vec have?

| In this version | In the real one |
|---|---|
| Rejecting ZSTs | For `()` it never allocates, and counts |
| Capacity overflow with `unwrap` | An `isize::MAX` check |
| Code in one type | Split into `RawVec`, with less repeated code |
| No `Send` for `T` | `unsafe impl Send` exists (later) |

## Summary

- The invariant: `0..len` is filled, `len..cap` is empty. Every line relies on this.
- `alloc`, `realloc`, `dealloc` and `Layout::array`.
- In `push` write then `len`, in `pop` `len` then read.
- `Drop`: first items, then memory.
- `Deref<Target = [T]>` gives all slice methods.
