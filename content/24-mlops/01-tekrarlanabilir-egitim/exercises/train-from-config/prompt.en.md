Write the function `train(config)`. Everything that affects the result should come from the `config` dictionary:

- Produce the data with `make_customers(config["rows"], seed=config["data_seed"])` and convert it with `to_xy`.
- Give `train_test_split` `test_size=config["test_share"]` and `random_state=config["split_seed"]`.
- Give `RandomForestClassifier` `n_estimators=config["n_estimators"]` and `random_state=config["model_seed"]`.
- Return the test accuracy rounded to three digits.

Write no numbers inside the function: they all come from `config`.

**Expected output:**

```
accuracy: 0.75
again: 0.75
more trees: 0.775
```
