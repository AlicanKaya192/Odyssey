## A comparison

| Property | `&T` / `&mut T` | `*const T` / `*mut T` |
|---|---|---|
| Can it be null? | No | Yes |
| Is it aligned? | Always | No promise |
| Lifetime check | Yes | No |
| Aliasing check | Yes | No |
| Reading | Safe | `unsafe` |
| Is it `Copy`? | `&T` yes, `&mut T` no | Both yes |
| `Send` / `Sync` | By type | No |

## Common errors

| Error | Why it is wrong |
|---|---|
| Returning a pointer to a local variable | The value is gone when the function ends |
| An old `as_ptr` after a `push` on a `Vec` | Reallocation changes the address |
| Writing through a pointer while a `&mut` is alive | The aliasing rule |
| An unaligned look like `*p as u8` | It may not be aligned |

The second error is the sneakiest:

```rust
let mut list = vec![1];
let p = list.as_ptr();
list.push(2);
// p may point to freed memory now.
```

Reading `p` here may be undefined behavior; if capacity is enough, it may not be. This is exactly why it cannot be learned by trying.

## The rule

Hold a raw pointer as short a time as possible. If you have a working `&T`, use it; step down to a pointer only at the point the compiler cannot prove, then return to a reference at once.
