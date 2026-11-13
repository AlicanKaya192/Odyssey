Dört model ailesi öğrendin: doğrusal, KNN, ağaç tabanlı ve topluluk.
Hangisi bu veriye uygun?

**Cevap ölçümden geliyor** — ve bu bölümde doğru **ölçüyü** seçmek de senin
işin.

**Yapman gerekenler:**

1. Veriyi hazırla ve ayır (`followup_calls` yok, `stratify=y`). Metin
   sütunlarını `OneHotEncoder(handle_unknown="ignore", drop="if_binary")`
   ile kodla: iki değerli sütunlar (`sex`, `smoker`) tek sütun olur. İki
   değerli bir sütunu iki sütuna açmak aynı bilgiyi iki kez verir.
2. `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` kur.
3. Dört modeli sırayla ele al:
   - `logreg` — `LogisticRegression(max_iter=1000)`
   - `knn` — `KNeighborsClassifier(n_neighbors=15)`
   - `forest` — `RandomForestClassifier(n_estimators=200, min_samples_leaf=30, random_state=42)`
     (`min_samples_leaf=30` her yaprakta en az 30 satır bırakıyor. Çok küçük
     yapraklarda iki ayrım tam eşit puan alabiliyor ve bu eşitlik işlemciye
     göre farklı bozuluyor; büyük yapraklarla sonuç her bilgisayarda aynı.)
   - `boosting` — `GradientBoostingClassifier(random_state=42)`
4. Her biri için tek satır yazdır: **ad, CV ortalama precision'ı, CV
   yayılımı, test ROC AUC'si, test ortalama precision'ı** (üç ondalık).
   Çapraz doğrulamada `scoring="average_precision"` kullan.
5. Ortalama precision'ın **taban çizgisini** yazdır (pozitif oranı).
6. Son satırda CV kazananını yazdır.

**Beklenen çıktı:**

```
logreg 0.541 0.038 0.723 0.46
knn 0.379 0.025 0.637 0.299
forest 0.518 0.067 0.709 0.39
boosting 0.462 0.024 0.71 0.411
0.195
logreg
```

**Neden doğruluk değil ortalama precision?** İkinci alıştırmada gördün:
taban çizgi 0.805 ve dört model de onun civarında doğruluk verecek.
Doğruluk bu problemde **hiçbir modeli diğerinden ayırt edemiyor** — bölüm
09'daki "yayılımı sıfıra yakın ölçü kararlı değil, kör" dersi.

Ortalama precision azınlık sınıfına duyarlı ve taban çizgisi **0.195**.
0.541 bunun yaklaşık üç katı.

**Sonuç sezginin tersi: en basit model kazanıyor.** Lojistik regresyon hem
CV'de (0.541) hem testte (0.46) önde. Orman 0.518, artırma 0.462, KNN
0.379.

Bu, birinci alıştırmadaki araba verisiyle aynı ders: **karmaşıklık kendi
başına bir avantaj değil.** Sekiz özellik ve 600 eğitim satırıyla,
topluluk yöntemlerinin öğreneceği fazladan bir yapı yok.

**Yayılımlara bakmayı unutma:** logreg 0.038, artırma 0.024. Aradaki
0.079'luk ortalama farkı yayılımların iki katından büyük, yani gerçek bir
fark — bölüm 08'de öğrendiğin kontrol. Orman ise logreg'e yakın (0.518) ama
yayılımı 0.067: aradaki 0.023'lük fark yayılımın çok altında, CV ikisini
ayıramıyor. Testte logreg önde (0.46'ya 0.39).

**Ve ROC AUC ile ortalama precision'ın farkına dikkat:** logreg için 0.723
ve 0.46. Aynı model, aynı olasılıklar. Bölüm 09'da ölçtüğün gibi, ROC
dengesiz veride iyimser çıkıyor.
