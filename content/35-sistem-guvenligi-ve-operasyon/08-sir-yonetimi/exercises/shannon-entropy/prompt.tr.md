`entropy(text)` metnin karakter başına Shannon entropisini, 2 basamağa
yuvarlanmış olarak döndürsün: her karakterin oranı `p` için
`-sum(p * math.log2(p))`. Boş metin için `0.0` döndürsün.

**Beklenen çıktı:**

```
'aaaaaaaa' 0.0
'password' 2.75
'q8Zr2LxP0vT7mWk9' 4.0
'' 0.0
```
