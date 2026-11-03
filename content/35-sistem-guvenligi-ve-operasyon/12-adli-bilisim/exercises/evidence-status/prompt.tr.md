`evidence` kanıt adı → içerik (metin), `recorded` ad → toplandığı an
kaydedilen SHA-256 (`hashlib.sha256(icerik.encode()).hexdigest()`).
`evidence_status(evidence, recorded)` her kanıt için ada göre abece
sırasıyla bir satır döndürsün: özet tutuyorsa `"<ad>: intact"`, tutmuyorsa
`"<ad>: altered"`, kaydı yoksa `"<ad>: unrecorded"`.

**Beklenen çıktı:**

```
image-1: intact
image-2: altered
image-3: unrecorded
```
