Bir model dosyası tek başına nereden geldiğini söylemez. Yanına küçük bir **model kartı** yazılır.

`model_card(rows, accuracy)` fonksiyonunu yaz. Şu dört anahtarı olan bir sözlük döndürsün:

- `"rows"`: müşteri sayısı
- `"churn_rate"`: `churned` değeri `1` olanların oranı, üç basamağa yuvarlanmış; liste boşsa `0.0`
- `"features"`: `ml_data.py`'deki `FEATURES` listesi
- `"accuracy"`: verilen doğruluk, üç basamağa yuvarlanmış

Her `rows` öğesi bir müşteri sözlüğü.

**Beklenen çıktı:**

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
