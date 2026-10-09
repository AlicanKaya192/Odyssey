## Yöntemler

| Yöntem | Çeşitlilik nereden? | scikit-learn |
|---|---|---|
| Bagging | önyükleme örnekleri | `BaggingClassifier` |
| Rastgele orman | önyükleme + bölmede rastgele özellik alt kümesi | `RandomForestClassifier` |
| Aşırı rastgele ağaçlar | rastgele eşikler de | `ExtraTreesClassifier` |

## Ayarlar

| Ayar | Etkisi |
|---|---|
| `n_estimators` | ağaç sayısı; çok olması zarar vermez, yavaşlatır |
| `max_features` | bölmede bakılan özellik sayısı; sınıflandırmada `"sqrt"` |
| `max_depth`, `min_samples_leaf` | tek ağaçların karmaşıklığı |
| `oob_score=True` | torba dışı doğrulama |

## Ne zaman?

- Tablo verisinde güçlü, az ayarla iyi çalışan bir model gerektiğinde.
- Ölçekleme gerekmez; doğrusal olmayan ilişkileri ve etkileşimleri öğrenir.
- Eksileri: tek ağacın okunabilirliği kaybolur; çok ağaç bellek ve tahmin
  süresi ister.

## Sık hatalar

- Ağacın kendi `feature_importances_`'ını kesin sanmak: çok değerli
  (sürekli) özellikleri kayırabilir; permütasyon önemi daha güvenilir.
- OOB ile test sonucunu karıştırmak: OOB eğitim verisinden gelir; nihai
  ölçüm yine ayrı test setiyle.
- Rastgele ormanda `max_features=None` bırakmak: bagging'e döner, ağaçlar
  benzeşir.
