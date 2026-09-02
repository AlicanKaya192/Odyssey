İki sınavın notları elinde ama **öğrenciler farklı sırada**. Toplamı
alacaksın — ve pandas'ın bunu neden doğru yaptığını göreceksin.

`first` serisi Ada, Kerem, Mina sırasında; `second` ise Mina, Ada, Kerem
sırasında.

**Yapman gerekenler:**

1. İki seriyi topla, sonucu `total` adlı seride tut.
2. `total` serisini ve **en yüksek toplamı yapanın adını** yazdır.
3. `extra` serisi yalnızca `Efe` etiketini taşıyor. `total + extra`
   sonucunu `with_extra` adlı seride tut ve kaç tane `NaN` olduğunu yazdır.

**Beklenen çıktı:**

```
Ada       65
Kerem    115
Mina     100
dtype: int64
Kerem
4
```

**İki şeyi birden görüyorsun:**

- **Hizalama:** sıralar tutmuyordu ama toplam doğru çıktı. pandas `Ada` ile
  `Ada`'yı topladı. NumPy olsaydı sıraya bakıp sessizce yanlış sonuç
  verirdi.
- **Eşleşmeyen etiket:** son satırda dört `NaN` çıkıyor. `Efe` ilk seride
  yok, diğer üçü `extra` içinde yok — pandas uydurmak yerine "bilinmiyor"
  diyor.
