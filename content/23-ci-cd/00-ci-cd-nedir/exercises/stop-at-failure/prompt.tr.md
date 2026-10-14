Bir hattın aşamaları `(ad, geçti_mi)` çiftlerinden oluşan bir listeyle veriliyor:

- `("test", False)`: `test` aşaması düştü.

`run_pipeline(stages)` fonksiyonunu yaz:

- Aşamalara sırayla bak.
- İlk düşen aşamanın **adını** döndür; hat orada durur.
- Hiçbiri düşmediyse `"passed"` döndür.

Alttaki üç satır fonksiyonunu çağırıp sonucu yazdırıyor.

**Beklenen çıktı:**

```
test
passed
install
```
