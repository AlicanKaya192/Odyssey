80'er kişilik düzen testinde (`make_layout_test(n=80, seed=181)`) önce her
düzenin ortalamasını sözlük olarak yazdır (hazır), sonra `stats.f_oneway`
ile F (3 basamak) ve p'yi (4 basamak) aynı satırda yaz.

**Beklenen çıktı:**

```text
{'A': 7.97, 'B': 8.38, 'C': 9.17, 'D': 8.58}
2.427 0.0655
```
