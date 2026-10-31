Write the order for `Entry`: the nearest deadline goes on top of the `BinaryHeap` (a reversed `Ord`). The `Sleep` future: `Ready` if the time is up; otherwise put an `Entry` on the heap, call `notify_one`, and return `Pending`.

**Expected output:**

```text
[2, 3, 1]
```
