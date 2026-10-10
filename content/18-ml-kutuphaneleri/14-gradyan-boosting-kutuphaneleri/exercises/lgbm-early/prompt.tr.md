`lgbm_early(patience)` LightGBM'i doğrulama parçasıyla (`eval_X=X_val`,
`eval_y=y_val`) ve `lgb.early_stopping(patience, verbose=False)` geri
çağrısıyla eğitsin; `[best_iteration_, test_skoru]` döndürsün (skor 3
basamak). `eval_set` bu sürümde eskidi, kullanma. Başlangıç kodu 2000 ağacın
hepsini eğitiyor.

**Beklenen çıktı:**

```
[57, 0.828]
[57, 0.828]
```
