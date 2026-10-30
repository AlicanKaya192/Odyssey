## Three tools

| Tool | Are contents valid | Does it drop at scope end |
|---|---|---|
| `T` | Yes | Yes |
| `MaybeUninit<T>` | No promise | No |
| `ManuallyDrop<T>` | Yes | No |

## Calls

| Call | Job | `unsafe`? |
|---|---|---|
| `MaybeUninit::uninit()` | An empty place | No |
| `MaybeUninit::new(v)` | A filled place | No |
| `m.write(v)` | Write, without dropping the old | No |
| `m.assume_init()` | Convert to `T` | Yes |
| `m.assume_init_ref()` | `&T` | Yes |
| `m.assume_init_drop()` | Drop in place | Yes |
| `ManuallyDrop::new(v)` | Wrap | No |
| `ManuallyDrop::drop(&mut m)` | Drop now | Yes |
| `ManuallyDrop::into_inner(m)` | Take back | No |
| `mem::forget(v)` | Never drop | No |

`mem::forget` is safe, because a leak is not undefined behavior in Rust. It is only bad.

## The old way

`mem::uninitialized()` and `mem::zeroed()` appear in old code. The first is deprecated. The second is undefined behavior if zero is not valid for `T`: like `&T`, `Box<T>`, `NonNull<T>`.

## A check while working by hand

| Question | If wrong |
|---|---|
| Does each filled place drop exactly once? | A leak or a double free |
| Was it written before reading? | Undefined behavior |
| Is the state valid in a panic? | A double free may happen |
