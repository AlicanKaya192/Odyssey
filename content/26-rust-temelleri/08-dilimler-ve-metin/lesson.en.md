# Slices, String and &str

Rust has two types for text, and at first this is one of the most confusing topics. Since you know ownership and borrowing, it is now easy to explain.

## A slice: borrowing a part

A **slice** is a reference looking at part of some data. It owns nothing and holds only a start address and a length. Let us see it with numbers first:

```rust
fn main() {
    let days = [10, 20, 30, 40, 50];
    let middle = &days[1..4];
    println!("{:?}", middle);
    println!("{:?}", &days[..2]);
    println!("{:?}", &days[3..]);
    println!("{}", middle.len());
}
```

```text
[20, 30, 40]
[10, 20]
[40, 50]
3
```

`&days[1..4]` points at the elements at positions 1, 2 and 3. Its type is `&[i32]`: "a slice of `i32`". You may omit the start or end: `[..2]` from the start, `[2..]` to the end, `[..]` the whole.

A slice does not copy the data. This is how functions that work for an array of any length are written:

```rust
fn total(values: &[i32]) -> i32 {
    let mut sum = 0;
    for v in values {
        sum += v;
    }
    sum
}

fn main() {
    let short = [1, 2];
    let long = [1, 2, 3, 4, 5];
    println!("{}", total(&short));
    println!("{}", total(&long));
    println!("{}", total(&long[1..3]));
}
```

```text
3
15
5
```

`[i32; 4]` was an array whose size is part of its type. `&[i32]` is a view whose size is known while running.

## &str: a text slice

`&str` is a slice looking at part of a text. It consists of two numbers: an address and a length.

```rust
fn main() {
    let text = String::from("hello world");
    let first = &text[0..5];
    let second = &text[6..];
    println!("{first} / {second}");
}
```

```text
hello / world
```

<figure class="fig"><svg viewBox="0 0 640 168" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">stack</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">heap</text><g><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">text</text><text class="dim" x="110" y="71" font-size="12.5">ptr, len 11, cap 11</text></g><g><rect class="box" x="20" y="102" width="230" height="44" rx="8"/><text class="ink" x="34" y="129" font-size="14" font-weight="600">first</text><text class="dim" x="110" y="129" font-size="12.5">ptr, len 5</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">hello world</text></g><path class="curve" d="M250 66 C320 66 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/><path class="curve" d="M250 124 C320 124 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/></svg><figcaption><code>first</code> points at the start of the same text and holds a length of 5; there is no copy and no capacity.</figcaption></figure>

The `"hello"` you write in code is a `&str` too: the text is embedded in the program and you get a slice pointing at it. That is why it cannot be changed. Its full name is `&'static str`:
`'static` means "lives for the whole program".

## String and &str

<figure class="fig"><div class="versus"><div><h4>String</h4>Owns. Lives on the heap, can grow and change. Dropped when its scope ends.</div><div><h4>&amp;str</h4>Borrows. Looks at part of a text and cannot change it. Very cheap.</div></div><figcaption>The same relation exists between <code>Vec&lt;T&gt;</code> and <code>&amp;[T]</code>.</figcaption></figure>

Conversions between them:

```rust
fn main() {
    let borrowed: &str = "hi";
    let owned: String = borrowed.to_string();
    let again: &str = &owned;
    let copy: String = String::from(again);
    println!("{borrowed} {owned} {again} {copy}");
}
```

```text
hi hi hi hi
```

## Functions should take &str

In the previous section we wrote `&String`. Better is `&str`: it accepts both a `String` and a text constant.

```rust
fn shout(text: &str) -> String {
    text.to_uppercase()
}

fn main() {
    let text = String::from("owned");
    println!("{}", shout(&text));
    println!("{}", shout("constant"));
    println!("{}", shout(&text[..2]));
}
```

```text
OWNED
CONSTANT
OW
```

`&text` is a `&String`, but Rust turns it into a `&str` by itself. This is called **deref coercion**. The Clippy tool warns you about a `&String` parameter. Likewise write `&[T]` rather than `&Vec<T>`.

## Slices are safe

Let us write a function that returns the first word of a text. If the text were cleared later, a returned number would become meaningless. If we return a slice the compiler protects us:

```rust
fn first_word(text: &str) -> &str {
    match text.find(' ') {
        Some(position) => &text[..position],
        None => text,
    }
}

fn main() {
    let mut text = String::from("hello world");
    let word = first_word(&text);
    text.clear();
    println!("{word}");
}
```

```text
error[E0502]: cannot borrow `text` as mutable because it is also borrowed as immutable
  --> main.rs:11:5
   |
10 |     let word = first_word(&text);
   |                           ----- immutable borrow occurs here
11 |     text.clear();
   |     ^^^^^^^^^^^^ mutable borrow occurs here
12 |     println!("{word}");
   |                ---- immutable borrow later used here
```

