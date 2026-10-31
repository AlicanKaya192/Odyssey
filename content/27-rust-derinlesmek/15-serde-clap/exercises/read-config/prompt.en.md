Read the JSON in `text` into `Config` and print the fields. `retries` is not in the JSON and must be 0 with `#[serde(default)]`; `proxy` is not there and must be an `Option<String>`.

**Expected output:**

```text
localhost:8080
retries: 0
proxy: None
```
