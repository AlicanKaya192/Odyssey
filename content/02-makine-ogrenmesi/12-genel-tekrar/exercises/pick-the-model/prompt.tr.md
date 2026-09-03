Dört model ailesi öğrendin: doğrusal, KNN, ağaç tabanlı ve topluluk.
Hangisi bu veriye uygun?

**Cevap ölçümden geliyor** — ve bu bölümde doğru **ölçüyü** seçmek de senin
işin.

**Yapman gerekenler:**

1. Veriyi hazırla ve ayır (`followup_calls` yok, `stratify=y`).
2. `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` kur.
3. Dört modeli sırayla ele al:
   - `logreg` — `LogisticRegression(max_iter=1000)`
   - `knn` — `KNeighborsClassifier(n_neighbors=15)`
   - `forest` — `RandomForestClassifier(n_estimators=200, random_state=42)`
   - `boosting` — `GradientBoostingClassifier(random_state=42)`
4. Her biri için tek satır yazdır: **ad, CV ortalama precision'ı, CV
   yayılımı, test ROC AUC'si, test ortalama precision'ı** (üç ondalık).
   Çapraz doğrulamada `scoring="average_precision"` kullan.
5. Ortalama precision'ın **taban çizgisini** yazdır (pozitif oranı).
6. Son satırda CV kazananını yazdır.

**Beklenen çıktı:**

```
logreg 0.542 0.04 0.724 0.462
knn 0.406 0.065 0.672 0.344
forest 0.429 0.043 0.662 0.309
boosting 0.455 0.026 0.71 0.411
0.195
logreg
```

**Neden doğruluk değil ortalama precision?** İkinci alıştırmada gördün:
taban çizgi 0.805 ve dört model de onun civarında doğruluk verecek.
Doğruluk bu problemde **hiçbir modeli diğerinden ayırt edemiyor** — bölüm
09'daki "yayılımı sıfıra yakın ölçü kararlı değil, kör" dersi.

Ortalama precision azınlık sınıfına duyarlı ve taban çizgisi **0.195**.
0.542 bunun yaklaşık üç katı.

**Sonuç sezginin tersi: en basit model kazanıyor.** Lojistik regresyon hem
CV'de (0.542) hem testte (0.462) önde. Orman 0.429, artırma 0.455, KNN
0.406.

Bu, birinci alıştırmadaki araba verisiyle aynı ders: **karmaşıklık kendi
başına bir avantaj değil.** Sekiz özellik ve 600 eğitim satırıyla,
topluluk yöntemlerinin öğreneceği fazladan bir yapı yok.

**Yayılımlara bakmayı unutma:** logreg 0.040, artırma 0.026. Aradaki
0.087'lik ortalama farkı yayılımların iki katından büyük, yani gerçek bir
fark — bölüm 08'de öğrendiğin kontrol.

**Ve ROC AUC ile ortalama precision'ın farkına dikkat:** logreg için 0.724
ve 0.462. Aynı model, aynı olasılıklar. Bölüm 09'da ölçtüğün gibi, ROC
dengesiz veride iyimser çıkıyor.
