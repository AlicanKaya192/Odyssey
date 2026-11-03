`is_internal(text)` bir IP adresi metni alsın; adres özel, geri döngü,
bağlantı yerel, belirtilmemiş ya da ayrılmışsa `True`, değilse `False`
döndürsün. Metin geçerli bir IP adresi değilse de `True` döndürsün:
emin olunamayan durumda reddet (`ipaddress.ip_address` `ValueError`
verir).

**Beklenen çıktı:**

```
100.20.30.40 False
127.0.0.1 True
10.1.2.3 True
169.254.169.254 True
0.0.0.0 True
not-an-ip True
```
