# References and Borrowing

We ended the previous section with an annoyance: to measure a text's length we had to give it to a function and take it back in a tuple. But the function
does not want to own the text; it only wants to look.

## A reference: using without taking ownership

A **reference** points at a value but does not own it. It is taken with `&`. Taking a reference is called **borrowing**:

```rust
fn length_of(text: &String) -> usize {
    text.len()
}

fn main() {
    let name = String::from("Ada");
    let length = length_of(&name);
    println!("{name} has {length} letters");
}
```

```text
Ada has 3 letters
```

There are two `&`: in the call `&name` says "I lend it", and in the signature `&String` says "I borrow it". When `length_of` ends, `text` goes out of scope, but
since it is not the owner the text is not dropped. `name` stays valid.

<figure class="fig"><svg viewBox="0 0 640 168" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">stack</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">heap</text><g><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">name</text><text class="dim" x="110" y="71" font-size="12.5">ptr, len 3, cap 3</text></g><g><rect class="box" x="20" y="102" width="230" height="44" rx="8"/><text class="ink" x="34" y="129" font-size="14" font-weight="600">text</text><text class="dim" x="110" y="129" font-size="12.5">&amp;String</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">Ada</text></g><path class="curve" d="M250 66 C320 66 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/><path class="curve2" d="M20 124 C-4 124 -4 66 14 66"/><polygon class="dot2" points="20,66 10,61 10,71"/></svg><figcaption><code>text</code> points not at the text but at the variable <code>name</code>. The owner is still <code>name</code>.</figcaption></figure>

As in real life: someone who borrows a book can read it, but the book belongs to its owner and the borrower may not burn it.

You reach the value behind a reference with `*` (**dereference**). Most of the time you need not write it, because Rust does it in method calls and in `println!`:

```rust
fn main() {
    let x = 5;
    let r = &x;
    println!("{}", *r + 1);
    println!("{r}");
}
```

```text
6
5
```

## To change it: &mut

An ordinary reference only reads. Trying to change a borrowed value gives:

```rust
fn add_mark(text: &String) {
    text.push_str("!");
}

fn main() {
    let word = String::from("hi");
    add_mark(&word);
}
```

```text
error[E0596]: cannot borrow `*text` as mutable, as it is behind a `&` reference
 --> main.rs:2:5
  |
2 |     text.push_str("!");
  |     ^^^^ `text` is a `&` reference, so it cannot be borrowed as mutable
  |
help: consider changing this to be a mutable reference
  |
1 | fn add_mark(text: &mut String) {
  |                    +++
```

To change it you need a **mutable reference**. `mut` is written in three places: the variable, the call and the signature.

```rust
fn add_mark(text: &mut String) {
    text.push_str("!");
}

fn main() {
    let mut word = String::from("hi");
    add_mark(&mut word);
    println!("{word}");
}
```

```text
hi!
```

## The two big rules

This is the heart of this section. For one value, at any moment you have either:

<figure class="fig"><div class="versus"><div><h4>Any number of readers</h4>Many <code>&amp;T</code> can exist at once. None can change it.</div><div><h4>One writer</h4>Only one <code>&amp;mut T</code> can exist, and while it does no other reference can.</div></div><figcaption>The second rule: a reference cannot outlive the value it points at.</figcaption></figure>

This is the rule that prevents data races at compile time. A **data race** happens like this: two pieces of code reach the same data at once, at least one
writes and there is no order between them. The result is unpredictable. In Rust such code does not compile.

Two writers:

```rust
fn main() {
    let mut s = String::from("hi");
    let a = &mut s;
    let b = &mut s;
    a.push_str("1");
    b.push_str("2");
}
```

```text
error[E0499]: cannot borrow `s` as mutable more than once at a time
 --> main.rs:4:13
  |
3 |     let a = &mut s;
  |             ------ first mutable borrow occurs here
4 |     let b = &mut s;
  |             ^^^^^^ second mutable borrow occurs here
5 |     a.push_str("1");
  |     - first borrow later used here
```

A writer while a reader exists:

```rust
fn main() {
    let mut s = String::from("hi");
    let reader = &s;
    let writer = &mut s;
    writer.push_str("!");
    println!("{reader}");
}
```

