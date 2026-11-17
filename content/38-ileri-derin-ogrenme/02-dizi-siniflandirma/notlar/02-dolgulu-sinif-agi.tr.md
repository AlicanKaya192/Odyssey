Derste bütün diziler aynı uzunluktaydı. Gerçek metinde öyle değil; o zaman
model uzunlukları da almalı ve LSTM'e paketli girdi vermeli. İyi bir model
için iyi bir sınama: **aynı diziye fazladan dolgu eklemek sonucu
değiştirmemeli.**

```python
import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence


class PackedClassifier(nn.Module):
    def __init__(self, vocab, dim=8, hidden=16):
        super().__init__()
        self.emb = nn.Embedding(vocab, dim, padding_idx=0)
        self.lstm = nn.LSTM(dim, hidden, batch_first=True)
        self.head = nn.Linear(hidden, 2)

    def forward(self, x, lengths):
        packed = pack_padded_sequence(self.emb(x), lengths, batch_first=True,
                                      enforce_sorted=False)
        out, (h, c) = self.lstm(packed)
        return self.head(h[-1])


torch.manual_seed(0)
model = PackedClassifier(vocab=20)
seq = torch.tensor([[4, 7, 2]])
short = nn.functional.pad(seq, (0, 2))
long = nn.functional.pad(seq, (0, 9))
lengths = torch.tensor([3])
print(tuple(short.shape), tuple(long.shape))
with torch.no_grad():
    print(torch.allclose(model(short, lengths), model(long, lengths)))
    plain_short = model.lstm(model.emb(short))[1][0]
    plain_long = model.lstm(model.emb(long))[1][0]
    print(torch.allclose(plain_short, plain_long))
```

```text
(1, 5) (1, 12)
True
False
```

- `nn.functional.pad(seq, (0, 2))` son boyutun sonuna 2 tane 0 ekler.
- Paketli modelde 2 ya da 9 dolgu aynı sonucu veriyor (`True`).
- Paketsiz LSTM'in son durumu dolgu sayısına göre değişiyor (`False`):
  grubu kuran kişinin seçtiği boy modelin cevabını değiştiriyor, ki bu bir
  hata.

## Sık yapılan hatalar

| Hata | Belirti | Çare |
|---|---|---|
| `lengths` GPU'da | `pack_padded_sequence` hata verir | Uzunluklar CPU'da `int64` kalır |
| Uzunluk 0 olan dizi | Paketleme hata verir | Boş örnekleri veriden çıkar |
| Çift yönde paketlememek | Geri yön önce dolguyu okur | Her zaman paketle |
| `padding_idx` vermemek | Dolgu vektörü öğrenilir | Paketli modelde zararsız ama maskeli ortalamada sorun olur |
