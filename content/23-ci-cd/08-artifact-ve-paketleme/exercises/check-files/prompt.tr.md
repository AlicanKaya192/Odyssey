`manifest` her dosyanın beklenen SHA-256 özetini tutan bir sözlük, `files` elindeki dosyaların içerikleri (`ad: metin`). `check_files(manifest, files)` fonksiyonunu yaz; sırayla şu satırların listesini döndürsün:

- `manifest`'teki her dosya için: elde yoksa `"ad: missing"`, özeti farklıysa `"ad: changed"`, aynıysa `"ad: ok"`.
- Sonra `files`'ta olup `manifest`'te olmayan her dosya için `"ad: unexpected"`.

Bir metnin özeti için hazır `sha256_text` fonksiyonunu kullan.

**Beklenen çıktı:**

```
app.py: ok
config.json: changed
data.csv: missing
notes.txt: unexpected
```
