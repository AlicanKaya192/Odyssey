## Where does the memory go?

If a type is held millions of times, a few bytes matter. Measure first: `size_of::<T>()` is known at compile time.

| Way | Example | Gain |
|---|---|---|
| A small integer | `u32` instead of `u64` | 4 bytes per field |
| Shrinking an enum | Put the large variant in a `Box` | The whole enum shrinks |
| `Box<str>`, `Box<[T]>` | Instead of `String`, `Vec` | No capacity field (16 bytes instead of 24) |
| A type with a free value | `Option<NonZeroU32>` | No tag |

## The largest variant of an enum

An enum takes as much space as its **largest variant**. If one variant is 200 bytes, all are 200 bytes:

```rust
enum Event {
    Click(u8),
    Report([u8; 200]),
}
```

Putting the large variant in a box shrinks all values: `Report(Box<[u8; 200]>)`. The enum is then 16 bytes, but a heap allocation is added for the large variant. Clippy warns with `large_enum_variant`.

## Zero-sized types

`()` and a struct with no fields take no space, so they can carry information as a type:

| Use | Example |
|---|---|
| Storing only keys | `HashSet<T>` is `HashMap<T, ()>` inside |
| State at the type level | `struct Open; struct Closed;` |
| An ownership marker | `PhantomData<T>` (later) |

## Measure, then shrink

Shrinking memory lowers readability. A `Vec<Item>`'s total size is `len * size_of::<Item>()`: if the number is small, do not bother.
