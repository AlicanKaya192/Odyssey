`count(text)` bölümdeki basitleştirilmiş sayacı yazsın: metni
`re.findall(r"\w+|[^\w\s]", text)` ile parçalara ayır; her noktalama
işareti 1 token, her kelime başladığı her dört karakter için 1 token
(`"cat"` 1, `"capital"` 2). Toplamı `int` olarak döndür.

**Beklenen çıktı:**

```
1 2 6
```
