## When to write generics?

Write with a concrete type first. Turn it generic when a second type is really needed: three small steps.

1. Write it for `i32`, and test.
2. Turn `i32` into `T`, and listen to the compiler.
3. Add the bounds it asks for.

Generality that will never be used makes code harder to read.

## Together with ownership

```rust
fn first_copy<T: Copy>(list: &[T]) -> T {
    list[0]
}

fn first_clone<T: Clone>(list: &[T]) -> T {
    list[0].clone()
}

fn first_ref<T>(list: &[T]) -> &T {
    &list[0]
}

fn main() {
    println!("{}", first_copy(&[1, 2]));
    let words = [String::from("a"), String::from("b")];
    println!("{}", first_clone(&words));
    println!("{}", first_ref(&words));
}
```

```text
1
a
a
```

| Signature | What it takes | Bound |
|---|---|---|
| `fn f<T>(x: T)` | Ownership | None |
| `fn f<T>(x: &T)` | A borrow | None |
| `fn f<T: Copy>(x: &[T]) -> T` | Returns a copy | `Copy` |
| `fn f<T: Clone>(x: &[T]) -> T` | Returns a `.clone()` | `Clone` |

Returning `&T` usually asks for the least: neither a copy nor a bound is needed.

## Where does a bound go?

| Place | Effect |
|---|---|
| `struct S<T: Debug>` | Must be written at each use; **avoid** |
| `impl<T: Debug> S<T>` | Only on those methods; **prefer** |

## PhantomData

Sometimes a type parameter is needed only as a mark and is not held in a field. The compiler does not accept an unused parameter; `std::marker::PhantomData` fills that gap. We will see it in the advanced module.
