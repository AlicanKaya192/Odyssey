`l1_columns(c)` `LogisticRegression(penalty="l1", C=c, solver="liblinear")` ile
`SelectFromModel` kurup başlangıç kodundaki veriye `fit` etsin ve seçilen
sütunların sırasını liste olarak döndürsün. `C` küçüldükçe daha az sütun
kalmalı.

**Beklenen çıktı:**

```
[0, 1, 2, 3]
[0, 2]
```
