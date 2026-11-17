`scale_with_train(values, split)` bütün seriyi ölçeklesin ama ortalamayı ve
standart sapmayı **yalnızca ilk `split` değerden** alsın (`statistics.mean`,
`statistics.pstdev`): `(v - mean) / std`. Sonucu 3 basamakla döndürsün.

**Beklenen çıktı:**

```
[-1.225, 0.0, 1.225, 2.449, 3.674]
```
