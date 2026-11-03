`routes` her biri `[method, path, changes_state]` olan uç noktalar.
`risky_routes(routes)` yöntemi `GET` ya da `HEAD` olduğu hâlde durum
değiştiren uç noktaların yollarını, listedeki sırayla döndürsün.

**Beklenen çıktı:**

```
['/delete-account', '/ping']
```
