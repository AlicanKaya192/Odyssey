`top_word_changes(n)` ilk `n` yorumu iki vektörleştiriciyle dönüştürsün:
varsayılan ve `sublinear_tf=True`. Her yorumun **en ağır kelimesinin**
(`argmax`) iki tabloda farklı olduğu kaç yorum var, onu döndürsün.

İpucu: seyrek matriste `X.argmax(axis=1)` her satırın en büyük sütununu
verir; `np.asarray(...).ravel()` ile düz diziye çevir.

**Beklenen çıktı:**

```
100 8
500 38
2000 135
```
