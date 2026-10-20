Güvenilen referans veriden bir şema çıkaran `infer_schema(rows, numeric, categorical, margin)` fonksiyonunu yaz:

- `numeric` listesindeki her sütun için en küçük (`low`) ve en büyük (`high`) değeri bul. Aralığa her iki uçtan `margin * (high - low)` kadar **pay** bırak. Bu sütunlarda değer negatif olamaz: alt sınır 0'ın altına inerse 0 yaz (`max(0.0, ...)`). İki sınırı da iki basamağa yuvarla: `{"min": ..., "max": ...}`.
- `categorical` listesindeki her sütun için görülen değerlerin **sıralı** listesi: `{"allowed": [...]}`.
- Önce sayısal sütunlar, sonra kategorik sütunlar, verilen sırayla sözlüğe eklensin.

**Beklenen çıktı:**

```
monthly_fee {'min': 1.1, 'max': 63.41}
usage_hours {'min': 0.0, 'max': 74.09}
plan {'allowed': ['basic', 'pro']}
```
