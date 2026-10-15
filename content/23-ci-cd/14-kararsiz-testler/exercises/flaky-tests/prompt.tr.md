`flaky_tests(runs)` fonksiyonunu yaz. `runs` test sonuçlarının listesi; her öğe `[commit, test, sonuç]`, sonuç `"pass"` ya da `"fail"`.

**Aynı commit'te** hem geçen hem düşen test kararsızdır (kod aynıyken sonuç değişmiş). Farklı commit'lerde düşüp geçmek kararsızlık değildir: arada kod değişmiştir.

Kararsız testlerin adlarını, her biri bir kez, abece sırasıyla döndür.

**Beklenen çıktı:**

```
['test_login', 'test_report']
[]
```
