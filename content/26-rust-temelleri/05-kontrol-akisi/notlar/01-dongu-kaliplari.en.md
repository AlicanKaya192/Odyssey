Common loop patterns. We compiled and ran all of them.

## Sum

```rust
fn main() {
    let mut total = 0;
    for n in 1..=100 {
        total += n;
    }
    println!("{total}");
}
```

```text
5050
```

The total must be `mut` and opened before the loop. If you open it inside the loop, it resets on every round.

## Counting

```rust
fn main() {
    let mut evens = 0;
    for n in 1..=10 {
        if n % 2 == 0 {
            evens += 1;
        }
    }
    println!("{evens}");
}
```

```text
5
```

## Finding the largest

```rust
fn main() {
    let values = [3, 9, 2, 7];
    let mut largest = i32::MIN;
    for v in values {
        if v > largest {
            largest = v;
        }
    }
    println!("{largest}");
}
```

```text
9
```

We used `i32::MIN` as the starting value: whatever number comes is greater than or equal to it.

## Stopping once found

```rust
fn main() {
    let values = [4, 8, 15, 16];
    for v in values {
        if v % 5 == 0 {
            println!("first: {v}");
            break;
        }
    }
}
```

```text
first: 15
```

## Common mistakes

| Symptom | Cause |
|---|---|
| The last element is missing | `1..n` leaves the last value out; `1..=n` is needed |
| The total is always the last value | `total` was opened inside the loop |
| The program does not end | The variable in the `while` condition never changes |
| `cannot assign twice` | The counter is not `mut` |
