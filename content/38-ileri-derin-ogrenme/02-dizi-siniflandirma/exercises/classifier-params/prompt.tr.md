`classifier_params(vocab, dim, hidden)` dersteki modelin üç katmanını kursun:
`nn.Embedding(vocab, dim)`, `nn.LSTM(dim, hidden, batch_first=True)` ve
`nn.Linear(hidden, 2)`. Üçünün toplam parametre sayısını döndürsün.

**Beklenen çıktı:**

```
1778
570
```
