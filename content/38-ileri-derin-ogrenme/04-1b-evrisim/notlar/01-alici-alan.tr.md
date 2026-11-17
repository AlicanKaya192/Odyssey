Bir çıkış konumunun girdinin kaç adımını "gördüğüne" **alıcı alan**
(receptive field) denir. Tek bir 5'lik çekirdek 5 adım görür. İki 5'lik
evrişim üst üste gelince ikincinin her konumu birincinin 5 konumunu, onlar da
girdinin toplam 9 adımını görür. Hesaplamak yerine autograd ile ölçebiliriz:
tek bir çıkışın türevi girdinin yalnızca gördüğü adımlarda sıfırdan farklı
olur.

```python
import torch
from torch import nn


def receptive_field(model, length=64):
    x = torch.randn(1, 1, length, requires_grad=True)
    out = model(x)
    out[0, 0, out.shape[-1] // 2].backward()
    return int((x.grad[0, 0] != 0).sum())


torch.manual_seed(0)
one = nn.Conv1d(1, 1, 5, padding=2)
two = nn.Sequential(nn.Conv1d(1, 1, 5, padding=2), nn.Conv1d(1, 1, 5, padding=2))
dilated = nn.Sequential(nn.Conv1d(1, 1, 5, padding=2),
                        nn.Conv1d(1, 1, 5, padding=4, dilation=2))
print(receptive_field(one), receptive_field(two), receptive_field(dilated))
```

```text
5 9 13
```

- Bir katman 5, iki katman 9 adım görüyor: her yeni `k`'lık katman alana
  `k − 1` ekler.
- **Genişletilmiş evrişim** (dilated convolution, `dilation=2`) çekirdeğin
  elemanları arasına boşluk koyar: aynı 5 ağırlık 9 adıma yayılır. Aynı
  parametreyle iki katman 13 adım görüyor.
- Arızayı yakalamak için alıcı alanın arıza deseninin boyu kadar olması
  yeter (derste 8 adım). Uzun bağımlılıklar için genişletme katman katman
  ikiye katlanır (1, 2, 4, 8, ...): alan katman sayısıyla üstel büyür.

`AdaptiveMaxPool1d(1)` sonrası ağın bütün pencereyi görmesi alıcı alanla
ilgili değil: her konum yine yerel bir pencereye bakar, havuzlama yalnızca
o yerel cevapların en büyüğünü seçer.
