`append_value(head, value)` fonksiyonunu yaz: listenin **sonuna** `value`
değerli yeni bir düğüm eklesin ve listenin başını döndürsün.

İki durum var: liste boşsa yeni düğüm listenin başı olur. Değilse son düğüme
(`next`'i `None` olana) kadar git ve onun `next`'ine yeni düğümü bağla.

**Beklenen çıktı:**

```
[1, 2, 3, 4]
[9]
```
