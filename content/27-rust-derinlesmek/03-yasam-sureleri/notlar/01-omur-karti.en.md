## Forms

| Place | Written |
|---|---|
| Function | `fn f<'a>(x: &'a str) -> &'a str` |
| Mutable | `&'a mut T` |
| Struct | `struct S<'a> { x: &'a str }` |
| impl | `impl<'a> S<'a> { ... }` |
| With generics | `fn f<'a, T>(x: &'a T) -> &'a T` |
| Elided | `impl S<'_> { ... }` |
| Static | `&'static str` |

## Elision examples

| What you write | What the compiler sees |
|---|---|
| `fn f(x: &str) -> &str` | `fn f<'a>(x: &'a str) -> &'a str` |
| `fn f(x: &str, n: i32) -> &str` | One reference lifetime: the same |
| `fn f(&self, y: &str) -> &str` | The returned one depends on `self` |
| `fn f(x: &str, y: &str) -> &str` | **Ambiguous: E0106** |

## Which error says what?

| Code | Meaning | Usual fix |
|---|---|---|
| `E0106` | A mark is missing | Add `'a` or return owned |
| `E0597` | The value does not live long enough | Widen the scope |
| `E0515` | Returning a reference to a local | Return owned |
| `E0499`, `E0502` | A borrow clash | Narrow the scope |

## End of a lifetime: last use

A reference's lifetime lasts not to the end of its scope but to its **last use**. That is why the following compiles:

```rust
fn main() {
    let mut list = vec![1, 2];
    let first = &list[0];
    println!("{first}");
    list.push(3);
    println!("{:?}", list);
}
```

```text
1
[1, 2, 3]
```

After `first` is used for the last time, `push` is free.
