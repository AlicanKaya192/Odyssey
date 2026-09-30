`stock_price.csv` bir hissenin günlük kapanış fiyatı. Üç yılın toplam
getirisini üç yoldan hesapla; biri yanlış.

**Yapman gerekenler:**

1. Dosyayı tarih indeksli oku; `close` sütununu `close` serisine al.
2. Günlük basit getiriyi hesapla: `r = close.pct_change()`.
3. **Gerçek** toplam getiri: son fiyatın ilk fiyata oranından, yüzde olarak
   bir ondalık.
4. **Yanlış** yol: günlük getirilerin toplamı (`r.sum()`), yüzde olarak bir
   ondalık.
5. **Doğru** yol: `(1 + r).cumprod()` serisinin son değerinden, yüzde olarak
   bir ondalık.
6. Logaritmik getirileri hesapla (`np.log(close).diff()`), topla ve
   `np.exp(toplam) - 1` ile yüzdeye çevirip yazdır (bir ondalık).
7. En yüksek günlük getirinin tarihini (`"%Y-%m-%d"`) ve yüzde değerini (iki
   ondalık) aynı satıra yazdır.

**Beklenen çıktı:**

```
66.1
62.3
66.1
66.1
2023-03-02 5.3
```

Dört sayıdan üçü aynı; farklı olan, yüzdeleri toplayan. Getiriler çarpılarak
birikiyor; toplanabilen bir ölçü istiyorsan logaritmik getiri kullanılıyor.
