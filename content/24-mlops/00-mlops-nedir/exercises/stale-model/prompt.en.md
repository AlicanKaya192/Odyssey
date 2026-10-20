The model was trained on month 0's customers and is ready (`model`). Now monitor it with the new customers who arrive each month:

- For every month from 0 to 6, get that month's customers with `make_customers(1000, seed=99, month=month)`.
- Measure the accuracy, round it to three digits and print it as `month 0 accuracy: 0.813`.
- Remember the first month in which the accuracy drops below `0.75`.
- At the end print `alarm at month: N`; if it never dropped, print `no alarm`.

**Expected output:**

```
month 0 accuracy: 0.813
month 1 accuracy: 0.82
month 2 accuracy: 0.777
month 3 accuracy: 0.782
month 4 accuracy: 0.674
month 5 accuracy: 0.682
month 6 accuracy: 0.686
alarm at month: 4
```
