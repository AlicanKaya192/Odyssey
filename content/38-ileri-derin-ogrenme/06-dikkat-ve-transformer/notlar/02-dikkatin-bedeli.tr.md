Dikkatin gücü her konumun her konuma bakması; bedeli de bu. Ağırlık
matrisi `(T, T)`: dizi uzunluğu 10 kat artınca matris 100 kat büyür. LSTM'de
ise adım başına iş sabit, toplam iş uzunlukla doğru orantılı.

```python
import torch
from torch import nn

for T in (100, 1000, 10000):
    print(T, T * T)

lstm = nn.LSTM(32, 32, batch_first=True)
block = nn.TransformerEncoderLayer(32, nhead=4, dim_feedforward=64, batch_first=True)
print(sum(p.numel() for p in lstm.parameters()))
print(sum(p.numel() for p in block.parameters()))
```

```text
100 10000
1000 1000000
10000 100000000
8448
8544
```

- 10 000 adımlık bir dizide tek bir başın ağırlık matrisi 100 milyon sayı:
  `float32` ile 400 MB, üstelik her baş ve her örnek için ayrı. Uzun ses ve
  sensör kayıtlarında önce evrişimle diziyi kısaltmak bu yüzden yaygın.
- Parametre sayıları yakın; fark parametrede değil, hesabın uzunlukla nasıl
  büyüdüğünde.

| | LSTM | Transformer |
|---|---|---|
| Uzunlukla iş | Doğru orantılı (T) | Karesiyle (T²) |
| Paralellik | Adımlar sıralı | Bütün konumlar aynı anda |
| Uzak bağımlılık | Durumdan geçerek, zayıflayarak | Tek adımda |
| Sıra bilgisi | Kendiliğinden | Konum gömmesiyle verilir |
| Çok veri olunca | İyileşmesi yavaşlar | Genelde daha iyi ölçeklenir |

Kısa dizilerde ve az veride ikisi yakındır; büyük metin modelleri
Transformer'ın paralelliği sayesinde mümkün oldu.
