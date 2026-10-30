## Choosing a package and a program

| Command | Job |
|---|---|
| `cargo run --bin report` | Run `src/bin/report.rs` |
| `cargo run -p app` | Run the `app` member of a workspace |
| `cargo build --workspace` | Compile all members |
| `cargo test -p core` | One member's tests |
| `cargo check` | Check without producing a program, the fastest |

## Features

| Command | Job |
|---|---|
| `--features a,b` | Also turn these on |
| `--no-default-features` | Turn off the `default` list |
| `--all-features` | Turn all on |
| `cargo tree -e features` | Which feature comes from whom |

## `Cargo.toml` pieces

```toml
[package]
name = "shop"
version = "0.1.0"
edition = "2024"
default-run = "shop"

[features]
default = ["color"]
color = []
fancy = ["color"]

[dependencies]
core = { path = "../core" }

[profile.release]
strip = true
```

`fancy = ["color"]`: one feature can turn on another. `default-run`: with several programs, which one `cargo run` runs.

## Build script commands

`build.rs` writes these with `println!`:

| Line | Job |
|---|---|
| `cargo:rustc-env=NAME=value` | Gives the code a value through `env!("NAME")` |
| `cargo:rerun-if-changed=file` | Run again only when this file changes |
| `cargo:warning=text` | Show a warning during the build |

Without `rerun-if-changed`, the script runs again when any file in the package changes.
