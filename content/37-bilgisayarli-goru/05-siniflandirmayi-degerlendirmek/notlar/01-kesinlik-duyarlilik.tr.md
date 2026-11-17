Üç sınıflı küçük bir örnekte bütün ölçüleri elle çıkarıp scikit-learn ile
karşılaştıralım.

| Ölçü | Soru | Matristen |
|---|---|---|
| Kesinlik | "c" dediklerimin kaçı c? | köşegen ÷ sütun toplamı |
| Duyarlılık | Gerçek c'lerin kaçını buldum? | köşegen ÷ satır toplamı |
| F1 | İkisi birden iyi mi? | `2 · k · d / (k + d)` |

```python
import torch
from sklearn.metrics import f1_score

y_true = torch.tensor([0, 0, 0, 0, 0, 0, 1, 1, 2, 2])
y_pred = torch.tensor([0, 0, 0, 0, 0, 1, 1, 0, 2, 1])
counts = torch.bincount(y_true * 3 + y_pred, minlength=9).reshape(3, 3)
correct = counts.diag().float()
precision = correct / counts.sum(dim=0)
recall = correct / counts.sum(dim=1)
f1 = 2 * precision * recall / (precision + recall)
print(counts.tolist())
print([round(v, 3) for v in precision.tolist()])
print([round(v, 3) for v in recall.tolist()])
print(round(f1.mean().item(), 3), round(f1_score(y_true, y_pred, average="macro"), 3))
print(round(f1_score(y_true, y_pred, average="weighted"), 3))
```

```text
[[5, 1, 0], [1, 1, 0], [0, 1, 1]]
[0.833, 0.333, 1.0]
[0.833, 0.5, 0.5]
0.633 0.633
0.713
```

- Elle hesaplanan F1'lerin ortalaması scikit-learn'ün `macro` F1'iyle aynı.
- `weighted` F1 daha yüksek: altı örnekli 0 sınıfı iyi tahmin edilmiş ve
  ağırlıklı ortalamada daha çok sayılıyor. Küçük sınıflardaki başarısızlığı
  görmek istiyorsan `macro`'ya bak.
- Bir sınıf hiç tahmin edilmezse sütun toplamı 0 olur ve kesinlik `0 / 0`
  çıkar (`nan`). scikit-learn bu durumda uyarı verip 0 yazar.
