Doğrusal regresyonun katsayıları soyut. Ağacın kuralları **cümleye
çevrilebiliyor** — ve bu, ağacın en değerli yanı.

**Yapman gerekenler:**

1. Aynı akışı kur ve **`max_depth=2`** ile bir ağaç eğit (`random_state=42`).
2. `export_text` ile kuralları yazdır. Sütun adlarını vermeyi unutma, yoksa
   `feature_0` gibi yazıyor.
3. **Kök bölünmesinin** özelliğini ve eşiğini yan yana yazdır (eşik iki
   ondalık).
4. **Yaprak sayısını ve derinliği** yan yana yazdır.

**Beklenen çıktı:**

```
|--- visits <= 18.50
|   |--- income <= 137500.00
|   |   |--- class: 1
|   |--- income >  137500.00
|   |   |--- class: 0
|--- visits >  18.50
|   |--- income <= 41500.00
|   |   |--- class: 0
|   |--- income >  41500.00
|   |   |--- class: 0
visits 18.5
4 2
```

**Kök soruyu cümleye çevir:** "Bu müşteri ayda 18.5'ten az mı giriyor?"
Ağaç bütün özellikleri ve bütün olası eşikleri deneyip grubu en iyi ayıran
soruyu seçmiş — ve `visits` kazanmış.

**Şimdi alttaki iki yaprağa dikkat et: ikisi de `class: 0`.**

Bölünme etiketi değiştirmiyor. O zaman ağaç neden bölmüş?

**Çünkü ağaç etiketi değil safsızlığı en iyiliyor.** Sol yaprakta 20 kayıt
var ve dağılım 11'e 9 (neredeyse yarı yarıya); sağ yaprakta 75 kayıt var ve
dağılım 74'e 1 (neredeyse saf). İkisinin de çoğunluğu aynı sınıf ama **güven
düzeyleri** bambaşka.

Bu fark `predict_proba` çağırdığında ortaya çıkıyor: soldaki yaprak %55
diyor, sağdaki %99. Yalnızca `predict` kullanan biri bu iki kaydı aynı
sayıyor — oysa biri neredeyse kesin, öteki yazı tura.

**Kural okurken her zaman iki şey birlikte bakılıyor:** kuralın kendisi ve
**kaç kayda dayandığı**. 3 kayıtlık bir yaprağın kuralı genellenebilir bir
bilgi taşımıyor olabilir.