The slice borrowed `text`, so the `clear` call gives `E0502`. The mistake was caught while compiling, not while running.

## The biggest trap: text is UTF-8

On a computer text is held as bytes in **UTF-8**. English letters are 1 byte, but letters such as Turkish `ş`, `ğ`, `ı` are 2 bytes. `.len()` gives not the number of letters but the number of **bytes**:

```rust
fn main() {
    println!("{}", "kitap".len());
    println!("{}", "şeker".len());
    println!("{}", "şeker".chars().count());
}
```

```text
5
6
5
```

That is why Rust does not let you reach text with `text[0]`. "Element 0" could be half a letter:

```rust
fn main() {
    let text = String::from("hello");
    println!("{}", text[0]);
}
```

```text
error[E0277]: the type `str` cannot be indexed by `{integer}`
 --> main.rs:3:25
  |
3 |     println!("{}", text[0]);
  |                         ^ string indices are ranges of `usize`
  |
  = help: the trait `SliceIndex<str>` is not implemented for `{integer}`
  = note: you can use `.chars().nth()` or `.bytes().nth()`
          for more information, see chapter 8 in The Book:
          <https://doc.rust-lang.org/book/ch08-02-strings.html#indexing-into-strings>
help: `usize` implements trait `SliceIndex<T>`
 -->
 /rustc/58cf8f9c35b355199727627d07ae34a4e2846d67/library\core\src\slice\index.rs:179:0
  |
  = note: `SliceIndex<[T]>`
 -->
 /rustc/58cf8f9c35b355199727627d07ae34a4e2846d67/library\core\src\bstr\traits.rs:197:0
  |
  = note: `SliceIndex<ByteStr>`
  = note: required for `String` to implement `Index<{integer}>`
```

When taking a slice, if the boundary falls in the middle of a letter the program panics:

```rust
fn main() {
    let text = String::from("şeker");
    println!("{}", &text[0..1]);
}
```

```text
thread 'main' panicked at main.rs:3:25:
end byte index 1 is not a char boundary; it is inside 'ş' (bytes 0..2 of string)
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

The letter `ş` holds bytes 0 and 1, and `[0..1]` would cut it in two. To work letter by letter, use `.chars()`:

```rust
fn main() {
    let word = "şeker";
    for letter in word.chars() {
        print!("[{letter}]");
    }
    println!();
    let reversed: String = word.chars().rev().collect();
    println!("{reversed}");
    println!("{}", word.chars().count());
}
```

```text
[ş][e][k][e][r]
rekeş
5
```

`.chars().rev()` reverses, and `.collect()` gathers the pieces into a new `String`. `.count()` gives the real number of letters. For line endings and such there is `.lines()`, and for words `.split_whitespace()`.

## Common text methods

```rust
fn main() {
    let line = "  Rust is fun  ";
    println!("[{}]", line.trim());
    println!("{}", line.to_uppercase().trim());
    println!("{}", line.contains("fun"));
    println!("{}", line.trim().starts_with("Rust"));
    println!("{}", line.trim().replace("fun", "hard"));
    for word in line.split_whitespace() {
        println!("{word}");
    }
}
```

```text
[Rust is fun]
RUST IS FUN
true
true
Rust is hard
Rust
is
fun
```

| Method | What it does | Returns |
|---|---|---|
| `trim` | Removes space at the start and end | `&str` |
| `to_uppercase` | Converts to capitals | `String` |
| `contains` | Is it inside? | `bool` |
| `starts_with` | Does it start like this? | `bool` |
| `replace` | Replaces | `String` |
| `split` | Walks by splitting | iterator |

Did you notice a rule? **Methods producing new text return `String`; those looking at what exists return `&str`.** `trim` allocates nothing and points at a part of the same text.

## Joining text

```rust
fn main() {
    let a = String::from("Hello");
    let b = String::from("World");
    let with_format = format!("{a}, {b}!");
    println!("{with_format}");
    let with_plus = a + ", " + &b;
    println!("{with_plus}");
    println!("{b}");
}
```

```text
Hello, World!
Hello, World
World
```

`format!` is the most readable way and moves nothing. `+` moves the `String` on the left, so `a` cannot be used afterwards.

## Summary

- A slice is a reference looking at part of some data: `&[T]` or `&str`.
- `String` owns and grows; `&str` borrows. For function parameters prefer `&str` and `&[T]`.
- `.len()` is a number of bytes. Turkish letters are 2 bytes. `text[0]` does not compile, and slicing in the middle of a letter panics.
- To work letter by letter use `.chars()`.
- Methods producing new text return `String`; those looking return `&str`.
