`kl_term(mu, logvar)` derste yazılan KL terimini hesaplasın (`(B, D)`
girdiler): `-0.5 · ortalama_B( toplam_D(1 + logvar − mu² − e^logvar) )`.
3 basamakla döndürsün; eksi sıfır yazmasın diye sonuca `+ 0.0` ekle.

**Beklenen çıktı:**

```
2.0
0.0
```
