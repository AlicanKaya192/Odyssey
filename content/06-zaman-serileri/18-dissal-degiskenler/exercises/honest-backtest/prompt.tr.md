Dış değişkenli modeli kayan başlangıçla sına. Her deneyde gelecek tablosunu
**yalnızca o ana kadar bilinenle** kur: takvim gerçek, sıcaklık mevsim
normali.

Başlangıç kodunda `cuts` (56 gün arayla 6 kesim) ve `plain(train, test)`
(dış değişkensiz modelin tahmini) hazır. (Birkaç saniye sürer.)

**Yapman gerekenler:**

1. `with_exog(train, test)` fonksiyonunu yaz:
   - `columns = ["promo", "holiday", "temp_c"]`
   - Modeli `train` üzerinde kur (`order=(1, 0, 0)`,
     `seasonal_order=(0, 1, 1, 7)`, `exog=train[columns]`).
   - Gelecek tablosu: `test[columns].copy()`; `temp_c` sütununu **eğitim**
     verisinden hesaplanan mevsim normaliyle değiştir
     (`train["temp_c"].groupby(train.index.dayofyear).mean()`; eksik gün için
     `.get(day, normal.mean())`).
   - 28 günlük tahmini numpy dizisi olarak döndür.
2. İki yöntemi 6 deneyde çalıştır: her kesimde eğitim `c.loc[:cut]`, test
   sonraki 28 gün. Her deneyin MAE'sini sakla.
3. Her yöntem için ortalama MAE'yi ve en kötü deneyi iki ondalıkla
   `ad ortalama en_kötü` biçiminde alt alta yazdır (adlar: `plain`, `exog`).
4. Dış değişkenli modelin kazandığı deney sayısını ve becerisini
   (`1 - ortalama_exog / ortalama_plain`, iki ondalık) aynı satıra yazdır.

**Beklenen çıktı:**

```
plain 28.23 44.88
exog 14.81 16.97
6 0.48
```

Tahmin anında bilinenle kurulan model hatayı yarıya indiriyor ve 6 deneyin
6'sında önde. En kötü deney de belirgin biçimde iyileşiyor. Mevsim normalini
her deneyde `train` üzerinden yeniden hesapladın: bütün veriden bir kez
hesaplasaydın test dönemi sıcaklıkları normale sızmış olurdu.
