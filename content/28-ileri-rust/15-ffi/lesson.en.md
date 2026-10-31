# FFI: Talking to C

Most operating systems, databases, graphics and cryptography libraries offer a C interface. Calling them from Rust, or making Rust code callable from other languages, is called **FFI** (Foreign Function Interface).

C is the common language of programming: from Python to Java, most languages talk to each other by C's rules. So learning to talk to C is learning to talk to all of them.

This section needs no C compiler: Rust programs already link to the C runtime library, and we will call its functions directly.

## The first call

To introduce a foreign function, we write its signature:

```rust
use std::ffi::c_int;

unsafe extern "C" {
    fn abs(n: c_int) -> c_int;
}

fn main() {
    let value = unsafe { abs(-7) };
    println!("{value}");
}
```

```text
7
```

- `extern "C"`: this function uses C's calling convention (ABI, how arguments pass).
- `c_int`: C's `int`. Since its size may vary by platform, this name is used instead of `i32`.
- `unsafe extern`: we wrote the signature, and the compiler cannot know if it is right. If we write it wrong, it is undefined behaviour.

The call itself needs `unsafe` too:

```rust
use std::ffi::c_int;

unsafe extern "C" {
    fn abs(n: c_int) -> c_int;
}

fn main() {
    println!("{}", abs(-7));
}
```

```text
error[E0133]: call to unsafe function `abs` is unsafe and requires unsafe block
 --> main.rs:8:20
  |
8 |     println!("{}", abs(-7));
  |                    ^^^^^^^ call to unsafe function
  |
  = note: consult the function's documentation for information on how to avoid undefined
    behavior
```

If `abs` is safe for every input, we can say so in the declaration. `safe fn` turns the call into an ordinary function; the promise now belongs to whoever wrote the declaration:

```rust
use std::ffi::c_int;

unsafe extern "C" {
    safe fn abs(n: c_int) -> c_int;
}

fn main() {
    println!("{}", abs(-7));
}
```

```text
7
```

## Strings: the most common problem

Rust's `&str` is a pointer and a length. A C string is only a pointer; its end is known by a **NUL byte** (`0`). They are not the same thing:

```rust
use std::ffi::c_char;

unsafe extern "C" {
    fn strlen(text: *const c_char) -> usize;
}

fn main() {
    let length = unsafe { strlen("hello") };
    println!("{length}");
}
```

```text
error[E0308]: mismatched types
 --> main.rs:8:34
  |
8 |     let length = unsafe { strlen("hello") };
  |                           ------ ^^^^^^^ expected `*const i8`, found `&str`
  |                           |
  |                           arguments to this function are incorrect
  |
  = note: expected raw pointer `*const i8`
               found reference `&'static str`
note: function defined here
 --> main.rs:4:8
  |
4 |     fn strlen(text: *const c_char) -> usize;
  |        ^^^^^^ ----
```

To send text from Rust to C, use `CString`:

```rust
use std::ffi::{CString, c_char};

unsafe extern "C" {
    fn strlen(text: *const c_char) -> usize;
}

fn main() {
    let text = CString::new("hello").unwrap();
    let length = unsafe { strlen(text.as_ptr()) };
    println!("{length}");
    println!("{:?}", text.as_bytes_with_nul());
}
```

```text
5
[104, 101, 108, 108, 111, 0]
```

The second line shows the final `0`. C finds the length by counting bytes, so it counts bytes, not letters:

```rust
use std::ffi::{CString, c_char};

unsafe extern "C" {
    fn strlen(text: *const c_char) -> usize;
}

fn main() {
    let text = CString::new("çay").unwrap();
    println!("{}", unsafe { strlen(text.as_ptr()) });
    println!("{}", "çay".chars().count());
}
```

```text
4
3
```

If there is a NUL in the middle, C ends the string there. That is why `CString::new` returns an error:

```rust
use std::ffi::CString;

fn main() {
    println!("{:?}", CString::new("a\0b"));
    println!("{:?}", CString::new("ab"));
}
```

```text
Err(NulError(1, [97, 0, 98]))
Ok("ab")
```

If the text is constant, the `c"..."` form gives a `&CStr` with no allocation:

```rust
use std::ffi::c_char;

unsafe extern "C" {
    fn strlen(text: *const c_char) -> usize;
}

fn main() {
    println!("{}", unsafe { strlen(c"hello".as_ptr()) });
}
```

```text
5
```

## A safe wrapper

The right shape of FFI code is this: `unsafe` stays inside a small function, and a safe interface comes out.

```rust
use std::ffi::{CString, c_char};

unsafe extern "C" {
    fn strlen(text: *const c_char) -> usize;
}

fn c_length(text: &str) -> Option<usize> {
    let text = CString::new(text).ok()?;
    // SAFETY: text is a valid, NUL-terminated string for the whole call.
    Some(unsafe { strlen(text.as_ptr()) })
}

fn main() {
    println!("{:?}", c_length("hello"));
    println!("{:?}", c_length("a\0b"));
}
```

```text
Some(5)
None
```

The caller now promises nothing. The NUL problem became `None`, and the `unsafe` is on one line with its reason beside it.

## Text coming from C

In the other direction, `CStr` is used: it borrows C's pointer. C functions may return a null pointer to say "none", so that is checked first:

```rust
use std::ffi::{CStr, c_char};

unsafe extern "C" {
    fn getenv(name: *const c_char) -> *const c_char;
}

