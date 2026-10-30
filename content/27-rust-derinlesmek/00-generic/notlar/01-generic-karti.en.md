## Forms

| Job | Written |
|---|---|
| Function | `fn f<T>(x: T) -> T` |
| Two parameters | `fn f<A, B>(a: A, b: B)` |
| A bound | `fn f<T: PartialOrd>(x: &T)` |
| Two bounds | `fn f<T: PartialOrd + Copy>(x: T)` |
| Struct | `struct S<T> { x: T }` |
| Enum | `enum E<T> { A(T), B }` |
| Methods | `impl<T> S<T> { ... }` |
| Only one type | `impl S<f64> { ... }` |
| Const | `fn f<const N: usize>(a: [i32; N])` |
| Giving a type | `f::<i32>(1)`, `Vec::<i32>::new()` |

## Naming customs

| Name | Use |
|---|---|
| `T`, `U` | Any type |
| `K`, `V` | Key, value (`HashMap<K, V>`) |
| `E` | Error (`Result<T, E>`) |
| `N` | A const number |

A longer name is written when meaningful: `Item`, `Output`.

## Common bounds

| Bound | What it gives |
|---|---|
| `PartialOrd` | `<`, `>` |
| `PartialEq` | `==`, `!=` |
| `Copy` | Copied on assignment |
| `Clone` | `.clone()` |
| `Debug` | `{:?}` |
| `Display` | `{}` |

## Errors

| Code | Meaning | Fix |
|---|---|---|
| `E0369` | No operator on `T` | Add a bound |
| `E0599` | No method on `T` | Add a bound |
| `E0308` | The same `T` with different types | A second parameter |
| `E0282` | The type could not be inferred | A turbofish or an annotation |
| `E0107` | The wrong number of type parameters | Fix the count |
