Kafe satışına iki model kur: biri yalnızca serinin geçmişiyle, öteki üç dış
değişkenle. Katsayıları oku.

Başlangıç kodunda `train` (31 Ekim 2024'e kadar) ve `columns` hazır.

**Yapman gerekenler:**

1. Dış değişkensiz model:
   `ARIMA(train["sales"], order=(1, 0, 0), seasonal_order=(0, 1, 1, 7)).fit()`.
2. Dış değişkenli model: aynısı, `exog=train[columns]` ile.
3. İki modelin AIC'sini bir ondalıkla aynı satıra yazdır (önce değişkensiz).
4. Üç dış değişkenin katsayısını `ad katsayı` biçiminde, bir ondalıkla alt
   alta yazdır.
5. Üç katsayının %95 güven aralığını yazdır: `fit.conf_int()` tablosundan her
   değişken için alt ve üst sınır (bir ondalık), `ad alt üst` biçiminde.
6. İki modelin kalıntı standart sapmasını (`resid.iloc[8:].std()`) bir
   ondalıkla aynı satıra yazdır.

**Beklenen çıktı:**

```
9464.3 7568.8
promo 49.3
holiday -75.2
temp_c 5.5
promo 46.1 52.5
holiday -78.0 -72.5
temp_c 5.3 5.7
24.0 9.4
```

Katsayılar doğrudan okunuyor: kampanya günü +49, tatil −75, her derece +5.5.
Güven aralıkları dar ve sıfırdan uzak: üç etki de net. Kalıntının standart
sapması 24'ten 9'a iniyor: model, daha önce "sürpriz" saydığı şeylerin
büyük kısmını artık açıklıyor.
