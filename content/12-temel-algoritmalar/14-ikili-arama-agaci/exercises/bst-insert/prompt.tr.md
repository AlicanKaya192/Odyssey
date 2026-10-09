`insert(node, value)` fonksiyonunu **özyinelemeyle** yaz: değeri kurala göre
doğru yere eklesin ve alt ağacın kökünü döndürsün. Ağaçta zaten olan değer
**eklenmesin**.

`insert_all(values)` değerleri sırayla ekleyip `inorder` sonucunu döndürüyor;
doğru bir BST'de bu, tekrarsız ve sıralı bir liste. `sorted` ve `sort` yok:
sırayı ağaç kurmalı.

**Beklenen çıktı:**

```
[1, 3, 4, 6, 7, 8, 10, 13, 14]
[2, 5, 9]
```
