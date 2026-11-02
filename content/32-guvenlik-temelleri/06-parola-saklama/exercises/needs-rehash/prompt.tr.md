`needs_rehash(record, min_iterations)` bir kaydın yeni parametrelerle
yeniden özetlenmesi gerekiyorsa `True` döndürsün:

- algoritma `"pbkdf2_sha256"` değilse,
- kayıt 4 parçalı değilse ya da yineleme sayısı rakam değilse,
- yineleme sayısı `min_iterations`'dan küçükse.

Başlangıç kodu sayıları **metin olarak** karşılaştırıyor: `"90000" <
"600000"` `False` çıkar, çünkü metinler harf harf karşılaştırılır ve `"9"`
`"6"`'dan büyüktür.

**Beklenen çıktı:**

```
1000 True
90000 True
600000 False
1 True
```
