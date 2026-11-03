`parse_age(text)` bir form alanından gelen yaşı izin listesiyle
doğrulasın: metin yalnızca **1 ile 3 arası rakamdan** oluşuyorsa ve değer
150'yi geçmiyorsa sayıyı, değilse `None` döndürsün. Hiçbir girdide hata
vermesin. İpucu: `re.fullmatch(r"[0-9]{1,3}", text)`.

**Beklenen çıktı:**

```
'42' 42
'150' 150
'151' None
'-3' None
'abc' None
'' None
```
