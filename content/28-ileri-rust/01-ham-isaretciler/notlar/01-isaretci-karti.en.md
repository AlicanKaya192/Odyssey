## Creating

| Written | Result |
|---|---|
| `&x as *const T` | From a reference |
| `&raw const x` | No intermediate reference |
| `&raw mut x` | No intermediate reference, mutable |
| `list.as_ptr()` | The start of a slice |
| `list.as_mut_ptr()` | The start of a slice, mutable |
| `ptr::null()`, `ptr::null_mut()` | Null |
| `Box::into_raw(b)` | Gives up ownership |
| `NonNull::new(p)` | `Option<NonNull<T>>` |

## Using

| Written | Job | Condition |
|---|---|---|
| `*p` | Read | Valid, aligned, alive |
| `*p = v` | Drop the old, write | The old value is valid |
| `p.add(i)` | `i` items forward | In the same piece of memory |
| `p.is_null()` | Is it null | No condition, safe |
| `p.as_ref()` | `Option<&T>` | Valid if not null |
| `ptr::read(p)` | Read bit by bit | No two owners afterwards |
| `ptr::write(p, v)` | Write without dropping | The old value may leak |
| `ptr::copy(a, b, n)` | `n` items, may overlap | Like a memory operation |
| `ptr::swap(a, b)` | Swap the two | They must be valid |

## Back to a reference

```rust
let r: &i32 = unsafe { &*p };
let m: &mut i32 = unsafe { &mut *q };
```

This is the most commonly written conversion. The resulting reference's lifetime is **made up**: the compiler cannot derive a lifetime from a pointer and gives whichever you want. You make sure it does not outlive the value.

## Between types

| Written | Meaning |
|---|---|
| `p as *const u8` | Look at it as another type |
| `p as usize` | Convert to a number (an address) |
| `p.cast::<u8>()` | A more readable `as` |
