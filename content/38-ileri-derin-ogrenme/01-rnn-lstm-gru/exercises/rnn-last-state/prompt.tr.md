`rnn_last_state(xs, w_ih, w_hh)` yanlılıksız bir RNN'i elle yürütsün: gizli
durum `w_ih`'nin satır sayısı kadar sıfırla başlar, her adımda
`h = tanh(x @ w_ih.T + h @ w_hh.T)`. Son gizli durumu 3 basamakla liste olarak
döndürsün.

**Beklenen çıktı:**

```
[0.0, 0.462]
[0.432, 0.462]
```
