Veri 600 abone. İki metin sütunu (`city`, `plan`), üç sayısal sütun
(`tenure`, `monthly`, `support`) ve hedef `churn`. Üç sütunda eksik değer
var.

Bölüm 04'te bunu elle yapmıştın: medyanı eğitimden al, testte de onu
kullan, kodlayıcıyı eğitimde `fit` et... Altı adım ve dört tane
"eğitimden" uyarısı.

Bu alıştırmada aynı işi **tek bir nesneye** yaptıracaksın.

**Yapman gerekenler:**

1. Veriyi oku. Eksik değer sayılarını sözlük olarak yazdır.
2. `X` olarak `churn` dışındaki her şeyi, `y` olarak `churn` sütununu al ve
   ayır (`test_size=0.25`, `random_state=42`, `stratify=y`).
3. Bir `ColumnTransformer` kur:
   - **sayısal** sütunlara: medyanla doldur, sonra ölçekle
   - **metin** sütunlarına: en sık değerle doldur, sonra
     `OneHotEncoder(handle_unknown="ignore")`
4. Bunu `LogisticRegression(max_iter=1000)` ile bir `Pipeline`'a bağla ve
   eğit.
5. Taban çizgiyi ve pipeline'ın test doğruluğunu yan yana yazdır
   (üç ondalık).
6. Ön işleme sonrası **sütun sayısını** ve **sütun adlarını** yazdır.

**Beklenen çıktı:**

```
{'city': 24, 'plan': 0, 'tenure': 0, 'monthly': 48, 'support': 30, 'churn': 0}
0.573 0.793
9
['num__tenure', 'num__monthly', 'num__support', 'cat__city_Ankara', 'cat__city_Bursa', 'cat__city_Izmir', 'cat__plan_basic', 'cat__plan_plus', 'cat__plan_pro']
```

**Taban çizgi 0.573, model 0.793.** 22 puanlık gerçek bir kazanç.

Ama bu alıştırmanın konusu skor değil. **Konu, `pipe.fit(X_train,
y_train)` satırının ne yaptığı:**

- Sayısal sütunların medyanını **yalnızca eğitimden** hesapladı
- Metin sütunlarının modunu **yalnızca eğitimden** hesapladı
- Kodlayıcıyı **yalnızca eğitimde** `fit` etti
- Ölçekleyiciyi **yalnızca eğitimde** `fit` etti
- Modeli eğitti

`pipe.predict(X_test)` çağrıldığında hiçbir adım **yeniden öğrenmedi**;
hepsi eğitimde öğrendiğini uyguladı.

**Bölüm 04'ün kuralı — "önce ayır, sonra dokun" — artık bir dikkat
meselesi değil.** Pipeline'ı yanlış sırada çalıştırmanın bir yolu yok.

**Sütun listesine bak:** üç sayısal sütun olduğu gibi kaldı, iki metin
sütunu altı sütuna açıldı (3 şehir + 3 plan). Toplam dokuz. Bu adlar
katsayıları okurken tek doğru kaynak.

**`handle_unknown="ignore"` neden var:** test kümesinde eğitimde
görülmemiş bir şehir çıkarsa `OneHotEncoder` varsayılan olarak **hata
veriyor**. `ignore` o satırın bütün şehir sütunlarını sıfır yapıyor.
Üretimde bu ayar olmadan model ilk beklenmedik değerde çöküyor.
