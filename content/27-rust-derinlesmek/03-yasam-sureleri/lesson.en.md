# Lifetimes

Recall the second half of the borrowing rule: **a reference cannot outlive its owner.** The compiler usually checks this by itself. Sometimes, though, it needs information the code alone does not give: "Which input does the returned reference depend on?" You write this information with a **lifetime** mark.

The most important sentence up front: **a lifetime mark makes no value live longer.** It only tells the compiler the relation between references.

## The problem: a dangling reference

```rust
fn main() {
    let r;
    {
        let x = 5;
        r = &x;
    }
    println!("{r}");
}
```

```text
error[E0597]: `x` does not live long enough
 --> main.rs:5:13
  |
4 |         let x = 5;
  |             - binding `x` declared here
5 |         r = &x;
  |             ^^ borrowed value does not live long enough
6 |     }
  |     - `x` dropped here while still borrowed
7 |     println!("{r}");
  |                - borrow later used here
```

`x` was deleted in the inner block, and `r` still points to it. Rust catches this at compile time. The part doing this check is called the **borrow checker**.

## The question the compiler cannot ask

A function returning the longer of two texts:

```rust
fn longest(x: &str, y: &str) -> &str {
    if x.len() > y.len() { x } else { y }
}

fn main() {
    println!("{}", longest("a", "bb"));
}
```

```text
error[E0106]: missing lifetime specifier
 --> main.rs:1:33
  |
1 | fn longest(x: &str, y: &str) -> &str {
  |               ----     ----     ^ expected named lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but the signature does
    not say whether it is borrowed from `x` or `y`
help: consider introducing a named lifetime parameter
  |
1 | fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
  |           ++++     ++          ++          ++
```

The compiler does not decide by looking at the function's body; it looks at its signature. In the signature two references go in and one comes out. Which does the returned one depend on? `x` or `y`? The calling code needs to learn this to know whether it is safe.

## Writing the mark

A lifetime parameter is written `'a` and is introduced in angle brackets like a generic:

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

fn main() {
    let a = String::from("long text");
    let b = "short";
    println!("{}", longest(&a, b));
}
```

```text
long text
```

It reads: "There is a duration `'a`; `x` and `y` live at least that long; the returned reference is valid at least that long too." In practice `'a` equals the **shorter** of `x` and `y`.

That is why this code does not compile:

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

fn main() {
    let a = String::from("long text");
    let result;
    {
        let b = String::from("short");
        result = longest(&a, &b);
    }
    println!("{result}");
}
```

```text
error[E0597]: `b` does not live long enough
  --> main.rs:10:30
   |
 9 |         let b = String::from("short");
   |             - binding `b` declared here
10 |         result = longest(&a, &b);
   |                              ^^ borrowed value does not live long enough
11 |     }
   |     - `b` dropped here while still borrowed
12 |     println!("{result}");
   |                ------ borrow later used here
```

`b` was deleted before `result`. Even if the function's body were to choose `a`, the compiler looks only at the signature, and the signature says "the returned one depends on the shorter".

## Only where needed

If `y` does not affect the return at all, do not mark it:

```rust
fn keep_first<'a>(x: &'a str, y: &str) -> &'a str {
    println!("ignoring {y}");
    x
}

fn main() {
    let a = String::from("kept");
    let result;
    {
        let b = String::from("gone");
        result = keep_first(&a, &b);
    }
    println!("{result}");
}
```

```text
ignoring gone
kept
```

Now the returned one depends only on `x`, and `y` may live as briefly as it likes.

## A reference to a local cannot be returned

The mark does no magic. A value the function itself creates is deleted when the function ends:

```rust
fn make<'a>() -> &'a str {
    let text = String::from("hi");
    &text
}

fn main() {
    println!("{}", make());
}
```

```text
error[E0515]: cannot return reference to local variable `text`
 --> main.rs:3:5
  |
3 |     &text
  |     ^^^^^ returns a reference to data owned by the current function
```

The fix is not a mark but returning an owned value: `String`.

## Why do we not write it in most functions?

`fn first_word(s: &str) -> &str` has no mark but compiles. The compiler adds the mark itself in common cases. This is called **lifetime elision**. There are three rules:

| Rule | Meaning |
|---|---|
| 1 | Each reference parameter gets its own lifetime |
| 2 | If there is one input lifetime, outputs get it |
| 3 | If there is `&self`, outputs get its lifetime |

If the output's lifetime is still unknown after the three rules, the compiler asks you: `E0106`. `longest` fell exactly here.

## A struct holding a reference

If a struct holds a reference it needs a mark too: "This struct cannot outlive the text it holds."

```rust
struct Excerpt<'a> {
    text: &'a str,
}

impl<'a> Excerpt<'a> {
    fn text(&self) -> &str {
        self.text
    }

    fn first_word(&self) -> &'a str {
        self.text.split_whitespace().next().unwrap_or("")
    }
}

fn main() {
    let novel = String::from("Call me Ishmael. Some years ago");
    let first = novel.split('.').next().unwrap();
    let part = Excerpt { text: first };
    println!("{}", part.text());
    println!("{}", part.first_word());
}
```

```text
Call me Ishmael
Call
```

`impl<'a> Excerpt<'a>` introduces it as with generics. For `text(&self) -> &str` the third rule is enough. If it is not written:

```rust
struct Excerpt {
    text: &str,
}

fn main() {
    let e = Excerpt { text: "hi" };
    println!("{}", e.text);
}
```

```text
error[E0106]: missing lifetime specifier
 --> main.rs:2:11
  |
2 |     text: &str,
  |           ^ expected named lifetime parameter
  |
help: consider introducing a named lifetime parameter
  |
1 ~ struct Excerpt<'a> {
2 ~     text: &'a str,
  |
```

In a structure carrying text, holding a `String` is usually simpler. A struct holding references is preferred when avoiding a copy is really necessary.

## 'static

A special lifetime: it lives until the end of the program. Text literals are like this, because they are embedded in the program:

```rust
fn name() -> &'static str {
    "Odyssey"
}

fn main() {
    let n: &'static str = name();
    println!("{n}");
}
```

```text
Odyssey
```

The compiler sometimes suggests `'static`. Usually this is not the right fix: it hides a wrong lifetime. Think about ownership first.

## Summary

- A reference cannot outlive its owner; the borrow checker does the check.
- A mark does not extend a value; it writes the relation between references.
- `fn f<'a>(x: &'a str, y: &'a str) -> &'a str`: the returned one is valid as long as the shorter.
- The compiler looks only at the signature. A local value cannot be returned by reference; return it owned.
- The three elision rules make most marks unnecessary.
- A struct holding a reference wants `struct S<'a>`. `'static` is until the end of the program.
