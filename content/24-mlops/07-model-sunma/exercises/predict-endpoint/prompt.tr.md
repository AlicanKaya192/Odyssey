`POST /predict` uç noktasını yaz. Girdi bir `Customer` modeli:

- `tenure`: tam sayı, 1–72
- `monthly_fee`: ondalıklı, 5–100
- `support_calls`: tam sayı, 0–10
- `usage_hours`: ondalıklı, 0–100
- `plan`: yalnızca `"basic"` ya da `"pro"`

Cevap: `{"churn_probability": ..., "model_version": VERSION}`; olasılık `churn_probability(...)` ile hesaplanıp üç basamağa yuvarlanmış. Kurala uymayan istek `422` almalı (bunu Pydantic kendisi yapar).
