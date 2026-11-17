Görüntü aramada her resmin gömmesi bir kez hesaplanıp saklanır; arama
sırasında yalnızca sorgu resminin gömmesi hesaplanır. Basit bir dizin:

```python
import torch
import torch.nn.functional as F

torch.manual_seed(0)
vectors = F.normalize(torch.randn(1000, 64), dim=1)
names = [f"img{i}.png" for i in range(1000)]
torch.save({"vectors": vectors, "names": names}, "index.pt")

index = torch.load("index.pt", weights_only=True)
query = index["vectors"][42] + 0.01 * torch.randn(64)
scores = index["vectors"] @ F.normalize(query, dim=0)
best = scores.topk(3).indices.tolist()
print(best[0], index["names"][best[0]])
print(index["vectors"].shape, len(best))
```

```text
42 img42.png
torch.Size([1000, 64]) 3
```

- Burada gömmeler rastgele; gerçekte ağın gövdesinden gelir. Sorgu, 42.
  resmin biraz bozulmuş hâli: en yakın sonuç 42.
- `weights_only=True` sözlük, liste ve metin gibi sade türleri de okuyor.
- Bin resimde bir matris çarpımı yeter. Milyonlarca resimde bütün vektörlere
  tek tek bakmak yavaşlar; o ölçekte **yaklaşık en yakın komşu** arayan
  özel kütüphaneler ve vektör veri tabanları kullanılır. Fikir aynı:
  normalleştirilmiş gömmeler arasında en büyük kosinüs.
- Ağ değişirse (yeniden eğitilirse) eski gömmeler geçersiz olur; dizin
  yeniden hesaplanır.
