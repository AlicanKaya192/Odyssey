## What this version lacks

| Missing | What the real Vec does | Why |
|---|---|---|
| ZSTs | Allocates nothing, `cap` is the largest value | `Vec<()>` works like a counter |
| `Send` / `Sync` | `unsafe impl` exists | `NonNull` does not give them by itself |
| Variance | Correct with `PhantomData<T>` | The next section |
| `Vec::with_capacity` | Exists | Allocating up front |
| `Drain`, `extend` | Panic safe | With the guard pattern |

## Why is RawVec separate?

The real `Vec` is split into `RawVec`, managing memory, and `Vec`, managing items. `RawVec` does not know whether items are filled; it only allocates and gives back memory. Separating responsibilities narrows where the `unsafe` is: `IntoIter` also uses `RawVec` and shares the same code.

## Why does growth double?

| Method | Copies in 1000 `push`es |
|---|---|
| +1 each time | About 500 000 |
| Doubling | Fewer than 1000 |

Doubling means constant work per `push` on average. The price is that half the capacity may stay empty. If you know the size up front, `with_capacity` prevents all of it.

## Should you write your own structure?

Almost never. This section's goal is seeing how `Vec` works and using `unsafe` in a small place. In a real project, first `Vec`, `VecDeque`, `HashMap`; if not enough, a well-tested crate.
