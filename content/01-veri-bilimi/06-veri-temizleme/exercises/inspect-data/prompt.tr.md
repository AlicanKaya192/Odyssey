Veriye dokunmadan önce ona **bakacaksın**. Temizliğin ilk adımı bu.

**Yapman gerekenler:**

1. Tablonun şeklini yazdır.
2. Sütun adlarını **liste hâlinde** yazdır.
3. Sütun tiplerini liste hâlinde yazdır.
4. Tabloda toplam kaç eksik hücre olduğunu yazdır.
5. Kaç tekrar eden satır olduğunu yazdır.

**Beklenen çıktı:**

```
(7, 3)
[' Name ', 'city', 'score']
['str', 'str', 'str']
0
0
```

**Çıktıya dikkatli bak, iki sorun görünüyor:**

- Sütun adı `' Name '` — başında ve sonunda **boşluk** var. Ekranda `Name`
  gibi görünüyor ama `raw["Name"]` yazınca `KeyError` alırsın.
- `score` sütunu **metin** tipinde, sayı değil. İçinde `"abc"` ve `"-1"`
  gibi değerler var.

Eksik ve tekrar sayısı sıfır çıkıyor ama bu veri temiz demek değil: eksikler
`"abc"` ve `"-1"` gibi **sahte değerlerin** içinde saklanıyor, tekrarlar da
farklı yazımlar yüzünden görünmüyor.
