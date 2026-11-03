`pseudonym(value, key)` değeri önce `strip()` ve `lower()` ile
normalleştirsin (aynı e-posta farklı yazılmış olabilir), sonra
`hmac.new(key.encode(), value.encode(), hashlib.sha256)` ile özetleyip
onaltılık özetin **ilk 12 karakterini** döndürsün.

**Beklenen çıktı:**

```
5e979343af4e
5e979343af4e
cfa192be9cd7
```
