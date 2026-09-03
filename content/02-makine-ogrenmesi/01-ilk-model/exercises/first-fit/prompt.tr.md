Önceki bölümde eşiği döngüyle arıyordun. Şimdi aynı işi üç satırda
yapacaksın — ve ilk kez bir kütüphane çağıracaksın.

Elinde sekiz evin metrekaresi ve fiyatı var.

**Yapman gerekenler:**

1. `sklearn.linear_model` içinden `LinearRegression` sınıfını içe aktar.
2. `areas` listesini modelin beklediği biçime çevir: **her sayı ayrı bir
   satır** olacak, çünkü `X` bir tablo olmak zorunda.
3. Bir model kur ve `fit` ile eğit.
4. Öğrendiği **eğimi** iki ondalıkla yazdır (`coef_`, ilk elemanı).
5. Öğrendiği **kesişimi** iki ondalıkla yazdır (`intercept_`).
6. **95 metrekarelik** bir ev için tahmini iki ondalıkla yazdır.

**Beklenen çıktı:**

```
2.43
33.35
264.17
```

İlk iki satır modelin öğrendiği kuralın kendisi:

```
fiyat = 2.43 x metrekare + 33.36
```

Üçüncü satır o kuralın **veride olmayan** bir girdiye uygulanması. Veride
90 var, 100 var, 95 yok — model aradaki değeri kuraldan üretti.

**Not:** `import` satırını sen yazacaksın. Bu bölümden itibaren başlangıç
kodu hazır içe aktarma vermiyor; hangi şeyin nereden geldiğini bilmek
işin parçası.
