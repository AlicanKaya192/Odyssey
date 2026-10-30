The borrowing errors you will see while learning Rust, and the first fix to try.

| Code | What it says | First fix |
|---|---|---|
| `E0382` | You used a moved value | Lend it with `&` |
| `E0499` | Two `&mut` at once | Finish one before taking the other |
| `E0502` | `&mut` while a `&` exists | Finish reading first |
| `E0505` | You moved a borrowed value | Move it after finishing with the reference |
| `E0506` | New value for a borrowed one | Assign after the reference's last use |
| `E0596` | `&mut` of something immutable | Add `mut` to the variable |
| `E0597` | The value died before the reference | Move the value to an outer scope |
| `E0515` | Returned a reference to a local | Return the value itself |
| `E0106` | The returned reference's lifetime is unclear | Return a value or write a lifetime |

## E0597: the value does not live long enough

```rust
fn main() {
    let r;
    {
        let value = 5;
        r = &value;
    }
    println!("{r}");
}
```

```text
error[E0597]: `value` does not live long enough
 --> main.rs:5:13
  |
4 |         let value = 5;
  |             ----- binding `value` declared here
5 |         r = &value;
  |             ^^^^^^ borrowed value does not live long enough
6 |     }
  |     - `value` dropped here while still borrowed
7 |     println!("{r}");
  |                - borrow later used here
```

`value` was dropped at the end of the inner block, and `r` tries to read it later. The fix: move `value` to the outer block.

## A common trick: taking a copy

For `Copy` types such as numbers, taking the value rather than a reference solves most conflicts:

```rust
fn main() {
    let mut list = vec![1, 2, 3];
    let first = list[0];
    list.push(first);
    println!("{:?}", list);
}
```

```text
[1, 2, 3, 1]
```

`first` is a copy of the first element, not a reference. Adding to the list is free again.

## Do not fight the compiler

The rule is this: if the compiler refuses something it usually has a good reason. Writing `.clone()` and moving on is sometimes right, but first ask yourself: **who
should really own this data?** Once the design is right most errors disappear.
