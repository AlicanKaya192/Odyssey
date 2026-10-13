`search_C(values)` hazır `pipe` üzerinde yalnızca modelin `C` değerini
(`values` içinden) **5 katlı** `GridSearchCV` ile arasın
(`scoring="f1_macro"`, yalnızca eğitim verisi). `[en iyi C, test macro F1]`
döndürsün; F1 test verisinde ölçülsün ve 3 basamakla yuvarlansın.

**Beklenen çıktı:**

```
[1, 0.874]
```
