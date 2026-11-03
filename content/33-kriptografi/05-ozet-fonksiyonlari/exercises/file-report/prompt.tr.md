`files` ad → içerik (metin), `known` ad → beklenen SHA-256 (onaltılık).
İçeriğin özeti `hashlib.sha256(icerik.encode()).hexdigest()` ile alınır.
`file_report(files, known)` her dosya için bir satır döndürsün, abece
sırasında:

- özeti `known`'daki değere uyuyorsa `"<ad> ok"`,
- `known`'da var ama özet tutmuyorsa `"<ad> changed"`,
- `known`'da yoksa `"<ad> unknown"`.

**Beklenen çıktı:**

```
a.txt ok
b.txt changed
c.txt unknown
```
