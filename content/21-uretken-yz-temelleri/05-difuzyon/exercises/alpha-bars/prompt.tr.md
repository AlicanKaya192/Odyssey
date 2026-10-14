`alpha_bars(T, start, end, ts)` `T` adımlık doğrusal bir gürültü takvimi
kursun (`np.linspace(start, end, T)`), `alpha = 1 - beta` ve
`alpha_bar = np.cumprod(alpha)` hesaplasın ve `ts` listesindeki adımların
`alpha_bar` değerlerini 4 basamağa yuvarlanmış `float` listesi olarak
döndürsün.

**Beklenen çıktı:**

```
[0.9999, 0.9545, 0.6399, 0.0056]
[0.9999, 0.0786, 0.0]
```
