Dört hata ölçüsünü birer fonksiyon olarak yaz ve Bölüm 14'teki deneye
uygula. Başlangıç kodunda `actual` (28 günlük test) ve `forecast` (mevsimsel
naif tahmin) numpy dizisi olarak hazır.

**Yapman gerekenler:**

1. Dört fonksiyon yaz; hepsi `actual` ve `forecast` alsın:
   - `mae`: mutlak hataların ortalaması
   - `rmse`: hataların karesinin ortalamasının karekökü
   - `mape`: `|hata| / |gerçek|` ortalaması × 100
   - `bias`: hataların ortalaması (gerçek − tahmin)
2. Dört sonucu iki ondalığa yuvarlayıp aynı satıra yazdır (sıra: MAE, RMSE,
   MAPE, yanlılık).
3. RMSE / MAE oranını iki ondalığa yuvarlayıp yazdır.
4. Aynı dört ölçüyü, her gün için eğitim ortalamasını tahmin eden yöntem için
   de yazdır (`np.full(28, train.mean())`).

**Beklenen çıktı:**

```
11.64 13.98 3.46 6.79
1.2
75.98 94.02 20.9 75.98
```

Mevsimsel naifte yanlılık MAE'nin yarısı kadar: hatalar iki yöne dağılmış.
Ortalama tahmininde MAE ile yanlılık aynı sayı: 28 günün hepsinde tahmin
düşük. Dört ölçü aynı sıralamayı veriyor, ama her biri başka bir şey
söylüyor: tipik ıska, büyük ıska, oransal ıska ve ıskanın yönü.
