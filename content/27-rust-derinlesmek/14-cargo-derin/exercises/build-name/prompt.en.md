`main.rs` wants `env!("RELEASE_NAME")`, but there is no value. In `build.rs`, write `cargo:rustc-env=RELEASE_NAME=spring` with `println!`. Also add `cargo:rerun-if-changed=build.rs`.

**Expected output:**

```text
release spring
```
