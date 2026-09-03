Şimdi gerçek bir dosyayla bütün akışı kuracaksın: oku, ayır, eğit, ölç.

Yanındaki `homes.csv` dosyasında 40 ev var; sütunlar `area`, `rooms`,
`age`, `price`.

**Yapman gerekenler:**

1. Gereken her şeyi içe aktar ve dosyayı oku.
2. `area` sütununu **tablo** olarak `X`'e, `price` sütununu **sütun** olarak
   `y`'ye al.
3. Veriyi ayır: **dörtte biri test**, `random_state=42`.
4. Eğitim ve test kayıt sayılarını **yan yana** yazdır.
5. Modeli eğit; öğrendiği **eğim ile kesişimi** yan yana yazdır (iki
   ondalık).
6. Test kümesindeki **ortalama mutlak hatayı** yazdır (iki ondalık).

**Beklenen çıktı:**

```
30 10
2.92 -1.48
18.5
```

**Dikkat edilecek üç yer:**

- `X`'te **çift**, `y`'de **tek** parantez. Tek parantezle
  `Expected 2D array` hatası alıyorsun.
- `train_test_split`'in dönüş sırası `X_train, X_test, y_train, y_test`.
  Karıştırırsan hata almıyorsun — yanlış sonuç alıyorsun.
- `random_state=42` olmadan her çalıştırmada başka sayı çıkar ve kontrol
  geçmez. Bu bir kısıt değil, alıştırmanın konusu: **sabitlenmemiş
  rastgelelik tekrarlanamaz sonuç demek.**

`-1.48` bir kesişim ve sıfır metrekarelik bir evin fiyatı gibi okunuyor —
anlamsız. Zararı yok: kesişimin işi doğruyu doğru yere oturtmak, tek
başına yorumlanmak değil.
