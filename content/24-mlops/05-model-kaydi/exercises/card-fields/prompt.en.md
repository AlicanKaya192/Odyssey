A model card is given as a dictionary. Write the function `missing_fields(card)`: return, in list order, the fields of the `REQUIRED` list that are **missing** from the card or **empty**.

Values that count as empty: `""`, `None`, `{}`, `[]`.

**Expected output:**

```
['data', 'limitations']
[]
```
