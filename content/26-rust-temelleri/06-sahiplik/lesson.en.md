# Ownership

This section is what sets Rust apart from other languages. Once you understand it, the rest of the language falls into place.
Read slowly and run the examples. It is normal if not everything settles on the first reading.

## First, why: when is memory given back?

While running, a program uses two memory areas:

- **The stack:** fast and orderly. When a function is called its variables go here, and when it ends they all leave at once. The
  **size** of everything on the stack **must be known at compile time**. `i32`, `bool` and fixed arrays go here.
- **The heap:** for data whose size is known only while running or changes: text the user typed, for example. The program asks
  for room and receives its **address**. A value holding that address is called a **pointer**. Room on the heap is not given back by itself.

All the difficulty lies in that heap memory. Forget to give it back and memory runs out. Use it after giving it back, or give it back
twice, and the program breaks. Rust's answer is three rules.

## The three rules

<figure class="fig"><div class="anat"><div class="anat-row"><span><b>1</b></span><span>Every value has an <b>owner</b>: the variable holding it.</span></div><div class="anat-row"><span><b>2</b></span><span>There can be only <b>one</b> owner at a time.</span></div><div class="anat-row"><span><b>3</b></span><span>When the owner goes out of scope the value is <b>dropped</b> and its memory given back.</span></div></div><figcaption>That is all of ownership's rules. Everything else follows from them.</figcaption></figure>

## Our first heap type: String

The `"Ada"` texts so far were embedded in the program and could not change. A `String` lives on the heap and can grow:

```rust
fn main() {
    let mut greeting = String::from("Hello");
    greeting.push_str(", world");
    println!("{greeting}");
}
```

```text
Hello, world
```

`String::from` takes room on the heap and copies the text there. `push_str` appends to the end; for that the variable must be `mut`.

A `String` keeps three parts on the stack: the address of the room on the heap, the current length and the reserved capacity.

<figure class="fig"><svg viewBox="0 0 640 110" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">stack</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">heap</text><g><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">greeting</text><text class="dim" x="110" y="71" font-size="12.5">ptr, len 12, cap 12</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">Hello, world</text></g><path class="curve" d="M250 66 C320 66 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/></svg><figcaption>The three parts on the stack point at the text on the heap. (Capacity was measured with <code>String::capacity</code>.)</figcaption></figure>

## Rule 3: dropped when the scope ends

```rust
fn main() {
    {
        let text = String::from("short life");
        println!("{text}");
    }
    println!("the block ended, text is gone");
}
```

```text
short life
the block ended, text is gone
```

`text` went out of scope at the end of the block. At that point Rust gave the memory on the heap back by itself. This is arranged not by
a helper at run time but by the **compiler**: it adds the cleanup code at the close of the block. There is no manual `free` and no garbage collector.

We can watch this dropping ourselves. Just read the next example for now; `Noisy` is our own type and `impl Drop` says "do this when being dropped".
We will see the details later:

```rust
struct Noisy(&'static str);

impl Drop for Noisy {
    fn drop(&mut self) {
        println!("dropping {}", self.0);
    }
}

fn main() {
    let _a = Noisy("a");
    let _b = Noisy("b");
    println!("end of main");
}
```

```text
end of main
dropping b
dropping a
```

Look at the order in the output: `b` was dropped first, then `a`. Variables are dropped in the **reverse** of the order they were defined.

## Rule 2: the move

Now the most important example. Let us begin with numbers, where nothing is surprising:

```rust
fn main() {
    let x = 5;
    let y = x;
    println!("{x} {y}");
}
```

```text
5 5
```

Let us do the same with `String`:

```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1;
    println!("{s1} {s2}");
}
```

```text
error[E0382]: borrow of moved value: `s1`
 --> main.rs:4:16
  |
2 |     let s1 = String::from("hello");
  |         -- move occurs because `s1` has type `String`, which does not implement the
  `Copy` trait
3 |     let s2 = s1;
  |              -- value moved here
4 |     println!("{s1} {s2}");
  |                ^^ value borrowed here after move
  |
help: consider cloning the value if the performance cost is acceptable
  |
3 |     let s2 = s1.clone();
  |                ++++++++
```

Error code `E0382` is the error you will see most while learning Rust. Read the message carefully:

- `move occurs because s1 has type String`: the value moved, because `String` is not copied.
- `value moved here`: the line where it moved.
- `value borrowed here after move`: the line where you then tried to use it.
- `help: consider cloning`: a suggested fix.

Why did this happen? `let s2 = s1;` does not copy the text on the heap; it copies only the three parts on the stack. At that moment two variables
would point to the same room on the heap. When both went out of scope the same memory would be given back **twice**. Rule 2 prevents exactly this: `s2`
becomes the new owner and `s1` is treated as invalid.

