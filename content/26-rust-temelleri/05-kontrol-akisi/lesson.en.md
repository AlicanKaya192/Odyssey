# Conditions and Loops

So far the program has moved along one path from top to bottom. Real programs make decisions and repeat work.

## Decisions with if

```rust
fn main() {
    let score = 72;
    if score >= 90 {
        println!("excellent");
    } else if score >= 50 {
        println!("passed");
    } else {
        println!("failed");
    }
}
```

```text
passed
```

There are no parentheses around the condition, and the curly braces are required. `else if` tests a new condition, and
`else` runs if none holds. The first branch that holds runs, from top to bottom, and the rest are not looked at.

**The condition must be a `bool`.** In some languages a number can be a condition; Rust refuses:

```rust
fn main() {
    let number = 3;
    if number {
        println!("yes");
    }
}
```

```text
error[E0308]: mismatched types
 --> main.rs:3:8
  |
3 |     if number {
  |        ^^^^^^ expected `bool`, found integer
```

You write what you mean: `if number != 0`.

## if is an expression

In the previous section we saw that a block is an expression. `if` is an expression too, so it gives a value. It takes the
place of the ternary operator (`? :`) of other languages:

```rust
fn main() {
    let age = 20;
    let label = if age >= 18 { "adult" } else { "child" };
    println!("{label}");
}
```

```text
adult
```

Watch the semicolons: none inside the branches, because they give values. There is one at the end of the `let` line, because
that is a statement.

The two branches must have the same type. The compiler has to know the variable's type at compile time:

```rust
fn main() {
    let flag = true;
    let value = if flag { 5 } else { "six" };
    println!("{value}");
}
```

```text
error[E0308]: `if` and `else` have incompatible types
 --> main.rs:3:38
  |
3 |     let value = if flag { 5 } else { "six" };
  |                           -          ^^^^^ expected integer, found `&str`
  |                           |
  |                           expected because of this
```

## loop: an endless loop

`loop` repeats until you stop it. `break` leaves the loop, `continue` moves to the next round:

```rust
fn main() {
    let mut n = 0;
    loop {
        n += 1;
        if n == 2 {
            continue;
        }
        if n > 4 {
            break;
        }
        println!("{n}");
    }
}
```

```text
1
3
4
```

`loop` is an expression too: `break` can carry a value. That is very handy for retrying something and getting the result:

```rust
fn main() {
    let mut value = 1;
    let first_big = loop {
        value *= 2;
        if value > 100 {
            break value;
        }
    };
    println!("{first_big}");
}
```

```text
128
```

## while: a conditional loop

It runs as long as the condition is true:

```rust
fn main() {
    let mut n = 3;
    while n > 0 {
        println!("{n}");
        n -= 1;
    }
    println!("go");
}
```

```text
3
2
1
go
```

## for: going over something

This is the most used loop in Rust. It walks over a **range** or a list:

```rust
fn main() {
    for n in 1..4 {
        print!("{n} ");
    }
    println!();
    for n in 1..=4 {
        print!("{n} ");
    }
    println!();
    for n in (1..4).rev() {
        print!("{n} ");
    }
    println!();
}
```

```text
1 2 3
1 2 3 4
3 2 1
```

| Written | Values |
|---|---|
| `1..4` | 1, 2, 3 (end excluded) |
| `1..=4` | 1, 2, 3, 4 (end included) |
| `(1..4).rev()` | 3, 2, 1 (reversed) |
| `(0..10).step_by(2)` | 0, 2, 4, 6, 8 |

Walking over an array is the same. If you need the position, `.iter().enumerate()` gives both the position and the value:

```rust
fn main() {
    let days = ["mon", "tue", "wed"];
    for day in days {
        println!("{day}");
    }
    for (position, day) in days.iter().enumerate() {
        println!("{position}: {day}");
    }
}
```

```text
mon
tue
wed
0: mon
1: tue
2: wed
```

Here `.iter()` gives something that walks the array one element at a time. We will see why this form is needed under ownership, and
iterators in full later.

Prefer `for` to keeping a counter and writing `array[i]` by hand: the chance of passing the limit disappears.

<figure class="fig"><div class="versus"><div><h4>Manual counter</h4><code>while i &lt; days.len() { ... days[i] ... i += 1; }</code><br>Easy to get the limit wrong, and it needs a check each round.</div><div><h4>for</h4><code>for day in days { ... }</code><br>A limit mistake cannot be written.</div></div><figcaption>The Rust habit: if you have a list, use <code>for</code>.</figcaption></figure>

## Leaving nested loops: labels

`break` leaves only the loop it is in. To leave an outer loop, give the loop a **label**. A label starts with a single quote:

```rust
fn main() {
    'outer: for row in 1..=3 {
        for col in 1..=3 {
            if row * col == 4 {
                println!("found at {row} {col}");
                break 'outer;
            }
        }
    }
    println!("done");
}
```

```text
found at 2 2
done
```

## Which one to choose?

| Situation | Loop |
|---|---|
| Going over a list or range | `for` |
| As long as a condition holds | `while` |
| The end becomes clear inside and you return a result | `loop` + `break` |

## Summary

- An `if` condition must be a `bool`; no parentheses, curly braces required.
- `if` is an expression: in `let x = if ... { a } else { b };` both branches must have the same type.
- `loop` + `break` can also return a value; `continue` moves to the next round.
- `for` is the most common loop: `1..4` excludes the end, `1..=4` includes it.
- To leave an outer loop use `'label:` and `break 'label`.
