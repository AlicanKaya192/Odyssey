`pick_cache(key, restore_keys, saved)` fonksiyonunu yaz. `saved` saklanmış önbelleklerin listesi; her biri `[ad, oluşturulma_dakikası]`, **sırasız**.

- Adı tam olarak `key` olan varsa: `"hit: " + ad`
- Yoksa `restore_keys`'teki önekleri sırayla dene; bir önekle başlayanlardan **en yenisini** (oluşturulma dakikası en büyük) bul: `"partial: " + ad`
- Hiçbiri yoksa: `"miss"`

**Beklenen çıktı:**

```
hit: pip-Linux-aaaa
partial: pip-Linux-cccc
partial: pip-Linux-cccc
miss
```
