`sends_cookie(samesite, cross_site, method, top_level)` tarayıcının
çerezi ekleyip eklemeyeceğini döndürsün. Aynı siteden gelen istek
(`cross_site` yanlış) her zaman `True`. Başka siteden: `"Strict"` hiçbir
zaman; `"Lax"` yalnızca `method == "GET"` **ve** `top_level` ise;
`"None"` her zaman.

**Beklenen çıktı:**

```
Strict GET False
Lax POST False
Lax GET True
Lax POST True
None POST True
```
