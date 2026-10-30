`main.rs` `env!("RELEASE_NAME")` istiyor ama değer yok. `build.rs`'te `println!` ile `cargo:rustc-env=RELEASE_NAME=spring` yaz. `cargo:rerun-if-changed=build.rs` de ekle.

**Beklenen çıktı:**

```text
release spring
```
