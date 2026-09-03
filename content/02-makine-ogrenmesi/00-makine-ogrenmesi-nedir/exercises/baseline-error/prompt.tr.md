Model kurmadan önce **taban çizgi** kurulur: hiçbir şey öğrenmeyen en
basit tahmin. Regresyonda bu, her şeye eğitim verisinin ortalamasını
söylemek.

**Yapman gerekenler:**

1. Eğitim fiyatlarının ortalamasını hesapla — taban çizgi bu.
2. Taban çizgiyi iki ondalığa yuvarlayarak yazdır.
3. Her test fiyatı için **mutlak hatayı** hesapla ve listeyi yazdır
   (her biri iki ondalık).
4. Bu hataların ortalamasını yazdır — buna **MAE** deniyor.

**Beklenen çıktı:**

```
297.5
[2.5, 97.5, 82.5]
60.83
```

**Neden mutlak değer:** biri +40, öteki -40 yanılan iki tahminin hataları
toplandığında sıfır çıkar ve model kusursuz görünür. Mutlak değer, yanılma
yönünü değil **miktarını** ölçüyor.

**Bu sayı ne işe yarıyor:** 60.83, kurduğun ilk modelin geçmesi gereken
çizgi. Modelin 55 verirse bir şey öğrenmiş demektir; 65 verirse
öğrenmemiş, üstelik ortalamadan da kötü.
