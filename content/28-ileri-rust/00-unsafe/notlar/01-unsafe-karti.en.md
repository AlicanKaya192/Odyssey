## Ask while writing

| Question | If the answer is no |
|---|---|
| Is there really no safe way? | Do not write `unsafe` |
| Is the pointer valid and aligned? | Undefined behavior |
| Does the value it points to fit its type? | Undefined behavior |
| Is another `&mut` absent at this moment? | Undefined behavior |
| Can I write `// SAFETY:`? | The code is probably wrong |

## How to write it

```rust
// SAFETY: i < len was checked just above, so the index is in bounds.
let value = unsafe { *list.get_unchecked(i) };
```

```rust
/// Returns the item at `i`.
///
/// # Safety
///
/// `i` must be smaller than `list.len()`.
unsafe fn item_at(list: &[i32], i: usize) -> i32 {
    // SAFETY: the caller guarantees i is in bounds.
    unsafe { *list.get_unchecked(i) }
}
```

| Comment | Place | For whom |
|---|---|---|
| `// SAFETY:` | Above the `unsafe` block | The reader: why it is correct |
| `# Safety` | The `unsafe fn` documentation | The caller: what to guarantee |

## Scope

Keep the `unsafe` block small. Safety is kept not only in the block but in the whole module: a line outside the block can break a condition the block relies on. So fields of a type containing `unsafe` are not `pub`.

## Common calls

| Call | Its condition |
|---|---|
| `get_unchecked(i)` | `i < len` |
| `slice::from_raw_parts(p, n)` | `n` items valid and alive |
| `String::from_utf8_unchecked(v)` | `v` is valid UTF-8 |
| `Box::from_raw(p)` | `p` came from `Box::into_raw` |
| `mem::transmute::<A, B>(x)` | The same size, a valid bit pattern |

`transmute` is the most dangerous; look first at safe ways like `as` and `from_ne_bytes`.
