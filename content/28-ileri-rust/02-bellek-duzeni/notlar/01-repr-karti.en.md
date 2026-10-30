## repr options

| Written | What it does | When |
|---|---|---|
| None | The compiler chooses, no promise | Nearly always |
| `#[repr(C)]` | The written order, C's rules | FFI, file formats |
| `#[repr(transparent)]` | The one field's layout | Wrapping a type and converting |
| `#[repr(packed)]` | No gaps | Bytes of a fixed format |
| `#[repr(align(64))]` | Alignment grows | Cache lines |
| `#[repr(u8)]` | The enum tag is `u8` | An enum converted to a number |

## Measuring

| Call | Gives |
|---|---|
| `size_of::<T>()` | Bytes |
| `align_of::<T>()` | Alignment |
| `size_of_val(&x)` | The real size, for a slice |
| `offset_of!(T, field)` | The field's distance from the start |
| `needs_drop::<T>()` | Whether deleting has work to do |

`size_of` and `align_of` are in the prelude; for `offset_of!`, `use std::mem::offset_of;`.

## The manual placement rule

In `repr(C)`, each field goes at the first address that is a multiple of its alignment. At the end, gaps are added until the total size is a multiple of the largest alignment.

| Field | Alignment | Position |
|---|---|---|
| `a: u8` | 1 | 0 |
| `b: u32` | 4 | 4 (1, 2, 3 are gaps) |
| `c: u8` | 1 | 8 |
| End | 4 | 9, 10, 11 are gaps, size 12 |

## A common error

Trusting the Rust layout and writing a struct as it is to a file. In the next compiler version the field order may change, and the file becomes unreadable. Produce the bytes by hand or use `repr(C)`; do not forget that gaps are uninitialized too.
