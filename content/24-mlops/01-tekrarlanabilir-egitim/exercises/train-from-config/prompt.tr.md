`train(config)` fonksiyonunu yaz. Sonucu etkileyen her şey `config` sözlüğünden gelsin:

- `make_customers(config["rows"], seed=config["data_seed"])` ile veriyi üret, `to_xy` ile çevir.
- `train_test_split`'e `test_size=config["test_share"]` ve `random_state=config["split_seed"]` ver.
- `RandomForestClassifier`'a `n_estimators=config["n_estimators"]` ve `random_state=config["model_seed"]` ver.
- Test doğruluğunu üç basamağa yuvarlayıp döndür.

Fonksiyonun içinde sayı yazma: hepsi `config`'ten.

**Beklenen çıktı:**

```
accuracy: 0.75
again: 0.75
more trees: 0.775
```
