`valid_time(text)` fonksiyonunu yaz: metin `"HH:MM"` biçimindeyse (iki
rakam, iki nokta, iki rakam: `re.fullmatch`) **ve** saat 24'ten, dakika
60'tan küçükse `True` döndürsün; değilse `False`. Biçimi regex, anlamı
Python denetlesin.

**Beklenen çıktı:**

```
09:30 True
23:59 True
24:00 False
7:15 False
12:60 False
```
