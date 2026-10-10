## Aynı ayar, iki ad

| Anlamı | HistGradientBoosting | LightGBM |
|---|---|---|
| ağaç sayısı | `max_iter` (100) | `n_estimators` (100) |
| öğrenme hızı | `learning_rate` (0,1) | `learning_rate` (0,1) |
| yaprak sayısı | `max_leaf_nodes` (31) | `num_leaves` (31) |
| derinlik | `max_depth` (sınırsız) | `max_depth` (-1, sınırsız) |
| yaprakta en az satır | `min_samples_leaf` (20) | `min_child_samples` (20) |
| L2 cezası | `l2_regularization` | `reg_lambda` |
| satır/sütun örneklemi | yok | `subsample` + `subsample_freq`, `colsample_bytree` |
| erken durdurma | `early_stopping="auto"`, `validation_fraction` | `eval_X`, `eval_y`, `lgb.early_stopping(n)` |
| kategorik | `categorical_features="from_dtype"` | `category` türü kendiliğinden |
| mesajları sustur | — | `verbose=-1` |

## Okunacak nitelikler

| Nitelik | Ne |
|---|---|
| `n_iter_` (Hist) / `best_iteration_` (LGBM) | erken durdurmada kullanılan ağaç |
| `is_categorical_` (Hist) | hangi sütun kategorik sayıldı |
| `feature_importances_` (LGBM) | bölme sayısı |
| `booster_.feature_importance(importance_type="gain")` | kazanç |
| `evals_result_` (LGBM) | her ağaçtan sonra doğrulama kaybı |

## Ayar sırası

1. Öğrenme hızını küçük tut (0,05–0,1), ağaç sayısını büyük ver, erken
   durdurmayla bıraksın.
2. Karmaşıklığı ayarla: `num_leaves` / `max_leaf_nodes`, `min_child_samples`.
3. Gerekirse örnekleme ve ceza (`subsample`, `colsample_bytree`,
   `reg_lambda`).
4. Bütün aramayı çapraz doğrulamayla; test en sonda bir kez.
