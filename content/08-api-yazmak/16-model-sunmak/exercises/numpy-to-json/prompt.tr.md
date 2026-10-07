`POST /predict` her istekte `500` veriyor: cevaba NumPy değerleri konmuş.

**Yapman gereken:** cevabı JSON'a çevrilebilir yap:

- `label`: Python `int`'i
- `probabilities`: üç olasılığın listesi, her biri `round(..., 3)`

- `5.1, 3.5, 1.4, 0.2` → `{"label": 0, "species": "setosa", "probabilities": [...]}`