fn env_var(name: &CStr) -> Option<String> {
    // SAFETY: name is a valid, NUL-terminated string.
    let value = unsafe { getenv(name.as_ptr()) };
    if value.is_null() {
        return None;
    }
    // SAFETY: getenv gave a NUL-terminated string, and we copy it at once.
    Some(unsafe { CStr::from_ptr(value) }.to_string_lossy().into_owned())
}

fn main() {
    println!("{:?}", env_var(c"ODYSSEY_NOT_SET"));
    let text = c"from c";
    println!("{:?}", text.to_str());
}
```

```text
None
Ok("from c")
```

`CStr` is a borrow; C owns the memory. If you will keep it, copy it to a `String` at once.

## Callbacks

We can give C a function too. C's sorting function `qsort` compares with our function:

```rust
use std::ffi::{c_int, c_void};

unsafe extern "C" {
    fn qsort(
        base: *mut c_void,
        count: usize,
        size: usize,
        compare: extern "C" fn(*const c_void, *const c_void) -> c_int,
    );
}

extern "C" fn compare_i32(a: *const c_void, b: *const c_void) -> c_int {
    // SAFETY: qsort gives pointers into the i32 slice we passed.
    let (a, b) = unsafe { (*(a as *const i32), *(b as *const i32)) };
    a.cmp(&b) as c_int
}

fn main() {
    let mut values = [5, 1, 4, 2];
    // SAFETY: the pointer, count and size all describe the same array.
    unsafe {
        qsort(
            values.as_mut_ptr().cast(),
            values.len(),
            size_of::<i32>(),
            compare_i32,
        );
    }
    println!("{values:?}");
}
```

```text
[1, 2, 4, 5]
```

The callback itself must be `extern "C"`. C does not know types: `*const c_void` means "the address of something", and we convert it to the right type. A closure cannot be given, because C has no room for what it captures.

## A panic cannot cross the boundary

A panic cannot leave an `extern "C"` function; C does not know how to unwind. Rust ends the process at once:

```rust
extern "C" fn boom() {
    panic!("inside the callback");
}

fn main() {
    boom();
    println!("never printed");
}
```

```text
thread 'main' panicked at main.rs:2:5:
inside the callback
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace

panic in a function that cannot unwind
thread caused non-unwinding panic. aborting.
```

(We shortened the stack trace in the output.) If that must not happen in a function C will call, catch it with `catch_unwind` and turn it into an error code:

```rust
use std::ffi::c_int;
use std::panic::catch_unwind;

extern "C" fn risky(n: c_int) -> c_int {
    match catch_unwind(|| 100 / n) {
        Ok(value) => value,
        Err(_) => -1,
    }
}

fn main() {
    println!("{}", risky(5));
    println!("{}", risky(0));
}
```

```text
20
-1
```

## Opening Rust to the outside

The other direction: C calling a Rust function. Two things are needed: C's calling convention and a name that does not change. Rust normally changes names (mangling); `#[unsafe(no_mangle)]` turns that off. This lets the linker find it by name. The `unsafe` in the syntax is a reminder that using the same name twice can break linking.

There is no C here, but we can call the same name through a separate declaration, as C would see it:

```rust
mod rust_side {
    #[unsafe(no_mangle)]
    pub extern "C" fn rust_add(a: i32, b: i32) -> i32 {
        a + b
    }
}

mod c_view {
    unsafe extern "C" {
        pub fn rust_add(a: i32, b: i32) -> i32;
    }
}

fn main() {
    let _keep = rust_side::rust_add;
    println!("{}", unsafe { c_view::rust_add(2, 3) });
}
```

```text
5
```

C does not know Rust types. The way to give out a Rust object is an **opaque pointer**: C only holds the address, does not see inside, and gives it back to us for every job.

```rust
pub struct Counter {
    total: u32,
}

#[unsafe(no_mangle)]
pub extern "C" fn counter_new() -> *mut Counter {
    Box::into_raw(Box::new(Counter { total: 0 }))
}

/// # Safety
/// `counter` must come from `counter_new` and must not be freed yet.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn counter_add(counter: *mut Counter, amount: u32) -> u32 {
    let counter = unsafe { &mut *counter };
    counter.total += amount;
    counter.total
}

/// # Safety
/// `counter` must come from `counter_new` and is invalid after this call.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn counter_free(counter: *mut Counter) {
    if !counter.is_null() {
        drop(unsafe { Box::from_raw(counter) });
    }
}

fn main() {
    let counter = counter_new();
    unsafe {
        counter_add(counter, 2);
        println!("{}", counter_add(counter, 3));
        counter_free(counter);
    }
}
```

```text
5
```

The header the C side would see looks like this:

```text
typedef struct Counter Counter;

Counter *counter_new(void);
uint32_t counter_add(Counter *counter, uint32_t amount);
void counter_free(Counter *counter);
```

`Box::into_raw` turns ownership into a pointer, and `Box::from_raw` takes it back. To really open a library to the outside, write `crate-type = ["cdylib"]` in `Cargo.toml`.

## Summary

- `unsafe extern "C" { ... }` introduces a foreign function; the signature's correctness is on us.
- Strings: `CString` from Rust to C, `CStr` from C to Rust, `c"..."` for constants.
- Keep `unsafe` inside a safe wrapper.
- Check a pointer returned from C with `is_null` first.
- A panic cannot cross `extern "C"`, and the process ends; turn it into an error code with `catch_unwind`.
- Opening to the outside: `#[unsafe(no_mangle)]`, `extern "C"`, an opaque pointer.
