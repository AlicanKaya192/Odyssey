# What Rust Is and How to Install It

This path is written so that someone who has never written code can walk it too.
Every new word is explained where it first appears. If you already know another
language you will move quickly through the first few sections; the genuinely new
ideas begin in section six.

## What is a program, what is a compiler?

A computer's processor understands only its own language: **machine code**, very
small instructions made of numbers. The text we write for people to read is called
**source code**. Something has to translate between them.

In Rust that job belongs to the **compiler**. It reads your source code from start
to finish, checks the rules and produces a single program file. On Windows that file
ends in `.exe`. Once compiled, the program needs neither the source code nor the
compiler to run.

<figure class="fig"><div class="flow"><span class="node">main.rs<br>source code</span><span class="arrow">→</span><span class="node acc">rustc<br>compiler</span><span class="arrow">→</span><span class="node ok">main.exe<br>program</span></div><figcaption>Rust's compiler is called <code>rustc</code>. If the code is wrong, the third box never appears.</figcaption></figure>

In interpreted languages such as Python, the program is translated line by line while
it runs. Think of the difference like this:

<figure class="fig"><div class="versus"><div><h4>Python</h4>An error appears when that line is reached. A mistake on a rarely used line can go unnoticed for weeks.</div><div><h4>Rust</h4>An error appears before the program runs. No program exists until the compiler agrees.</div></div><figcaption>Both approaches have their place; Rust charges its price up front.</figcaption></figure>

## Why does Rust exist?

While running, programs keep their data in **memory** (RAM). Memory must be handed
back when it is no longer needed. Most languages solve this in one of two ways:

- **Manual management** (C, C++): the programmer says "give this memory back". It is
  very fast, but forgetting, or doing it twice, leads to security holes.
- **Garbage collector** (Python, Java, C#): a helper runs in the background while the
  program works, finding and cleaning up unused memory. It is comfortable, but it means
  extra work and pauses.

Rust chose a third way: **ownership** rules. When each piece of data is handed back is
proven at compile time. No helper runs in the background, and code that breaks the rules
does not compile. The result is speed close to C together with memory safety. We will
go through these rules step by step in section six.

Let us state the price openly too: **the compiler is strict.** At first your code will
be rejected often. That is not failure; it is how Rust works. The compiler's messages
usually describe the problem and often the fix as well, and we will learn to read them.

## Installation

The official way to install Rust is a program called **rustup**. It installs the
compiler, fetches new versions and brings along two more tools:

| Tool | What it does |
|---|---|
| `rustc` | The compiler: turns source code into a program |
| `cargo` | The project manager: builds, runs, downloads packages (next section) |
| `rustup` | The installation manager: updates Rust itself |

On Windows the steps are:

1. Open `https://www.rust-lang.org/tools/install` in a browser and download
   `rustup-init.exe`.
2. Run the file. During installation it may ask you to install Visual Studio: the
   **linker** Rust uses to assemble programs comes from there. Follow the prompts and
   accept the default options.
3. When it finishes, **close and reopen any terminals and Odyssey**. Rust's folder is
   only visible to newly opened programs.

A **terminal** is the text window where you type commands. On Windows you can open one
by typing "PowerShell" in the Start menu. Test the installation with these two commands:

```bash
rustc --version
cargo --version
```

The numbers may differ; what matters is that a version is printed:

```text
rustc 1.99.1 (58cf8f9c3 2026-10-13)
cargo 1.99.1 (5f94df478 2026-08-27)
```

If something goes wrong, see this section's "Installation Problems" note. The exercises in
this path use the compiler on your computer, so this step is required.

## Your first program

The traditional first program prints a greeting. The whole code is three lines:

```rust
fn main() {
    println!("Hello, world!");
}
```

Its output:

```text
Hello, world!
```

Those three lines contain several new things. Let us take them one at a time.

<figure class="fig"><div class="anat"><div class="anat-row"><span><code>fn</code></span><span>Short for "function": it says that a function definition follows. A function is a named piece of work.</span></div><div class="anat-row"><span><code>main</code></span><span>The function's name. This name is special: a program always starts at <code>main</code>.</span></div><div class="anat-row"><span><code>{ }</code></span><span>Curly braces wrap the function's body. The work is written between them.</span></div><div class="anat-row"><span><code>println!</code></span><span>Prints one line to the screen. The <code>!</code> marks it as a <b>macro</b>: for now, think of it as a special command called with an exclamation mark.</span></div><div class="anat-row"><span><code>;</code></span><span>The semicolon says the command has ended.</span></div></div><figcaption>The parts of the first program.</figcaption></figure>

Text inside quotes is called a **string** and is printed as it is. If you write several
`println!` lines they run in order from top to bottom:

```rust
fn main() {
    println!("First line");
    println!("Second line");
}
```

```text
First line
Second line
```

## Putting values inside text

The `{}` in a string is a **placeholder**: it means "put the next value here". You can
do arithmetic too; `*` is the multiplication sign:

```rust
fn main() {
    println!("{} times {} is {}", 6, 7, 6 * 7);
}
```

```text
6 times 7 is 42
```

Each `{}` takes one value in order. If the number of placeholders and values do not match
the compiler refuses. This is your first example of Rust catching a mistake before the
program runs.

## Reading a compile error

Let us mistype a letter. Writing `prinln` instead of `println` gives:

```rust
fn main() {
    prinln!("Hello");
}
```

```text
error: cannot find macro `prinln` in this scope
 --> main.rs:2:5
  |
2 |     prinln!("Hello");
  |     ^^^^^^
  |
 --> /rustc/58cf8f9c35b355199727627d07ae34a4e2846d67/library\std\src\macros.rs:143:0
  |
  = note: similarly named macro `println` defined here
help: a macro with a similar name exists
  |
2 |     println!("Hello");
  |         +
```

Read the message piece by piece:

- The `error:` line says what is wrong: there is no such macro.
- The `-->` line says where: file `main.rs`, line 2, column 5.
- The `^^^^^^` marks exactly which word is meant.
- A `help:` line, when present, is often the fix. Here it suggests the right name.

When you see an error, do not panic. **Start with the first one** and read these four
parts. Later errors are often consequences of the first and disappear once it is fixed.

## Running in Odyssey

When you press **Run** on the exercise screen, Odyssey saves your code as `main.rs`, compiles
it with the `rustc` on your computer and runs the resulting program. In the terminal panel
you see the compiler's own messages; if there is an error, a short explanation appears below it.

If the compiler cannot be found, the exercise says so plainly. That has nothing to do with
your code; just go back to the installation steps.

## Summary

- The compiler (`rustc`) turns source code into a single program and checks the rules in advance.
- Rust manages memory without a garbage collector, using rules proven at compile time.
- A program starts inside `fn main()`; `println!` prints; `{}` is a value placeholder.
- In an error message read `error`, then `-->`, then `help`. Start with the first error.
