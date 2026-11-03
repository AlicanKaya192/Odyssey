Her dosya `[yol, izin, icerik]`; izin `"644"` gibi sekizlik metin.
`audit_files(files)` iki tür bulgu döndürsün, abece sırasıyla:
`"<yol>: world-writable"` (izinlerin son hanesinde yazma biti var:
`int(mode[-1]) & 2`) ve `"<yol>: secret"` (bir satır, boşlukları
atılıp küçük harfe çevrilince `SECRET_KEYS`'ten biriyle başlıyorsa; dosya
başına bir kez). Dosya İzinleri ve Sır Yönetimi bölümleri.

**Beklenen çıktı:**

```
app/config.ini: secret
tmp/notes.txt: secret
tmp/notes.txt: world-writable
```
