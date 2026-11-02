Zararsız oyuncak "dosyalar" bir sözlükte: ad → metin içerik.
`known` bilinen kötü örneklerin SHA-256 özetlerinin (hex) listesi.

`signature_scan(files, known)` içeriğinin özeti (`hashlib.sha256(
icerik.encode()).hexdigest()`) listede olan dosyaların adlarını abece
sırasında döndürsün. Hızlı arama için listeyi önce kümeye çevir.

**Beklenen çıktı:**

```
copy.bin
toy.bin
```
