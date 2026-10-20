A model file does not say where it came from on its own. A small **model card** is written next to it.

Write the function `model_card(rows, accuracy)`. It returns a dictionary with these four keys:

- `"rows"`: the number of customers
- `"churn_rate"`: the share whose `churned` value is `1`, rounded to three digits; `0.0` if the list is empty
- `"features"`: the `FEATURES` list from `ml_data.py`
- `"accuracy"`: the given accuracy, rounded to three digits

Each item of `rows` is a customer dictionary.

**Expected output:**

```
rows = 500
churn_rate = 0.302
accuracy = 0.813
features:
- tenure
- monthly_fee
- support_calls
- usage_hours
- plan
```
