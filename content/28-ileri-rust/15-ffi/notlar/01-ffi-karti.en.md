## Type mapping

| C | Rust |
|---|---|
| `int` | `c_int` |
| `unsigned int` | `c_uint` |
| `long` | `c_long` |
| `char` | `c_char` |
| `double` | `c_double` |
| `size_t` | `usize` |
| `void *` | `*mut c_void` |
| `const char *` | `*const c_char` |
| `int32_t` | `i32` |
| `void` (return) | No return type |
| Function pointer | `extern "C" fn(...)` |
| Nullable function pointer | `Option<extern "C" fn(...)>` |

All are in `std::ffi`. `long` is 32 bits on Windows and 64 on Linux, which is why writing `i64` would be wrong.

## Text types

| Type | Owner | NUL at the end | When |
|---|---|---|---|
| `String` | Rust | No | Inside Rust |
| `&str` | A borrow | No | Inside Rust |
| `CString` | Rust | Yes | Sending to C |
| `&CStr` | A borrow | Yes | Taking from C, constants |
| `OsString` | Rust | No | Operating system paths |

## Conversions

| From, to | Written as |
|---|---|
| `&str` → `CString` | `CString::new(text)?` |
| `CString` → pointer | `text.as_ptr()` |
| Constant → `&CStr` | `c"hello"` |
| Pointer → `&CStr` | `unsafe { CStr::from_ptr(p) }` |
| `&CStr` → `&str` | `text.to_str()?` |
| `&CStr` → text | `text.to_string_lossy()` |

## Declaration forms

| Need | Written as |
|---|---|
| A function from C | `unsafe extern "C" { fn f(); }` |
| Safe for every input | `safe fn f();` |
| A function open to C | `#[unsafe(no_mangle)] pub extern "C" fn f()` |
| A C-compatible struct | `#[repr(C)] struct S { ... }` |
| A C-compatible `enum` | `#[repr(C)] enum E { ... }` |
| A library | `crate-type = ["cdylib"]` |

## A common mistake

Taking the pointer of a temporary `CString`:

```rust
use std::ffi::{CString, c_char};

fn main() {
    let pointer: *const c_char = CString::new("hi").unwrap().as_ptr();
    println!("{pointer:?}");
}
```

```text
warning: this creates a dangling pointer because temporary `CString` is dropped at end
of statement
 --> main.rs:4:62
  |
4 |     let pointer: *const c_char = CString::new("hi").unwrap().as_ptr();
  |                                  --------------------------- ^^^^^^ pointer created
  here
  |                                  |
  |                                  this `CString` is dropped at end of statement
  |
  = help: bind the `CString` to a variable such that it outlives the pointer returned by
    `as_ptr`
  = note: a dangling pointer is safe, but dereferencing one is undefined behavior
  = note: returning a pointer to a local variable will always result in a dangling
    pointer
  = note: for more information, see
    <https://doc.rust-lang.org/reference/destructors.html>
  = note: `#[warn(dangling_pointers_from_temporaries)]` on by default
```

The `CString` drops at the end of the line and the pointer dangles. First `let text = CString::new(...)?;`, then `text.as_ptr()`.
