`files` dosya adı → içerik (metin), `lock` dosya adı → beklenen SHA-256
(`hashlib.sha256(icerik.encode()).hexdigest()`). `verify_downloads(files,
lock)` her dosya için bir satır döndürsün, ada göre abece sırasıyla:

- özet tutuyorsa `"<ad>: ok"`,
- `lock`'ta var ama tutmuyorsa `"<ad>: mismatch"`,
- `lock`'ta yoksa `"<ad>: not in lock"`.

**Beklenen çıktı:**

```
alpha-1.0.zip: ok
beta-2.1.zip: mismatch
gamma-0.3.zip: not in lock
```
