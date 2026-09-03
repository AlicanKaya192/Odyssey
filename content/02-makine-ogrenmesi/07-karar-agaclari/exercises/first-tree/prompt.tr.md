KNN "bu kayda en çok kim benziyor" diye soruyordu. Karar ağacı bambaşka bir
şey soruyor: **"hangi soruyu sorarsam grubu en iyi ayırırım?"**

Aynı veride üç modeli yan yana koyacaksın.

**Yapman gerekenler:**

1. `customers.csv`'yi oku, üç sütunu `X`'e, `churn`'ü `y`'ye al, ayır
   (`random_state=42`, `stratify=y`).
2. **Taban çizgiyi** kur: en sık sınıf.
3. **Karar ağacı** eğit: `max_depth=3`, `random_state=42`. **Ölçekleme
   yapma** — sebebini bir sonraki alıştırmada göreceksin.
4. **KNN** eğit: `k=25` ve **ölçeklenmiş** veri (bölüm 06'daki sağlam
   seçim).
5. Üç doğruluğu **tek satırda yan yana** yazdır: taban çizgi, ağaç, KNN.
6. Ağaç taban çizgiyi geçiyorsa `better`, geçmiyorsa `worse` yazdır.
7. Hangi model daha iyi? `knn` ya da `tree` yazdır.

**Beklenen çıktı:**

```
0.7 0.8 0.92
better
knn
```

**Ağaç taban çizgiyi geçiyor** (0.80'e karşı 0.70) — yani öğrendiği bir şey
var.

**Ama KNN'e kaybediyor** (0.92). Bu, ağaçların kötü olduğu anlamına
gelmiyor; **bu veriye** daha az uyduğu anlamına geliyor.

Sebebi ağacın çalışma biçiminde: ağaç basamaklı kurallar kuruyor
(`visits <= 18.5` gibi). Sınır düzgün ve eğriyse, basamaklarla taklit etmek
zorunda kalıyor ve her basamakta biraz kaybediyor.

Bölüm 05'te tersini görmüştük: araba verisinde ağacın hatası 64, doğrusal
regresyonunki 16.5'ti. Orada da veri doğrusaldı ve ağaç basamaklarla
uğraşıyordu.

**Alınacak ders: model seçimi bir ölçüm işi.** Hangisinin kazanacağı verinin
şekline bağlı ve bunu önceden bilmenin yolu yok. Ağacın kendine ait
avantajları var — sonraki alıştırmalarda göreceksin.
