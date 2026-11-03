`passes_fermat(n, bases)` `bases` listesindeki **her** `a` için
`pow(a, n - 1, n) == 1` ise `True`, birinde bile değilse `False`
döndürsün. Başlangıç kodu yalnızca ilk tabana bakıyor. Not: test yalnızca
"olası asal" der; `561 = 3 × 11 × 17` asal olmadığı hâlde bu tabanlarla
geçer.

**Beklenen çıktı:**

```
True
False
True
```
