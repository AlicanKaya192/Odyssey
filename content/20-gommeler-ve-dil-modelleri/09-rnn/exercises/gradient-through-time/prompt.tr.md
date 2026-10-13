Tek sayılık bir RNN: `h_0 = 0`, `h_t = tanh(w · h_{t-1} + x_t)`.
`gradient_through_time(w, xs)` son durumun önceki durumlara göre türevini
döndürsün: önce `1.0` (son durumun kendisine göre), sonra geriye doğru her
adımda bir öncekini `w · (1 − h_t²)` ile çarparak, `h_0`'a kadar. 4
basamak.

**Beklenen çıktı:**

```
[1.0, 0.496, 0.24, 0.1041, 0.0219]
[1.0, 0.1721, 0.0344, 0.0119, 0.01]
```
