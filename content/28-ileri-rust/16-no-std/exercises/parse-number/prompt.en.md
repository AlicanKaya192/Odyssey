`tiny/src/lib.rs` is `no_std`. Write `parse_number`: it turns digits into a `u32`. Empty text, a non-digit letter or an overflow gives `None`. Do not use `parse`; use `to_digit` and `checked_mul`.

**Expected output:**

```text
Some(120)
None
None
None
```
