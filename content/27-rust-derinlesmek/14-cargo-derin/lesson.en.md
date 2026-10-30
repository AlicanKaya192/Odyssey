# Workspaces and Features

As a project grows, one crate is not enough. This section covers Cargo's tools for large projects: gathering several crates under one roof, optional features, build profiles and a build script.

## A library and a program together

In the Fundamentals we saw `src/main.rs` or `src/lib.rs`. Both can live in one package: the work is in the library, and the program is only a thin shell. Tests then reach the logic directly.

```text
src/lib.rs        the work
src/main.rs       program shop
src/bin/report.rs program report

$ cargo run --bin shop
total 7

$ cargo run --bin report
report: 2 items
report total 7

$ cargo run
error: `cargo run` could not determine which binary to run. Use the `--bin` option to
specify a binary, or the `default-run` manifest key.
available binaries: report, shop
```

Each file under `src/bin/` becomes a separate program. `cargo run --bin report` chooses which one runs.

## A workspace: one roof

For several connected crates, one `Cargo.toml` at the root is enough:

```toml
[workspace]
resolver = "3"
members = ["app", "calc"]

```

Members have only their own `Cargo.toml`; they connect to each other with `path`:

```toml
# app/Cargo.toml
[package]
name = "app"
version = "0.1.0"
edition = "2024"

[dependencies]
calc = { path = "../calc" }

```

When it runs:

```text
app/Cargo.toml   calc/Cargo.toml
app/src/main.rs  calc/src/lib.rs

$ cargo run -p app
42

$ cargo test -p calc --quiet
running 1 test
.
test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in
0.00s


running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in
0.00s
```

| What a workspace gives | Result |
|---|---|
| One `target/` folder | The same thing is not compiled twice |
| One `Cargo.lock` | Everyone uses the same version |
| `cargo test --workspace` | Tests all at once |
| `-p name` | Works with one member |

You can write common versions in one place at the root: `[workspace.dependencies]`, and `serde.workspace = true` in the member. Raising a version then takes one line.

## A feature: optional code

A `feature` adds optional code to the build. Those who do not use it do not pay for it:

```toml
[package]
name = "shop"
version = "0.1.0"
edition = "2024"

[features]
default = ["color"]
color = []
shout = []

```

In code it is selected with `#[cfg(feature = "...")]`:

```rust
fn greet() -> String {
    let text = String::from("hello");

    #[cfg(feature = "shout")]
    let text = text.to_uppercase();

    #[cfg(feature = "color")]
    let text = format!("[color] {text}");

    text
}

fn main() {
    println!("{}", greet());
}

```

The same code, three different builds:

```text
$ cargo run
[color] hello

$ cargo run --features shout
[color] HELLO

$ cargo run --no-default-features
hello
```

| Command | Meaning |
|---|---|
| `cargo run` | Those in the `default` list are on |
| `cargo run --features shout` | `shout` is on as well |
| `cargo run --no-default-features` | None is on |
| `cargo run --all-features` | All are on |

The rule: a feature **adds**, it does not remove. If two dependencies ask for the same crate with different features, Cargo merges them. If turning one on breaks the other, the design is wrong.

The same in tests: `cargo test --all-features`. Code that is off is not compiled, so the compiler cannot see errors inside it.

## Conditional compilation

`#[cfg(...)]` is not only for features:

```rust
fn main() {
    #[cfg(target_os = "windows")]
    println!("windows build");

    #[cfg(not(target_os = "windows"))]
    println!("other build");

    if cfg!(debug_assertions) {
        println!("debug checks on");
    } else {
        println!("debug checks off");
    }
}
```

```text
windows build
debug checks on
```

`#[cfg]` removes code from the build. The `cfg!` macro only gives `true` or `false`; both arms are compiled. `debug_assertions` is on in `cargo build` and off in `--release`.

## Profiles

`dev` compiles fast, `release` runs fast. Their settings change in `Cargo.toml`. You can define your own profile too; `inherits` says which one to start from:

```toml
[profile.small]
inherits = "release"
opt-level = "z"
lto = true
codegen-units = 1
strip = true
panic = "abort"

```

The size of the same small program in three profiles (measured on this computer):

```text
cargo build                   176 KB
cargo build --release         132 KB
cargo build --profile small   111 KB
```

| Setting | Effect |
|---|---|
| `opt-level` | 0 no optimization, 3 the fastest, `"z"` the smallest |
| `lto` | Optimization across crates, and slower builds |
| `codegen-units = 1` | Better code, slower builds |
| `strip` | Drops debugging information |
| `panic = "abort"` | No stack unwinding, and the program shrinks |

## A build script

`build.rs` in the root folder is compiled and run **before** the crate. Its output gives the build information:

```rust
// build.rs
fn main() {
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rustc-env=BUILD_TAG=v7");
}

// src/main.rs
fn main() {
    println!("tag {}", env!("BUILD_TAG"));
}

```

```text
$ cargo run
tag v7
```

One rule: `build.rs` can run in every build, so it must be short and free of side effects. A build script going to the internet or writing into the source folder causes trouble on someone else's computer; a file you generate goes to `OUT_DIR`.

## Summary

- The work is in the library, and `main.rs` is thin; `src/bin/` holds several programs.
- A workspace: one `target/`, one `Cargo.lock`, `-p name`.
- A feature adds; `#[cfg(feature = "...")]` selects the code.
- `#[cfg]` removes code, and `cfg!` only gives a value.
- Profiles trade size and speed.
- `build.rs` runs before the crate; keep it short.
