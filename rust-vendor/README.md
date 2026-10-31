# rust-vendor

Source code of the Rust crates used by the Rust path's exercises (`serde`, `serde_json`, `clap`, `tokio` and their
dependencies), so that Cargo can build them offline. Odyssey does not download anything for these exercises.

Every crate keeps its own licence files in its folder. The crates here are licensed under MIT, Apache-2.0 or Unlicense;
`unicode-ident` additionally under Unicode-3.0.

Do not edit these files: Cargo checks them against `.cargo-checksum.json`.

To update, in an empty project with these dependencies run `cargo vendor` and replace the folders:

```toml
[dependencies]
clap = { version = "4", features = ["derive"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
tokio = { version = "1", features = ["rt", "rt-multi-thread", "macros", "time", "sync", "net", "io-util"] }
```
