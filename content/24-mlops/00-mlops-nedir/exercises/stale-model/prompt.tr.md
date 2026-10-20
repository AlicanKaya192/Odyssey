Model 0. ayın müşterileriyle eğitildi ve hazır (`model`). Şimdi onu her ay yeni gelen müşterilerle izle:

- 0'dan 6'ya kadar her ay için `make_customers(1000, seed=99, month=month)` ile o ayın müşterilerini al.
- Doğruluğu ölç, üç basamağa yuvarla ve `month 0 accuracy: 0.813` biçiminde yazdır.
- Doğruluk ilk kez `0.75`'in altına düştüğü ayı hatırla.
- Sonda `alarm at month: N` yazdır; hiç düşmediyse `no alarm`.

**Beklenen çıktı:**

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
