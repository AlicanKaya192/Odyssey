Kayıt satırları `"10:01 sudo user=bob result=denied cmd=passwd"`
biçiminde: zaman, `sudo`, ardından `anahtar=değer` alanları.
`denied_users(lines, threshold)` `result=denied` satır sayısı `threshold`'a
**eşit ya da büyük** olan kullanıcıları abece sırasıyla döndürsün.

**Beklenen çıktı:**

```
['bob']
['bob', 'eve']
```
