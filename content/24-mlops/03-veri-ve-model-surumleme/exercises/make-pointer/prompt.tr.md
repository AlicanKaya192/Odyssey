Bir metin dosyasının işaret dosyasını kuran `make_pointer(name, text)` fonksiyonunu yaz. Bir sözlük döndürsün:

- `"path"`: dosyanın adı (`name`).
- `"sha256"`: metnin UTF-8 baytlarının SHA-256 özeti, onaltılık yazımın **tamamı** (64 karakter).
- `"size"`: baytların sayısı.

Aynı içerik, adı farklı olsa da aynı özeti verir.

**Beklenen çıktı:**

```
notes.txt 5
2cf24dba5fb0
64
True
```
