`churn_auc(c)` terk verisinde pipeline'ın 5 katlı ortalama AUC'sini (3
basamak) döndürüyor. `monthly` sütununda eksik var; başlangıç kodu sayı
sütunlarını yalnızca ölçeklediği için hata alıyor. Sayı parçasını
**medyanla doldur + ölçekle** biçiminde kur
(`make_pipeline(SimpleImputer(strategy="median"), StandardScaler())`).

**Beklenen çıktı:**

```
0.777
0.771
```
