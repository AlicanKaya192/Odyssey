Veri ortalaması -2, standart sapması 0,5 olan sayılar. Ağlar, optimizer'lar ve
döngünün başı hazır. Döngünün içine iki adımı yaz:

1. Ayırt edici: gerçeklere 1, `fake.detach()`'e 0; iki kaybı topla, yalnızca
   `opt_d` adım atsın.
2. Üretici: `D(fake)` için hedef 1; yalnızca `opt_g` adım atsın.

Sondaki iki satır, üretilen sayıların ortalamasının -2'ye ve ayırt edicinin
ortalama tahmininin 0,5'e yakın olup olmadığını yazıyor.

**Beklenen çıktı:**

```
True
True
```
