Mevsimsel naif tahmine, geçmiş hatalarının yüzdeliklerinden bir aralık
ekle ve aralığın dürüst olup olmadığını ölç.

**Yapman gerekenler:**

1. Bir gün sonrası hatasını hesapla: `error = s - s.shift(7)`. 2023'ün
   hatalarını `past`, 2024'ünkileri `future` olarak ayır.
2. `past`'ın %10 ve %90 yüzdeliklerini bir ondalıkla aynı satıra yazdır.
   Bunlar %80'lik aralığın tahmine eklenecek sınırları.
3. 15 Mart 2024 için tahmini (`s.shift(7)`), aralığın alt ve üst ucunu ve
   gerçek değeri tam sayıya yuvarlayıp aynı satıra yazdır.
4. `coverage(level)` fonksiyonunu yaz: `past`'tan o düzeyin iki yüzdeliğini
   alsın (`(1 - level) / 2` ve `1 - (1 - level) / 2`) ve `future` hatalarının
   ne kadarının bu iki sınır arasında kaldığını üç ondalıkla döndürsün.
5. `coverage(0.5)`, `coverage(0.8)` ve `coverage(0.95)` sonuçlarını aynı
   satıra yazdır.

**Beklenen çıktı:**

```
-21.0 23.0
288 267 311 301
0.533 0.825 0.945
```

Üç aralık da söylediğine çok yakın kapsıyor. Hiçbir formül, hiçbir dağılım
varsayımı kullanmadın: yalnızca "bu yöntem geçmişte ne kadar yanıldı" sorusunu
sordun. Aralık simetrik değil (−21 ve +23): hatalar da tam simetrik değildi.
