`check_value(value, low, high)` fonksiyonunu yaz. Değere sırayla şu soruları sor ve ilk tutan cevabı döndür:

- Değer `None` ise `"missing"`.
- Sayı değilse (`int` ya da `float` değilse) `"not a number"`.
- `low` ile `high` arasında değilse (iki uç dahil) `"out of range"`.
- Hiçbiri değilse `"ok"`.

**Beklenen çıktı:**

```
ok
missing
not a number
out of range
ok
```
