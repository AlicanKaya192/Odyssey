An API wants its field names in `camelCase`, but in Rust we write `snake_case`. Use `rename_all`. If `nick_name` is `None` it must not be written into the JSON at all.

**Expected output:**

```text
{"userId":1}
{"userId":2,"nickName":"gh"}
```
