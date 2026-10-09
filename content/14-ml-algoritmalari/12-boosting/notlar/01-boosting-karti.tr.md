## Yöntemler

| Yöntem | Fikir | Nerede |
|---|---|---|
| AdaBoost | yanlış sınıflananları ağırlaştır, kütükleri oylat | `AdaBoostClassifier` |
| Gradyan artırma | her turda kaybın gradyanına (regresyonda artığa) ağaç | `GradientBoostingRegressor` |
| Histogram tabanlı GB | özellikleri kutulara ayırıp çok hızlı bölme arar | `HistGradientBoostingClassifier` |
| XGBoost, LightGBM, CatBoost | aynı fikir, düzenlileştirme ve büyük veri için hızlandırılmış | ayrı kütüphaneler |

## Ayarlar

| Ayar | Etkisi |
|---|---|
| `n_estimators` | ağaç sayısı; **aşırı uyutabilir**, erken durdurmayla seç |
| `learning_rate` | her ağacın katkısı; küçük → daha çok ağaç, genelde daha iyi |
| `max_depth` | ağaçların derinliği; boosting'de sığ ağaçlar (2–6) |
| `subsample` | her ağaç verinin bir kısmıyla (stokastik GB) |

## Bagging ile karşılaştırma

| | Bagging / rastgele orman | Boosting |
|---|---|---|
| Ağaçlar | bağımsız, paralel | sıralı, öncekine bağlı |
| Ağaç tipi | derin (düşük yanlılık) | sığ (zayıf öğrenici) |
| Ağaç sayısı artınca | aşırı uyumaz | aşırı uyabilir |
| Ne düşer | varyans | yanlılık (ve varyans) |

## Sık hatalar

- Ağaç sayısını eğitim hatasıyla seçmek: hep "daha çok" der.
- Büyük öğrenme oranı: birkaç ağaçta ezber.
- Gürültülü etiketlerde AdaBoost: yanlış etiketlere ağırlık yığar.
