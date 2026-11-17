ResNet her evrişimden sonra `BatchNorm2d` kullanıyor. Kısaca ne yaptığına ve
eğitim ile tahminde neden farklı davrandığına bakalım:

```python
import torch
from torch import nn

torch.manual_seed(0)
bn = nn.BatchNorm2d(4)
x = torch.randn(8, 4, 5, 5) * 3 + 10
y = bn(x)
print(abs(y.mean().item()) < 1e-5, round(y.std().item(), 2))
print(sum(p.numel() for p in bn.parameters()))
print([name for name, _ in bn.named_buffers()])
bn.eval()
print(abs(bn(x).mean().item()) > 1)
```

```text
True 1.0
8
['running_mean', 'running_var', 'num_batches_tracked']
True
```

- **Eğitim kipinde** her kanalı **o yığının** ortalaması ve sapmasıyla
  normalleştiriyor: ortalaması 10 olan girdi ortalaması 0 olan çıktıya
  dönüştü.
- İki öğrenilen parametresi var (kanal başına bir ölçek, bir kaydırma): 4
  kanalda 8. Ağ isterse normalleştirmeyi geri alabilsin diye.
- Ayrıca **tampon** (buffer) tutuyor: `running_mean`, `running_var`. Bunlar
  öğrenilmiyor; eğitim boyunca yığın istatistiklerinin kayan ortalaması.
- **Değerlendirme kipinde** yığının değil, bu kayan ortalamaların
  kullanılıyor. Tek bir adımdan sonra kayan ortalama henüz gerçek ortalamaya
  (10) ulaşmadığı için çıktının ortalaması sıfırdan uzak.

Sonuç: BatchNorm'lu bir ağı tahmin ederken `model.eval()` unutulursa her
yığının kendi istatistiği kullanılır; tek resimle tahmin bile yanlış çıkabilir.
Transfer öğrenmede bu fark yeniden karşımıza çıkacak.
