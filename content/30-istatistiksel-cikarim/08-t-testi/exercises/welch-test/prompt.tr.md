200'er kişilik tasarım testinde (`make_design_test(n=200, seed=121)`) yeni
tasarımın (B) etkisini ölç. Alt alta yaz: B eksi A ortalama farkı (2
basamak), Welch testinin p'si (4 basamak) ve farkın %95 güven aralığı (2
basamak). Başlangıç kodu `ttest_ind(a, b)` yazıyor: aralık "A eksi B"
oluyor ve farkla ters işaretli çıkıyor.

**Beklenen çıktı:**

```text
0.26
0.6747
-0.97 1.49
```
