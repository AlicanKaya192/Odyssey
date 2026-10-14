`nearest_labels(text, k)` havuzun (`POOL`) metinleriyle bir
`TfidfVectorizer` eğitsin, havuzun ve `text`'in vektörlerinin nokta
çarpımıyla benzerlik puanlarını bulsun ve en benzer `k` örneğin
kategorilerini döndürsün. Puana göre büyükten küçüğe sırala; eşit
puanlarda havuzda önce gelen önce gelsin
(`sorted(range(len(POOL)), key=lambda i: -scores[i])`).

**Beklenen çıktı:**

```
['shipping', 'shipping', 'refunds']
['returns', 'warranty']
```
