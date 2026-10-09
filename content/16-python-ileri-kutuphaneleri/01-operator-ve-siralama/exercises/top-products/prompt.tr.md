`top_products(products, n)` fonksiyonunu yaz: `{"name": ..., "sales":
...}` sözlüklerinden en çok satan `n` ürünün adlarını, satışı büyükten
küçüğe döndürsün. Bütün listeyi sıralamadan: `heapq.nlargest(n, products,
key=itemgetter("sales"))`.

**Beklenen çıktı:**

```
['book', 'pen']
```
