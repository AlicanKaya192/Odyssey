Bir pipeline'ın asıl kazancı tek satırda görünmüyor. Bölüm 05'teki
`cross_val_score`'a pipeline verildiğinde ortaya çıkıyor.

**Yapman gerekenler:**

1. Veriyi hazırla ve ayır. Ön işleyiciyi **üreten bir fonksiyon** yaz
   (her model kendi kopyasını almalı).
2. `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` kur.
3. İki pipeline kur ve sırayla ele al:
   - `logreg` — `LogisticRegression(max_iter=1000)`
   - `forest` — `RandomForestClassifier(n_estimators=200, random_state=42)`
4. Her biri için tek satır yazdır: **ad, CV ortalaması, CV yayılımı, test
   doğruluğu** (üç ondalık). Çapraz doğrulamayı **ham `X_train`** ile yap —
   pipeline hazırlığı kendisi yapıyor.
5. Son satırda CV kazananını ve test kazananını yan yana yazdır.

**Beklenen çıktı:**

```
logreg 0.738 0.037 0.793
forest 0.689 0.027 0.753
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

**Yayılımlar da anlamlı:** 0.037 ile 0.027. Aradaki 0.049'luk ortalama
farkı bu yayılımların üstünde, yani gerçek bir fark.
