Her çalışan için en üstten kendisine kadar uzanan **yönetim zincirini**
tek bir metin olarak yaz. Adlar `' > '` (boşluk, büyüktür, boşluk) ile
ayrılsın.

Sütunlar: `id`, `path`. `path`'e göre sırala.

```
id  path
--  -------------------------------------
1   Ada Kilic
2   Ada Kilic > Bora Yilmaz
3   Ada Kilic > Bora Yilmaz > Ceren Aksoy
4   Ada Kilic > Bora Yilmaz > Deniz Kaya
5   Ada Kilic > Emre Sahin
6   Ada Kilic > Emre Sahin > Fulya Demir
```

Kademe alıştırmasının aynısı, sayı yerine metinle. Bir hata mesajıyla
karşılaşman muhtemel — `Types don't match between the anchor and the
recursive part`. Mesaj neyin eşleşmediğini söylüyor: iki parçadaki
sütunun tipi.
