`hsts_ok(value)` HSTS başlığının değerini `;` ile parçalara ayırsın
(her parçada `strip`, adlarda küçük harf). `max-age` bir tam sayıysa ve
en az `31536000` ise **ve** `includesubdomains` parçası varsa `True`,
yoksa `False` döndürsün. Sayı için `isdigit` değil `re.fullmatch(r"[0-9]+", ...)`.

**Beklenen çıktı:**

```
True
False
False
True
False
```
