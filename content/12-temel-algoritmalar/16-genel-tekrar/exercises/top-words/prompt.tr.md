`top_words(words, k)` fonksiyonunu yaz: en sık geçen `k` kelimeyi, **sayıya
göre azalan**, sayısı eşitse **alfabetik** sırayla bir liste olarak
döndürsün.

İki adım: sözlükle say, sonra sırala ya da heap kullan
(`heapq.nsmallest(k, ..., key=...)`). Anahtar için `(-sayı, kelime)` demeti
iki ölçütü birden verir. `Counter` ve `most_common` yok.

**Beklenen çıktı:**

```
['the', 'and', 'cat']
['a', 'b']
```
