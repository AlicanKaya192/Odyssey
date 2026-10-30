## Memory calls

| Call | Job | Condition |
|---|---|---|
| `Layout::new::<T>()` | One `T` | None |
| `Layout::array::<T>(n)` | `n` of `T` | `Err` on overflow |
| `alloc::alloc(layout)` | Take memory | Size cannot be zero |
| `alloc::realloc(p, old, size)` | Grow | `p` was allocated with that layout |
| `alloc::dealloc(p, layout)` | Give back | `p` was allocated with that layout |
| `handle_alloc_error(layout)` | Memory ran out | Exits, never returns |

`alloc` can return a null pointer: when memory runs out. Checking is required.

## Moving places

| Call | Job |
|---|---|
| `ptr::write(p, v)` | Write, without dropping the old |
| `ptr::read(p)` | Take ownership out |
| `ptr::copy(a, b, n)` | Move `n` items, may overlap |
| `ptr::copy_nonoverlapping(a, b, n)` | Faster, cannot overlap |

`insert` shifts like this:

```rust
unsafe {
    let p = self.ptr.as_ptr().add(index);
    ptr::copy(p, p.add(1), self.len - index);
    ptr::write(p, value);
}
self.len += 1;
```

`remove` is the reverse: first `read` the value, then `copy` the rest one forward, and `len -= 1` last.

## A checklist

| Question | If wrong |
|---|---|
| Does each `alloc` have one `dealloc`? | A leak or a double free |
| Is `dealloc` with the same `Layout`? | Undefined behavior |
| Does each filled item drop exactly once? | A leak or a double free |
| Is an old pointer left after `realloc`? | Undefined behavior |
| Did `len` grow before writing? | Undefined behavior in a panic |
