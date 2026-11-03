`needs_preflight(method, headers)` istek basit değilse `True`
döndürsün. Basit istek: yöntem `SIMPLE_METHODS` içinde; her başlık adı
(küçük harfle) `SIMPLE_HEADERS` içinde; `content-type` varsa değerinin
`;`'den önceki kısmı (küçük harf, `strip`) `SIMPLE_TYPES` içinde.

**Beklenen çıktı:**

```
False
False
True
True
True
```
