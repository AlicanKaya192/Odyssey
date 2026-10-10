`split_codes(codes)` `"TR-34-0012"` biçimindeki kodları `str.extract` ile
parçalasın: iki büyük harf (ülke), iki rakam (bölge), dört rakam (numara).
Kalıba uymayan kodlar atılsın (`dropna()`). Şunu döndürsün:

- `"country"`: ülkeler (liste)
- `"num"`: numaralar, **tam sayı** (`astype(int)`)

**Döngü yazma.**

**Beklenen çıktı:**

```
['TR', 'TR', 'DE']
[12, 450, 7]
```
