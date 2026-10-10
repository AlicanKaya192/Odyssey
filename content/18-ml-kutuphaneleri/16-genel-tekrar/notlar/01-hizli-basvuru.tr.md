## Bir modelin yolu

1. Veriyi ayır: `train_test_split(..., stratify=y)`; test en sona kalır.
2. Ön işlemeyi kur: `ColumnTransformer` + `make_pipeline`; öğrenen her şey
   içeride.
3. Doğrulamayı seç: `StratifiedKFold(shuffle=True)`, gruplar varsa
   `GroupKFold`, zaman varsa `TimeSeriesSplit`.
4. Ölçüyü seç: işin maliyetine uyan `scoring`; gerekirse `make_scorer`.
5. Taban çizgiyle başla: doğrusal model; sonra ağaç / boosting.
6. Ara: `GridSearchCV` / `RandomizedSearchCV`; fark sapmadan küçükse basit
   olanı seç.
7. Eşiği seç: `TunedThresholdClassifierCV`.
8. Testte bir kez ölç; rapora bu sayı girer.
9. Açıkla: permütasyon önemi, kısmi bağımlılık + ICE.
10. Kaydet: model + sürüm + sütunlar + eşik, `compress=3`.

## Sık hatalar ve bölümleri

| Hata | Bölüm |
|---|---|
| Ölçekleyiciyi bütün veride `fit` etmek | scikit-learn API'si, Pipeline |
| `remainder="drop"` ile sessizce kaybolan sütun | ColumnTransformer |
| Özellik seçimini pipeline dışında yapmak | Özellik Seçimi |
| `best_score_`'u rapora yazmak | Hiperparametre Arama |
| Sıralı veride karıştırmadan bölmek, gruplu veride `KFold` | Doğrulama Araçları |
| AUC'ye `predict` vermek, eşiği testte seçmek | Metrikler ve Scorer |
| `max_iter` ile `ConvergenceWarning` susturmak | Doğrusal Modeller |
| `feature_importances_`'a güvenmek | Ağaç ve Topluluk Modelleri |
| Küme numarasıyla doğruluk hesaplamak | Kümeleme ve Boyut İndirgeme |
| Güvenmediğin model dosyasını yüklemek | Model Kaydetme |
| `add_constant`'ı unutmak | statsmodels: OLS |
| Poisson'da `offset`'i unutmak | statsmodels: GLM ve Formüller |
| Erken durdurmayı test verisiyle yapmak | Gradyan Boosting Kütüphaneleri |
| Tam sayı sütunda kısmi bağımlılık | Modeli Açıklamak |

## Bu sürümde değişenler (eski öğreticilerde farklı)

| Eski yazım | Bu sürümde |
|---|---|
| `LogisticRegression(penalty="l1")` | `l1_ratio=1, solver="saga"` |
| `LogisticRegression(penalty=None)` | `C=np.inf` |
| LightGBM `fit(eval_set=[(X, y)])` | `fit(eval_X=X, eval_y=y)` |
| `HDBSCAN(...)` uyarısı | `copy=True` yaz |
