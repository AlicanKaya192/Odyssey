Bir pipeline'ın asıl kazancı tek satırda görünmüyor. Bölüm 05'teki
`cross_val_score`'a pipeline verildiğinde ortaya çıkıyor.

**Yapman gerekenler:**

1. Veriyi hazırla ve ayır. Ön işleyiciyi **üreten bir fonksiyon** yaz
   (her model kendi kopyasını almalı).
2. `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` kur.
3. İki pipeline kur ve sırayla ele al:
   - `logreg` — `LogisticRegression(max_iter=1000)`
   - `forest` — `RandomForestClassifier(n_estimators=200, min_samples_leaf=30, random_state=42)`
     (`min_samples_leaf=30` her yaprakta en az 30 satır bırakıyor. Çok küçük
     yapraklarda iki ayrım tam eşit puan alabiliyor ve bu eşitlik işlemciye
     göre farklı bozuluyor; büyük yapraklarla sonuç her bilgisayarda aynı.)
4. Her biri için tek satır yazdır: **ad, CV ortalaması, CV yayılımı, test
   doğruluğu** (üç ondalık). Çapraz doğrulamayı **ham `X_train`** ile yap —
   pipeline hazırlığı kendisi yapıyor.
5. Son satırda CV kazananını ve test kazananını yan yana yazdır.

**Beklenen çıktı:**

```
logreg 0.738 0.037 0.793
forest 0.711 0.021 0.733
logreg logreg
```

**Dikkat et: `cross_val_score`'a verdiğin şey ham `X_train`.** Doldurulmamış
eksik değerler, kodlanmamış metin sütunları, ölçeklenmemiş sayılar.

`cross_val_score` beş kat açıyor ve **her katta pipeline'ın bütün
adımlarını baştan eğitiyor.** Birinci katın medyanı, o katın eğitim
kısmından; ikinci katınki ikinci kattan.

**Bunu elle yapmayı dene:** ölçekleyiciyi bir kez `fit_transform` edip
sonucu `cross_val_score`'a verirsen, ölçekleyici bütün eğitim verisini
görmüş olur. Sonra o veri beş kata bölünür ve her katın "doğrulama"
kısmı, ölçekleyicinin zaten gördüğü satırlardan oluşur. **Sessiz bir
sızıntı** — ve kimse fark etmez.

Pipeline bunu **yapısal olarak imkânsız** hâle getiriyor. Üçüncü
alıştırmada bu sızıntının ne kadar büyüyebildiğini ölçeceksin.

**Sonuçlara gelince:** lojistik regresyon her iki sütunda da önde. Bu veri
büyük ölçüde doğrusal — `tenure` arttıkça ayrılma düşüyor, `support`
arttıkça yükseliyor — ve orman bu düzgünlükten faydalanamıyor.

**Yayılımlara da bak:** 0.037 ile 0.021. Aradaki 0.027'lik ortalama farkı
logreg'in yayılımından küçük: CV tek başına kesin bir kazanan söylemiyor.
Test doğruluğu da aynı yönü gösteriyor (0.793'e 0.733); iki ölçü birlikte
logreg'i öne çıkarıyor.
