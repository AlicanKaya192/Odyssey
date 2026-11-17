`lstm_shapes(input_size, hidden, layers, bidirectional, batch, steps)` verilen
ayarlarla `batch_first=True` bir `nn.LSTM` kursun, `(batch, steps,
input_size)` şeklinde sıfırlardan bir girdiyi ondan geçirsin ve `out`, `h`,
`c` şekillerini liste olarak döndürsün.

**Beklenen çıktı:**

```
[[2, 5, 3], [1, 2, 3], [1, 2, 3]]
[[2, 5, 6], [4, 2, 3], [4, 2, 3]]
```
