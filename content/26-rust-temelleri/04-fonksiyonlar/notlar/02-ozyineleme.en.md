## A function can call itself

A function calling itself is called **recursion**. Two things are needed: a step that shrinks the work and a condition
that stops it.

```rust
fn factorial(n: u64) -> u64 {
    if n <= 1 {
        return 1;
    }
    n * factorial(n - 1)
}

fn main() {
    println!("{}", factorial(5));
    println!("{}", factorial(20));
}
```

```text
120
2432902008176640000
```

`factorial(5)` opens up like this: `5 * factorial(4)`, which is `4 * factorial(3)`, and so on until `n` is 1. Then the
results are multiplied on the way back.

## If the stopping condition is forgotten

Each call takes room in the memory area called the **stack**. Recursion that never stops fills that area and the program
dies with a stack overflow. Rust does not catch this at compile time, but it stops safely and does not corrupt other memory.

## The type still matters

Even `u64` is not infinite: `factorial(21)` does not fit in `u64` and panics in a development build. Think about limits when
working with large numbers.

## Recursion or a loop?

Both do most jobs. In Rust a loop is usually faster and does not fill the stack. Recursion is natural for structures that
repeat themselves, such as trees. We see loops in the next section.
