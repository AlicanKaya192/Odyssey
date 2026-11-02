`belongs_to(url, domain)` adresin sunucusu tam olarak `domain` ise ya da
onun bir alt alan adıysa (`... + "." + domain` ile bitiyorsa) `True`
döndürsün. `domain` büyük harfle gelebilir; küçük harfe çevir.

Başlangıç kodu yalnızca `domain in url` diye bakıyor: alan adı adresin
herhangi bir yerinde geçince kanıyor.

**Beklenen çıktı:**

```
True
False
False
True
```
