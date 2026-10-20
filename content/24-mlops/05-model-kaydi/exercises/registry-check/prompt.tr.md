Bir modelin kayıt girdisi (`entry`) ve diskteki dosyalar (`disk`: dosya yolu → özet) veriliyor. `check_registry(entry, disk)` fonksiyonunu yaz ve sorunların listesini döndür:

1. Önce etiketler, sözlükteki sırayla: etiketin gösterdiği numarada sürüm yoksa `"<etiket>: version <n> does not exist"`.
2. Sonra sürümler, listedeki sırayla: dosya diskte yoksa `"v<n>: file missing"`; varsa ama özeti kayıttakiyle aynı değilse `"v<n>: hash mismatch"`.

Sorun yoksa boş liste.

**Beklenen çıktı:**

```
staging: version 4 does not exist
v2: hash mismatch
v3: file missing
```
