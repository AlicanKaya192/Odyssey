`caesar` hazır, `cipher_data.py`'de `SAMPLE` ve `ENGLISH_FREQ` var.

`best_shift(secret, freq)` 0'dan 25'e her kaydırma `s` için
`caesar(secret, -s)` metninin ki-kare puanını hesaplasın ve **en küçük**
puanlı kaydırmayı döndürsün. Puan: her harf için beklenen = `toplam *
freq[harf] / 100`, puan += `(gorulen - beklenen) ** 2 / beklenen`.

**Beklenen çıktı:**

```
7
20
```
