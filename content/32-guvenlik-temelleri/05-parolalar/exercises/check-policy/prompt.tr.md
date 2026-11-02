`check_policy(password, username, common)` bir parolayı bugünkü kılavuzlara
göre denetleyip sorunların listesini şu sırayla döndürsün:

1. `"too-short"`: 12 karakterden kısaysa,
2. `"common"`: büyük/küçük harf farkı gözetmeden `common` listesindeyse,
3. `"has-username"`: kullanıcı adı boş değilse ve büyük/küçük harf farkı
   gözetmeden parolanın içinde geçiyorsa.

Sorun yoksa boş liste. Karakter türü kuralı **yok**.

**Beklenen çıktı:**

```
['too-short', 'common']
['has-username']
[]
```
