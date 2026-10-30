## The places of &

| Written | Meaning |
|---|---|
| `&x` | Borrow x (for reading) |
| `&mut x` | Borrow x (for writing) |
| `x: &T` | A reading reference parameter |
| `x: &mut T` | A writing reference parameter |
| `*r` | The value behind the reference |
| `&&T` | A reference to a reference; rare |

## let mut r = &x versus let r = &mut x

A confusing pair:

```rust
fn main() {
    let a = 1;
    let b = 2;
    let mut r = &a;
    println!("{r}");
    r = &b;
    println!("{r}");

    let mut c = 3;
    let w = &mut c;
    *w = 30;
    println!("{c}");
}
```

```text
1
2
30
```

| Written | Can the variable point elsewhere? | Can the value behind it change? |
|---|---|---|
| `let r = &x` | No | No |
| `let mut r = &x` | **Yes** | No |
| `let r = &mut x` | No | **Yes** |
| `let mut r = &mut x` | Yes | Yes |

## Automatic dereference

When calling a method, `.` adds as many `*` as needed. So `text.len()` is written the same for `String` and `&String`. Comparison is different: `&i32` and `i32` cannot
be compared directly with `==`; write `*r == 5`.

## A reference is a value too

`&T` is `Copy`: creating a second reader of the same thing is free. `&mut T` is not `Copy`, because there cannot be two writers at once.

## The size of a reference

A reference is an address, so it is very small: 8 bytes on this machine. However large the text, lending it is equally cheap.
