Bu bölümün verisi 1500 kart işlemi ve içlerinden yalnızca 85'i
dolandırıcılık. Sınıflardan biri **%5,7**.

Bölüm 03'te doğruluğun tek başına yetmediğini görmüştün. Burada
yetmemekle kalmıyor — yanıltıyor.

**Yapman gerekenler:**

1. Veriyi oku, `X` olarak üç sütunu (`amount`, `hour`, `attempts`), `y`
   olarak `fraud` sütununu al.
2. Pozitif oranını yazdır (üç ondalık).
3. Veriyi ayır: `test_size=0.25`, `random_state=42`, **`stratify=y`**.
   Sonra ölçekle (lojistik regresyon ölçeklemeden hoşlanıyor).
4. Test kümesindeki toplam kayıt sayısını ve **dolandırıcılık sayısını**
   yan yana yazdır.
5. Taban çizgiyi kur: **her şeye 0 de.** Doğruluğunu ve recall'ünü yan yana
   yazdır (üç ondalık).
6. `LogisticRegression(max_iter=1000)` eğit. Doğruluk, precision, recall ve
   F1 değerlerini tek satırda yazdır.
7. Karışıklık matrisini yazdır.
8. Son satırda kaç dolandırıcılığın **kaçırıldığını** yazdır.

**Beklenen çıktı:**

```
0.057
375 21
0.944 0.0
0.955 0.75 0.286 0.414
[[352   2]
 [ 15   6]]
15
```

**Taban çizgi 0,944.** Hiçbir şey yapmayan, tek satır model kodu
içermeyen bir tahminci %94,4 doğru. Bu sayıyı bir sunumda görsen
etkilenirdin.

**Model 0,955.** Taban çizgiden 1,1 puan yukarıda. "Modelimiz %95,5
doğrulukta" cümlesi teknik olarak doğru ve tamamen boş.

**Şimdi recall'e bak: 0,286.** Test kümesindeki 21 dolandırıcılığın
**15'i kaçmış**. Ürün açısından model dolandırıcılıkların dörtte üçünü
görmüyor.

**Doğrulukla recall arasındaki fark burada:**

- Doğruluk 0,944 → 0,955. Grafiğe koysan düz çizgi.
- Recall 0,000 → 0,286. Hiçbir şeyden altı yakalamaya.

İkisi de aynı iki modeli anlatıyor. **Ölçüyü seçen kişi sonucu da
seçiyor.**

Model kasten tembellik yapmıyor: eğitim verisinin 1068 satırı negatif,
57'si pozitif. "Emin değilsen negatif de" stratejisi toplam hatayı
gerçekten düşürüyor. Sorun modelde değil, ona sorduğumuz soruda.