```text
error[E0502]: cannot borrow `s` as mutable because it is also borrowed as immutable
 --> main.rs:4:18
  |
3 |     let reader = &s;
  |                  -- immutable borrow occurs here
4 |     let writer = &mut s;
  |                  ^^^^^^ mutable borrow occurs here
5 |     writer.push_str("!");
6 |     println!("{reader}");
  |                ------ immutable borrow later used here
```

## Why it matters: reading while changing a list

You may wonder "what harm in a single thread?". Here is the harm. A `Vec` is a list that grows (we see it in the Collections section). Adding an element may move the memory, and
then a reference taken to the first element points at dropped memory:

```rust
fn main() {
    let mut list = vec![1, 2, 3];
    let first = &list[0];
    list.push(4);
    println!("{first}");
}
```

```text
error[E0502]: cannot borrow `list` as mutable because it is also borrowed as immutable
 --> main.rs:4:5
  |
3 |     let first = &list[0];
  |                  ---- immutable borrow occurs here
4 |     list.push(4);
  |     ^^^^^^^^^^^^ mutable borrow occurs here
5 |     println!("{first}");
  |                ----- immutable borrow later used here
```

In C++ the same code compiles and sometimes works, sometimes crashes. In Rust it does not compile.

## Where does a reference end?

A reference ends where it is last used, not at the end of the block. This rule is called **NLL** (non-lexical lifetimes) and it makes code much more comfortable:

```rust
fn main() {
    let mut s = String::from("hello");
    let r1 = &s;
    let r2 = &s;
    println!("{r1} {r2}");
    let r3 = &mut s;
    r3.push_str(" world");
    println!("{r3}");
}
```

```text
hello hello
hello world
```

`r1` and `r2` were last used in `println!` and ended there. That is why the later `&mut` is accepted. You can try changing the order and getting `E0502`.

In practice most `E0502` and `E0499` errors are solved this way: finish the reading first, then write.

## There are no dangling references

In C a function can return the address of a local variable, and this is a big source of bugs. Rust does not allow it:

```rust
fn make_text() -> &String {
    let text = String::from("gone soon");
    &text
}

fn main() {
    println!("{}", make_text());
}
```

```text
error[E0106]: missing lifetime specifier
 --> main.rs:1:19
  |
1 | fn make_text() -> &String {
  |                   ^ expected named lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but there is no value
    for it to be borrowed from
help: consider using the `'static` lifetime, but this is uncommon unless you're
returning a borrowed value from a `const` or a `static`
  |
1 | fn make_text() -> &'static String {
  |                    +++++++
help: instead, you are more likely to want to return an owned value
  |
1 - fn make_text() -> &String {
1 + fn make_text() -> String {
  |
```

The message says `missing lifetime specifier`; we will see lifetimes in the second module. For now the upshot is: `text` will be dropped when the function ends, and a
reference to it would point at nothing. The fix is to return not a reference but the value itself:

```rust
fn make_text() -> String {
    let text = String::from("made here");
    text
}

fn main() {
    println!("{}", make_text());
}
```

```text
made here
```

## for loops and references

Now we can understand the `.iter()` of the earlier section. Walking an array with `for` moves its items if they are not `Copy`. To walk it by borrowing, write `&`:

```rust
fn main() {
    let names = [String::from("Ada"), String::from("Linus")];
    for name in &names {
        println!("{}", name.len());
    }
    println!("{}", names[0]);
}
```

```text
3
5
Ada
```

`&names` lends the array, and `name` is a `&String` on each round. To change them, use `&mut`:

```rust
fn main() {
    let mut values = [1, 2, 3];
    for n in &mut values {
        *n *= 10;
    }
    println!("{:?}", values);
}
```

```text
[10, 20, 30]
```

`*n` reaches the value behind the reference: `n` is an address, `*n` is the number there.

## Which to take? A guide to function signatures

| What the function will do | Parameter | Call |
|---|---|---|
| Only read | `x: &T` | `f(&value)` |
| Change | `x: &mut T` | `f(&mut value)` |
| Keep or consume | `x: T` | `f(value)` |

The rule: **ask for the least power.** If reading is enough, take `&T`.

## Summary

- `&` borrows and does not take ownership. When the reference ends the value is not dropped.
- `&mut` gives permission to change; the variable must be `mut` too.
- At any moment either many `&T` or one `&mut T`. The errors are `E0499` and `E0502`.
- A reference ends where it is last used. Changing the order solves most errors.
- Dangling references do not compile; return the local value itself.
- In a function signature ask for the least power.
