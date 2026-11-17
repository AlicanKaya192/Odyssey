Sınıflar dengesizse doğruluk yanıltır. 100 resmin 5'inde kusur olan bir
üretim hattı düşünelim. Hiçbir şeye bakmadan hep "kusur yok" diyen bir
model:

```python
import torch

y = torch.tensor([1] * 5 + [0] * 95)
always_no = torch.zeros(100, dtype=torch.long)
accuracy = (always_no == y).float().mean().item()
found = ((always_no == 1) & (y == 1)).sum().item()
recall = found / (y == 1).sum().item()
print(round(accuracy, 2), recall)
```

```text
0.95 0.0
```

%95 doğruluk, ama aradığımız beş kusurun hiçbirini bulmuyor (duyarlılık 0).
Böyle bir problemde:

- Ölçü olarak nadir sınıfın **duyarlılığı**, **kesinliği** ve **F1**'i
  raporlanır; doğruluk tek başına verilmez.
- Karışıklık matrisine mutlaka bakılır.
- Eğitimde kayba sınıf ağırlığı vermek (`nn.CrossEntropyLoss(weight=...)`)
  ya da nadir sınıfı daha sık örneklemek (`WeightedRandomSampler`) yardımcı
  olabilir.

Bu modülün şekil ve rakam verileri dengeli; nesne algılama ve bölütleme
bölümlerinde dengesizlik yeniden karşımıza çıkacak (resmin çoğu arka plan).
