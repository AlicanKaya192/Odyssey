## Split and gather

Divide a list into slices, process each slice on its own branch, and join the results:

```rust
use std::thread;

fn parallel_sum(list: &[i32], parts: usize) -> i32 {
    let size = list.len().div_ceil(parts).max(1);
    thread::scope(|s| {
        let handles: Vec<_> = list
            .chunks(size)
            .map(|part| s.spawn(move || part.iter().sum::<i32>()))
            .collect();
        handles.into_iter().map(|h| h.join().unwrap()).sum()
    })
}

fn main() {
    let list: Vec<i32> = (1..=100).collect();
    println!("{}", parallel_sum(&list, 4));
}
```

```text
5050
```

`chunks` splits a list without copying. Thanks to `scope`, the branches borrow the slices.

## A worker pool (the idea)

Jobs on a channel, workers on several branches. The standard library has no ready pool. Since the receiver must be single, sharing it wants a `Mutex`; we will see that in section 11.

## An order guarantee

| Method | Order |
|---|---|
| Joining handles in order | The starting order |
| Receiving from a channel | The finishing order, unknown |
| A channel + a sequence number | You sort afterwards |

**Do not compare output of unknown order in a test:** sort first. A test passing once may be luck.

## Common errors

- **Not waiting for a branch:** `main` ends and the job is cut off.
- **Not closing `tx`:** `for x in rx` hangs.
- **Syncing with `thread::sleep`:** it differs per machine. Use `join` or a channel.
- **Opening a branch for a small job:** opening a branch has a cost too; it only gains if the job is big enough.