<figure class="fig"><svg viewBox="0 0 640 168" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">stack</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">heap</text><g opacity="0.45"><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">s1</text><text class="dim" x="110" y="71" font-size="12.5">ptr, len 5, cap 5</text></g><line class="curve2" x1="26" y1="66" x2="244" y2="66"/><g><rect class="box" x="20" y="102" width="230" height="44" rx="8"/><text class="ink" x="34" y="129" font-size="14" font-weight="600">s2</text><text class="dim" x="110" y="129" font-size="12.5">ptr, len 5, cap 5</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">hello</text></g><path class="curve" d="M250 124 C320 124 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/></svg><figcaption>After <code>let s2 = s1;</code>: there is still one text on the heap, owned by <code>s2</code>. <code>s1</code> can no longer be used.</figcaption></figure>

This is called a **move**. Since only the small part on the stack is copied it is very cheap: the same even if the text is a gigabyte.

## If you really need a copy: clone

If you want to copy the data on the heap too, you say so explicitly:

```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1.clone();
    println!("{s1} {s2}");
}
```

```text
hello hello
```

<figure class="fig"><svg viewBox="0 0 640 168" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">stack</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">heap</text><g><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">s1</text><text class="dim" x="110" y="71" font-size="12.5">ptr, len 5, cap 5</text></g><g><rect class="box" x="20" y="102" width="230" height="44" rx="8"/><text class="ink" x="34" y="129" font-size="14" font-weight="600">s2</text><text class="dim" x="110" y="129" font-size="12.5">ptr, len 5, cap 5</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">hello</text></g><g><rect class="box" x="390" y="102" width="220" height="44" rx="8"/><text class="ink" x="404" y="129" font-size="14">hello</text></g><path class="curve" d="M250 66 C320 66 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/><path class="curve" d="M250 124 C320 124 320 124 382 124"/><polygon class="dot" points="390,124 380,119 380,129"/></svg><figcaption>After <code>.clone()</code>: two separate texts on the heap, two separate owners.</figcaption></figure>

When you see `.clone()`, work that may be expensive is happening. Rust does not hide this; a copy never appears secretly.

## Copy types: why do numbers not move?

An `i32` uses no heap; its whole value is on the stack. Copying is as cheap as moving and there is nothing to drop twice. So such types carry the
`Copy` property: assignment produces a copy and the old one stays valid.

| `Copy` | Not `Copy` |
|---|---|
| `i32`, `u8`, `f64`, all numbers | `String` |
| `bool`, `char` | `Vec` (later) |
| Tuples and arrays whose items are `Copy` | A tuple containing a `String` |
| Shared references such as `&str` | Every type that uses the heap |

## Functions move ownership too

Giving a value to a function follows the same rule as assignment:

```rust
fn consume(text: String) {
    println!("{text}");
}

fn main() {
    let name = String::from("Ada");
    consume(name);
    println!("{name}");
}
```

```text
error[E0382]: borrow of moved value: `name`
 --> main.rs:8:16
  |
6 |     let name = String::from("Ada");
  |         ---- move occurs because `name` has type `String`, which does not implement
  the `Copy` trait
7 |     consume(name);
  |             ---- value moved here
8 |     println!("{name}");
  |                ^^^^ value borrowed here after move
  |
note: consider changing this parameter type in function `consume` to borrow instead if
owning the value isn't necessary
 --> main.rs:1:18
  |
1 | fn consume(text: String) {
  |    -------       ^^^^^^ this parameter takes ownership of the value
  |    |
  |    in this function
help: consider cloning the value if the performance cost is acceptable
  |
7 |     consume(name.clone());
  |                 ++++++++
```

The call to `consume` took ownership of the text. When the function ended, the parameter `text` went out of scope and the text was dropped. `name` is now
invalid. That is why the compiler refuses; otherwise we would read dropped memory.

Ownership can also be given back through a return value:

```rust
fn shout(text: String) -> String {
    let mut loud = text;
    loud.push_str("!");
    loud
}

fn main() {
    let name = String::from("Ada");
    let name = shout(name);
    println!("{name}");
}
```

```text
Ada!
```

This works, but giving a value to every function and taking it back is tiring. And if the function must also return something else you must write a tuple:

```rust
fn measure(text: String) -> (String, usize) {
    let length = text.len();
    (text, length)
}

fn main() {
    let name = String::from("Ada");
    let (name, length) = measure(name);
    println!("{name} {length}");
}
```

```text
Ada 3
```

The solution is **borrowing**: permission to use a value without giving it away. That is exactly the subject of the next section.

## What does all this gain?

Because these rules are checked at compile time, in safe Rust the following **cannot** happen:

- Reading dropped memory (use after free)
- Giving the same memory back twice (double free)
- Continually leaking memory by forgetting to give it back (in most cases)

A large share of security holes in C and C++ programs come from this class. In Rust most of these errors are caught before the program runs.

## Summary

- Every value has one owner; when the owner goes out of scope the value is dropped.
- `let b = a;` **moves** for types using the heap: `a` becomes invalid, error `E0382`.
- For a real copy use `.clone()`, explicitly and with the cost visible.
- `Copy` types (numbers, `bool`, `char`) are copied on assignment, not moved.
- Giving a value to a function moves it too; it can be taken back through a return value, but the real solution is borrowing.
