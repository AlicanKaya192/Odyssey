# Cargo and Your First Project

For a one-file program `rustc main.rs` is enough. But a real project consists of several
files, uses code written by others and needs settings. Managing that by hand is hard.
**Cargo** is Rust's project manager, and the whole Rust world uses it.

Cargo does three basic jobs: it builds the project, runs it and downloads other code the
project needs.

## A new project

Let us create a project in a terminal:

```bash
cargo new hello
```

```text
Creating binary (application) `hello` package
```

Cargo opened a folder and put these inside:

```text
hello
├── .git
├── .gitignore
├── Cargo.toml
└── src
    └── main.rs
```

Source code lives in the `src` (source) folder. The file `src/main.rs` is nearly the same as our
first program; Cargo writes a ready "Hello, world!". `.git` and `.gitignore` are for the version control
tool Git: if Git is on your computer, Cargo opens a repository too. If you do not know Git, that does not matter for now.

## Cargo.toml: the project's identity

`Cargo.toml` is the project's settings file. It is written in a simple format called TOML:
`name = "value"` lines and headings in square brackets.

```toml
[package]
name = "hello"
version = "0.1.0"
edition = "2024"

[dependencies]
```

| Line | Meaning |
|---|---|
| `[package]` | What follows describes the project itself |
| `name` | The project's name; the resulting program takes this name too |
| `version` | The project's version number |
| `edition` | Which **edition** of Rust's rules to compile with |
| `[dependencies]` | Other packages the project uses; empty for now |

What is an **edition**? Every few years Rust releases a new edition that brings small language
changes without breaking old code: 2015, 2018, 2021, 2024. Each project says in its own file which
edition it uses, so old projects keep compiling. New projects use the latest.

## Building and running

Let us enter the project folder and build. `cd` changes folder in a terminal:

```bash
cd hello
cargo build
```

```text
Compiling hello v0.1.0 (C:\projects\hello)
Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.42s
```

That line teaches something: this build used the `dev` profile, the **fast build, slow program** setting.
`unoptimized` means the code was not improved, and `debuginfo` means debugging information was added.
The time varies by computer.

The program appears under `target/debug/`. Everything Cargo produces is in the `target` folder; if you
delete it your source code stays in place, and it is rebuilt next time.

To build and run straight away:

```bash
cargo run
```

```text
Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.01s
Running `target\debug\hello.exe`
Hello, world!
```

This time there is no `Compiling` line: Cargo saw that nothing changed and did not build again. If you
change the code, `cargo run` builds first.

## A quick check: cargo check

While writing code we often only want to know "does it compile?". `cargo check` checks the rules but
produces no program, so on large projects it is much faster than `cargo build`.

```bash
cargo check
```

```text
Checking hello v0.1.0 (C:\projects\hello)
Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.05s
```

## A fast program: --release

A program you will publish is built with optimisation:

```bash
cargo build --release
```

```text
Compiling hello v0.1.0 (C:\projects\hello)
Finished `release` profile [optimized] target(s) in 0.17s
```

Now the profile is `release` and the result is `optimized`: the build takes longer and the program runs
faster. The file goes under `target/release/`.

To measure the difference we ran the same program under both profiles. It performs an addition 300 million
times in a loop. On this computer:

```text
debug:   1.59 s
release: 0.46 s
```

Do not forget `--release` when measuring a program's speed. Numbers measured on a debug build mislead.

<figure class="fig"><div class="versus"><div><h4>cargo build</h4>While developing. Builds fast, runs slowly, checks mistakes such as overflow. Result in <code>target/debug/</code>.</div><div><h4>cargo build --release</h4>When publishing and measuring. Builds slowly, runs fast. Result in <code>target/release/</code>.</div></div><figcaption>The two profiles produce two different programs from the same code.</figcaption></figure>

## Packages: crates

In Rust a unit of compilation, meaning a library or a program, is called a **crate**. Crates written by
others live on the `crates.io` site. To use one you only write its name and version under `[dependencies]`,
and Cargo handles the rest:

```toml
[dependencies]
serde = "1"
```

On the first build it downloads and compiles the crate. It writes which versions were used to the
`Cargo.lock` file, so anyone building the project on another computer gets the same versions. `Cargo.toml`
is your wish; `Cargo.lock` is the exact record Cargo derived from it.

We will not use outside packages in this module. First we learn the language itself.

## Cargo in Odyssey

Most exercises in this path are a single file compiled with `rustc main.rs`. If you see a `Cargo.toml` in an
exercise, Odyssey uses `cargo`, and all of it works without internet. In this section's exercises you will
edit the `Cargo.toml` file too.

One tip: you can read a value from `Cargo.toml` at compile time. The `env!` macro turns the given name into
text while compiling, and Cargo provides the project's name as `CARGO_PKG_NAME`:

```rust
fn main() {
    println!("{} {}", env!("CARGO_PKG_NAME"), env!("CARGO_PKG_VERSION"));
}
```

```text
hello 0.1.0
```

## Summary

- `cargo new name` opens a project; code is in `src/main.rs`, settings in `Cargo.toml`.
- `cargo run` builds and runs, `cargo build` only builds, `cargo check` only checks.
- `--release` builds slowly and runs fast. Speed measurements use it.
- `target` holds produced files, not source code.
- Packages are called crates; they go under `[dependencies]` in `Cargo.toml`, exact versions stay in `Cargo.lock`.
