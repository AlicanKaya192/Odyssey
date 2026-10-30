## A skeleton

```rust
struct Steps {
    current: u32,
    end: u32,
}

impl Iterator for Steps {
    type Item = u32;

    fn next(&mut self) -> Option<u32> {
        if self.current >= self.end {
            return None;
        }
        self.current += 1;
        Some(self.current)
    }
}
```

## IntoIterator's three forms

| Written | Element | Source |
|---|---|---|
| `for x in shelf` | `Book` | `impl IntoIterator for Shelf` |
| `for x in &shelf` | `&Book` | `impl IntoIterator for &Shelf` |
| `for x in &mut shelf` | `&mut Book` | `impl IntoIterator for &mut Shelf` |

It is handed to the inner list: `self.books.iter()`, `self.books.iter_mut()`, `self.books.into_iter()`.

## Common errors

| Symptom | Cause |
|---|---|
| The program does not end | No `take` on an endless iterator |
| The first element is skipped | In `next`, increasing and returning are in the wrong order |
| The last element is missing | An end check of `>` rather than `>=`, or the reverse |
| `E0207`, `E0106` | `'a` is missing |

Try the end check with boundary values: an empty range, a single element.

## A length hint

`size_hint` gives "how many elements remain"; `Vec` uses it to reserve room during `collect`. The default is enough. If you know the exact number, `ExactSizeIterator` is also written, which earns `.len()`.
