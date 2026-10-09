## Hangi yöntem ne zaman?

| Yöntem | Ne yapar | scikit-learn | Ne zaman? |
|---|---|---|---|
| Eğitim/test ayrımı | bir kez böler | `train_test_split` | veri çok büyükse, hızlı bir ilk bakış |
| k-katlı | `k` parça, her biri bir kez test | `KFold`, `cross_val_score` | çoğu durumda varsayılan |
| Katmanlı k-katlı | sınıf oranlarını korur | `StratifiedKFold` | sınıflandırma, özellikle dengesiz sınıflar |
| Birini dışarıda bırak | `k = n` | `LeaveOneOut` | çok küçük veri |
| Gruplu k-katlı | aynı grubun örnekleri aynı katta | `GroupKFold` | aynı hastanın, kullanıcının birden çok satırı |
| Zaman serisi ayrımı | eğitim hep testten önce | `TimeSeriesSplit` | zamana bağlı veri |
| Permütasyon testi | etiketi karıştırıp tekrar ölçer | `permutation_test_score` | sonuç şanstan iyi mi? |
| Bootstrap | yerine koyarak örnekler | — (ALG 2 · 12) | güven aralığı |

## Sık hatalar

- **Önce ölçekleyip sonra bölmek:** ortalama test verisini de görmüş olur.
  Her kat için ölçekleyici yalnızca o katın eğitim kısmıyla `fit` edilir
  (scikit-learn'de `Pipeline` bunu kendiliğinden yapar).
- **Aynı kişinin satırlarını iki tarafa dağıtmak:** model kişiyi ezberler,
  test sonucu şişer. Gruplu ayrım gerekir.
- **Zaman serisini karıştırmak:** model geleceği görerek geçmişi tahmin eder.
- **Hiperparametreyi test setine bakarak seçmek:** test seti artık "görülmüş"
  olur; seçim çapraz doğrulamayla, son ölçüm ayrı bir test setiyle yapılır.
