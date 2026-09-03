Pipeline `GridSearchCV` ile doğrudan çalışıyor — ve yalnızca modelin
değil, **ön işlemenin** ayarları da aranabiliyor.

**Yapman gerekenler:**

1. Veriyi hazırla, ayır ve pipeline'ı kur
   (`LogisticRegression(max_iter=1000)`).
2. `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` kur.
3. İki parametreli bir ızgara tanımla:
   - `prepare__num__impute__strategy`: `["median", "mean"]`
   - `model__C`: `[0.01, 0.1, 1, 10]`
4. `GridSearchCV` ile ara (`scoring="accuracy"`). Her nokta için tek satır
   yazdır: **strateji, C, CV ortalaması** (üç ondalık).
5. En iyi ayarları (strateji ve C) ve o ayarın CV skorunu yazdır.
6. Son satırda **aramanın test doğruluğu** ile **ayarsız pipeline'ın test
   doğruluğunu** yan yana yazdır.

**Beklenen çıktı:**

```
median 0.01 0.711
mean 0.01 0.704
median 0.1 0.74
mean 0.1 0.74
median 1 0.738
mean 1 0.744
median 10 0.736
mean 10 0.736
mean 1 0.744
0.793 0.793
```

**Izgaranın anahtar biçimi bu bölümün en çok karıştırılan yeri:**

```
prepare__num__impute__strategy
   |     |      |        |
   |     |      |        +-- SimpleImputer'in parametresi
   |     |      +----------- ColumnTransformer icindeki adim
   |     +------------------ ColumnTransformer'in bolumu
   +------------------------ Pipeline'daki adim
```

Her seviye **iki alt çizgiyle** ayrılıyor. Tek alt çizgi yazarsan
`GridSearchCV` "böyle bir parametre yok" diyor.

**Doldurma stratejisi artık bir hiperparametre.** Eskiden "medyan mı
ortalama mı" diye düşünüp bir tanesini seçiyordun; şimdi ölçüyorsun.

**Sonuca gelince — dürüst kısım burası.**

En iyi ayar `mean` ve `C=1`, CV skoru 0.744. Varsayılan (`median`, `C=1`)
0.738 veriyor. **Kazanç 0.006.**

**Son satır daha da açık: 0.793 ve 0.793.** Arama sonucu seçilen ayarla
ayarsız pipeline test kümesinde **birebir aynı** skoru veriyor.

Yani sekiz nokta tarandı, kırk model eğitildi ve **hiçbir şey
değişmedi.**

**Bu bir başarısızlık değil, bir bilgi.** Bu veride ne `C` ne doldurma
stratejisi önemli; iyileşme başka yerden gelmeli — daha çok veri, daha
iyi özellikler ya da farklı bir model. Bunu ölçmeden bilemezdin.

**Ve bir uyarı:** `best_score_` (0.744) son rapor değil. O sayı eğitim
tarafındaki çapraz doğrulamadan geliyor ve **sekiz nokta arasından en
iyisi seçildiği için** iyimser. Son rapor test kümesinde: 0.793.
