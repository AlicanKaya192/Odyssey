Bir modeli başkasına teslim ederken yalnızca `.pt2` dosyası yetmez. Karşı
taraf şunları da bilmeli: girdi kaç özellik, çıkışın her sütunu hangi sınıf,
ve elindeki dosyanın senin dosyanla **aynı sonucu** verdiği nasıl
doğrulanır. Küçük bir teslim paketi üç dosya: model, açıklama, örnek
girdi–çıktı ("altın" çıktı).

```python
import json
import torch
from torch import nn

torch.manual_seed(0)
model = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 3)).eval()
example = torch.randn(5, 4, generator=torch.Generator().manual_seed(1))
batch = torch.export.Dim("batch")
ep = torch.export.export(model, (example,), dynamic_shapes=({0: batch},))
torch.export.save(ep, "model.pt2")
meta = {"classes": ["low", "mid", "high"], "features": 4}
with torch.no_grad():
    golden = {"input": example.tolist(), "output": model(example).tolist()}
with open("meta.json", "w") as f:
    json.dump(meta, f)
with open("golden.json", "w") as f:
    json.dump(golden, f)
print(sorted(meta), len(golden["output"]))
```

```text
['classes', 'features'] 5
```

- `dynamic_shapes=({0: batch},)`: argüman adı yerine sırayla da
  verilebiliyor; burada tek argümanın 0. boyutu serbest.
- `meta.json` modelin dışındaki bilgiyi taşıyor; `golden.json` sabit bir
  girdi ve modelin ona verdiği çıktı.

Karşı tarafın kodu modelin sınıfını bilmeden yükler, önce altın çıktıyı
denetler, sonra tahmin eder:

```python
loaded = torch.export.load("model.pt2").module()
with open("meta.json") as f:
    meta = json.load(f)
with open("golden.json") as f:
    golden = json.load(f)
out = loaded(torch.tensor(golden["input"]))
print(torch.allclose(out, torch.tensor(golden["output"]), atol=1e-5))
labels = [meta["classes"][i] for i in out.argmax(dim=1).tolist()]
print(len(labels), set(labels) <= set(meta["classes"]))
```

```text
True
5 True
```

- Altın çıktı denetimi "doğru dosya, doğru sürüm, doğru yükleme" üçünü birden
  sınar. Tutmazsa tahmine geçilmez.
- `atol=1e-5`: farklı bir makinede ya da farklı bir PyTorch sürümünde son
  basamaklar değişebilir; birebir eşitlik beklenmez.

Bu modülün tekrarlanabilirlik bölümünde paketi bir tahmin fonksiyonunun
arkasına koyacağız; FastAPI ile REST API Yazmak modülündeki "Bir ML Modelini
Sunmak" bölümü aynı türden bir paketi bir web uç noktasının arkasına
koyuyor.
