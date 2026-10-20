Depodan geri gelen bir dosyanın içeriği (`text`) ile işaret dosyası (`pointer`: `"path"`, `"sha256"`, `"size"`) veriliyor. `verify(pointer, text)` fonksiyonunu yaz:

- Metnin UTF-8 baytlarının sayısı `pointer["size"]` değilse `"size mismatch"` döndür. Boyu ölçmek ucuz; önce ona bak.
- Boy tutuyor ama SHA-256 özeti (onaltılık yazımın tamamı) `pointer["sha256"]` değilse `"hash mismatch"`.
- İkisi de tutuyorsa `"ok"`.

**Beklenen çıktı:**

```
ok
size mismatch
hash mismatch
```
