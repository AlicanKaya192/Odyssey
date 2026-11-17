Gerçek bir projede (örneğin ImageNet'te eğitilmiş bir ResNet ile kedi ve
köpek ayırmak) adımlar derstekinin aynısı, yalnızca gövde daha büyük. Burada
ağırlık indirmemek için `weights=None` yazıyoruz; gerçek projede
`weights=models.ResNet18_Weights.DEFAULT` yazılır ve ağırlık dosyası ilk
kullanımda internetten indirilir.

```python
from torch import nn
from torchvision import models

model = models.resnet18(weights=None)
for p in model.parameters():
    p.requires_grad = False
model.fc = nn.Linear(model.fc.in_features, 2)
trainable = [name for name, p in model.named_parameters() if p.requires_grad]
print(trainable)
print(sum(p.numel() for p in model.parameters() if p.requires_grad))
```

```text
['fc.weight', 'fc.bias']
1026
```

- Önce bütün parametreler donduruluyor, **sonra** yeni `fc` takılıyor: yeni
  katmanın parametreleri varsayılan olarak öğrenilebilir.
- 11 milyonu aşkın parametreden yalnızca 1026'sı eğitiliyor (512 × 2 + 2).
  Birkaç yüz resim bunun için yeter.

Kontrol listesi:

1. Resimleri modelin beklediği gibi hazırla: `weights.transforms()` (boyut,
   kesme, ImageNet ortalaması ve sapması). Gri resimleri RGB'ye çevir.
2. Gövdeyi dondur, yeni baş tak; optimizer'a yalnızca başın parametrelerini
   ver.
3. Eğitirken `model.train()`'den sonra gövdeyi `eval()`'de tut (BatchNorm).
4. Doğrulama doğruluğu durunca istersen gövdenin son aşamasını (`layer4`)
   çözüp küçük öğrenme oranıyla ince ayar yap.
5. Tahminde `model.eval()` ve `torch.no_grad()`.
