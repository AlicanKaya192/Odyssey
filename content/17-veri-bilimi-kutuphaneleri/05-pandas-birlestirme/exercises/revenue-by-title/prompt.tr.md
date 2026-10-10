`revenue_by_title(sales, products)` satışları (`[product_id, qty]`,
`product_id` sayı) ürünlerle (`[id, title, price]`, `id` **metin**)
eşleştirsin. Önce `id`'yi `int`'e çevir, sonra `left_on="product_id",
right_on="id"` ile birleştir. Her satırın cirosu `qty * price`; ürün adına
göre toplayıp `{ad: ciro}` döndürsün. **Döngü yazma.**

**Beklenen çıktı:**

```
{'cup': 20.0, 'pen': 10.0}
```
