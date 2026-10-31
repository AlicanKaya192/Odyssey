Write `text_of!` in `my_macros/src/lib.rs`: it produces the input's text as a string literal. `input.to_string()` and `format!("{:?}", ...)` do the job.

**Expected output:**

```text
hello
a + 1
Vec<u8>
```
