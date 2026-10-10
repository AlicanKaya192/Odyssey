## Sık kullanılan scoring adları

| Ad | Ölçü |
|---|---|
| `"accuracy"`, `"balanced_accuracy"` | doğruluk, sınıf başına recall ortalaması |
| `"f1"`, `"precision"`, `"recall"` | iki sınıf, pozitif sınıf 1 |
| `"f1_macro"`, `"f1_weighted"`, `"recall_macro"` | çok sınıf ortalamaları |
| `"roc_auc"`, `"average_precision"` | sıralama (olasılıkla) |
| `"neg_log_loss"`, `"neg_brier_score"` | olasılığın kalitesi |
| `"neg_mean_absolute_error"`, `"neg_root_mean_squared_error"` | regresyon hatası |
| `"r2"`, `"neg_mean_absolute_percentage_error"` | regresyon |

## Ortalama türleri

| `average=` | Ne yapar |
|---|---|
| `None` | her sınıfın değeri ayrı |
| `"macro"` | düz ortalama; küçük sınıf eşit sayılır |
| `"weighted"` | sınıf büyüklüğüyle ağırlıklı |
| `"micro"` | bütün tahminler tek havuzda |
| `"binary"` (iki sınıfta varsayılan) | yalnızca `pos_label` sınıfı |

## make_scorer

| Yazım | Anlamı |
|---|---|
| `make_scorer(f)` | `f(y_true, y_pred)` büyükse iyi |
| `make_scorer(f, greater_is_better=False)` | küçükse iyi; scorer eksi döndürür |
| `make_scorer(f, response_method="predict_proba")` | `f`'ye olasılık gider |
| `make_scorer(fbeta_score, beta=2)` | ek ayarlar `f`'ye geçer |
| `get_scorer("roc_auc")` | adı scorer nesnesine çevirir |

## Eşik

| Yazım | Ne yapar |
|---|---|
| `TunedThresholdClassifierCV(m, scoring=scorer, cv=5)` | eşiği eğitimde, çapraz doğrulamayla seçer; `best_threshold_` |
| `FixedThresholdClassifier(m, threshold=0.2)` | eşiği sabitler |
| `(model.predict_proba(X)[:, 1] >= t).astype(int)` | elle eşik |
