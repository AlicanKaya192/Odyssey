MASE'yi yaz ve birimleri farklı iki seride dört tahmini aynı ölçekte
karşılaştır.

**Yapman gerekenler:**

1. `mase(actual, forecast, train, m)` fonksiyonunu yaz (hepsi numpy dizisi):
   pay `np.mean(np.abs(actual - forecast))`, payda
   `np.mean(np.abs(train[m:] - train[:-m]))`.
2. **Günlük satış** (`m = 7`; eğitim 5 Kasım 2024'e kadar, test sonraki
   28 gün): mevsimsel naif ve eğitim ortalaması tahminleri için MASE'yi iki
   ondalıkla aynı satıra yazdır.
3. **Aylık yolcu** (`m = 12`; eğitim 2023 sonuna kadar, test 2024):
   mevsimsel naif (2023'ün kopyası) ve büyümeli mevsimsel naif (2023 ×
   `2023 toplamı / 2022 toplamı`) için MASE'yi iki ondalıkla aynı satıra
   yazdır.
4. İki serinin paydasını (ölçeğini) iki ondalığa yuvarlayıp aynı satıra
   yazdır.

**Beklenen çıktı:**

```
0.88 5.72
1.82 0.5
13.29 22.27
```

Dört tahmin artık aynı cetvelde: yolcuda büyümeli tahmin (0.5) en iyisi,
satışta mevsimsel naif (0.88) 1'in altında, yolcuda düz mevsimsel naif (1.82)
ve satışta ortalama (5.72) çıtanın üstünde. Son satırdaki iki ölçek birbirinden
çok farklı; MAE'leri bu yüzden karşılaştıramazdın.
