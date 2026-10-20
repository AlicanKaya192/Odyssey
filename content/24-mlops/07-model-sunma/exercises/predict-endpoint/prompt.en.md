Write the `POST /predict` endpoint. The input is a `Customer` model:

- `tenure`: integer, 1–72
- `monthly_fee`: decimal, 5–100
- `support_calls`: integer, 0–10
- `usage_hours`: decimal, 0–100
- `plan`: only `"basic"` or `"pro"`

The answer: `{"churn_probability": ..., "model_version": VERSION}`; the probability computed with `churn_probability(...)` and rounded to three digits. A request that breaks the rules should get `422` (Pydantic does this itself).
