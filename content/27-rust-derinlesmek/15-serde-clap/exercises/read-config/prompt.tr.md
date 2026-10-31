`text` içindeki JSON'u `Config`'e oku ve alanları yazdır. `retries` JSON'da yok, `#[serde(default)]` ile 0 olmalı; `proxy` yok, `Option<String>` olmalı.

**Beklenen çıktı:**

```text
localhost:8080
retries: 0
proxy: None
```
