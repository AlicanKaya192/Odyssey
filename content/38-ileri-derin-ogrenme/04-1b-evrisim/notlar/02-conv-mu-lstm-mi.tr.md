İki katman ailesi aynı veriyi farklı biçimde ister; aradaki geçiş tek bir
`transpose`.

```python
import torch
from torch import nn

torch.manual_seed(0)
x = torch.randn(4, 64, 3)
lstm = nn.LSTM(3, 8, batch_first=True)
conv = nn.Conv1d(3, 8, kernel_size=5, padding=2)
out_lstm, _ = lstm(x)
out_conv = conv(x.transpose(1, 2))
print(tuple(out_lstm.shape), tuple(out_conv.shape))
print(tuple(out_conv.transpose(1, 2).shape))
n_lstm = sum(p.numel() for p in lstm.parameters())
print(n_lstm, sum(p.numel() for p in conv.parameters()))
```

```text
(4, 64, 8) (4, 8, 64)
(4, 64, 8)
416 128
```

- `x` LSTM biçiminde `(B, T, D)`: 4 kayıt, 64 adım, 3 eksen.
  `transpose(1, 2)` onu `(B, D, T)` yapar; evrişimin çıkışı da aynı yolla
  geri çevrilebilir.
- `transpose` olmadan `Conv1d` 64'ü kanal sayısı sanar ve "3 kanal
  bekleniyordu" diye hata verir; o hata iyidir. Kötüsü, kanal sayısının
  zaman uzunluğuna tesadüfen eşit olduğu durum: hata yok, sonuç yanlış.

## Hangisini seçmeli?

| | 1B evrişim | LSTM / GRU |
|---|---|---|
| Hesap | Bütün konumlar paralel, hızlı | Adım adım, sıralı |
| Gördüğü | Alıcı alan kadar yerel pencere | İlke olarak bütün geçmiş |
| İyi olduğu | Yerel desen: sıçrama, titreşim, ses olayı | Sıra ve uzun bağımlılık |
| Konum | Deseni her yerde tanır | Konumu durumla taşır |

İkisi birlikte de kullanılır: önce birkaç evrişim katmanı yerel desenleri
çıkarır ve diziyi kısaltır (`stride` ya da havuzlama), sonra bir LSTM bu
kısa özet dizisini okur.
