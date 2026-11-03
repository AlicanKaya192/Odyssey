`policy` rol → izinli işlemler listesi; `"everyone"` anahtarındaki
işlemler **herkese** açık. `allowed(role, operation, policy)` işlem rolün
listesinde ya da `"everyone"` listesindeyse `True`, değilse `False`
döndürsün. Politikada olmayan rol hata vermesin: varsayılan olarak
reddedilir (yalnızca `"everyone"` işlemleri açık).

**Beklenen çıktı:**

```
True
False
True
False
```
