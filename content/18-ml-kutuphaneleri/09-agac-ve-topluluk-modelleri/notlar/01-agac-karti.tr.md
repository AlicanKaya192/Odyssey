## Sınıflar

| Sınıf | Fikir | `NaN` |
|---|---|---|
| `DecisionTreeClassifier` / `Regressor` | tek ağaç, okunabilir | kabul eder |
| `RandomForestClassifier` / `Regressor` | önyükleme + rastgele sütun, oylama | kabul eder |
| `ExtraTreesClassifier` / `Regressor` | kesim noktaları da rastgele | kabul eder |
| `GradientBoostingClassifier` / `Regressor` | ağaçlar sırayla artıklara | etmez |
| `HistGradientBoostingClassifier` / `Regressor` | hızlı boosting, büyük veri | kabul eder |
| `BaggingClassifier(estimator)` | herhangi bir modeli torbalar | modele bağlı |
| `VotingClassifier(list, voting="soft")` | olasılık ortalaması | modele bağlı |
| `StackingClassifier(list, final_estimator)` | tahminlerin üstüne model | modele bağlı |

## Ağacı sınırlayan ayarlar

| Ayar | Etki |
|---|---|
| `max_depth` | en fazla kaç soru üst üste |
| `min_samples_leaf` | yaprakta en az kaç satır |
| `max_leaf_nodes` | en fazla kaç yaprak |
| `ccp_alpha` | budama bedeli; `cost_complexity_pruning_path` adayları verir |

## Orman ayarları

| Ayar | Etki |
|---|---|
| `n_estimators` | ağaç sayısı; çok olması aşırı öğrenme yapmaz, yalnızca yavaşlatır |
| `max_features` | her bölünmede bakılan sütun (`"sqrt"` varsayılan) |
| `oob_score=True` | torba dışı doğruluk, `oob_score_` |
| `n_jobs=-1` | bütün çekirdekler |
| `class_weight="balanced"` | dengesiz sınıflar |

## Okunacak nitelikler

| Nitelik | Ne |
|---|---|
| `get_n_leaves()`, `get_depth()` | ağacın boyu |
| `feature_importances_` | saflık artışı (eğitimden, yanlı) |
| `estimators_` | ormandaki ağaçlar |
| `export_text(tree)`, `plot_tree(tree)` | ağacı yazmak / çizmek |
