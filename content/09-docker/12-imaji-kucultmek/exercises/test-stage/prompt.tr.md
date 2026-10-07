Testleri imaja koymadan Dockerfile'da çalıştırmanın yolu bir test aşaması.

**Yapman gereken:** `base` ile `runtime` arasına `test` adında bir aşama
ekle: `base`'den başlasın ve `python -m unittest` çalıştırsın.

Odyssey iki derleme yapacak: `--target test` (testler geçmeli) ve
varsayılan derleme (son aşama `runtime`).

**Beklenen çıktı** (`runtime`):

```
2 + 3 = 5
```
