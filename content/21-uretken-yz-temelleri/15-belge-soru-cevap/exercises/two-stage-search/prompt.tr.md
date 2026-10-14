Salt okunur `retrieval.py` dersteki `Index`, `by_article` ve `by_sentence`'i
içeriyor. `two_stage(question)` makale düzeyindeki aramayla en ilgili makaleyi
bulsun (`Index(by_article()).search(question, 1)`) ve `by_sentence()` içinden
yalnızca o makalenin cümlelerini, sırasını bozmadan, metin listesi olarak
döndürsün.

**Beklenen çıktı:**

```
Gift cards are available for
They cannot be exchanged for
You can use one gift
```
