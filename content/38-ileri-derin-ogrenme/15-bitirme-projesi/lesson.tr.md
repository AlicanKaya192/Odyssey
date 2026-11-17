# Bitirme: Sensör Arıza Algılayıcı

Bir fabrikadaki titreşim sensörleri saniyede bir 64 ölçümlük pencereler
gönderiyor. Arızalı bir makinede pencerenin bir yerinde kısa, sert bir
sıçrama ve titreşim görülüyor. Görevimiz uçtan uca bir algılayıcı:
veriyi tanımak, basit bir kuralla taban çizgisi koymak, 1B evrişimli bir ağ
eğitmek, doğru ölçülerle değerlendirmek ve modeli teslim edilebilir hâle
getirmek. Bu modülde öğrendiklerimizin çoğu burada bir araya geliyor.

<figure class="fig">
<div class="flow">
<span class="node">veri</span><span class="arrow">→</span>
<span class="node">taban kural</span><span class="arrow">→</span>
<span class="node acc">1B evrişim</span><span class="arrow">→</span>
<span class="node">değerlendirme</span><span class="arrow">→</span>
<span class="node ok">teslim paketi</span>
</div>
<figcaption>Projenin adımları. Derin ağ ancak basit kuralı geçerse işe yarar.</figcaption>
</figure>

## Veri

`make_sensor` pencereleri ve 0/1 arıza etiketlerini veriyor. Gerçek
sensörlerin kazancı (gain) birbirinden farklıdır: aynı titreşimi biri iki
kat büyük ölçer. Bunu taklit etmek için her pencereyi 0,5 ile 2 arasında
sabit tohumlu bir kazançla çarpıyoruz.

```python
import json
import numpy as np
import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_sensor

x_np, y_np = make_sensor(600, seed=7)
gain = np.random.default_rng(3).uniform(0.5, 2.0, (600, 1)).astype(np.float32)
x_np = x_np * gain
x, y = torch.tensor(x_np).unsqueeze(1), torch.tensor(y_np)
splits = {"train": slice(0, 400), "val": slice(400, 500), "test": slice(500, 600)}
print(tuple(x.shape), [int(y[s].sum()) for s in splits.values()])
```

```text
(600, 1, 64) [119, 19, 30]
```

- `unsqueeze(1)`: `Conv1d` girdiyi `(grup, kanal, uzunluk)` ister; tek
  kanal ekledik.
- 600 pencerenin 400'ü eğitim, 100'ü doğrulama, 100'ü test; liste her
  bölümdeki arıza sayısı. Arızalar azınlık: eğitimde ve testte yaklaşık üçte
  biri, doğrulamada daha az. Hep "sağlam" diyen bir model testte
  yaklaşık %70 doğru olurdu; doğruluk tek başına yetmeyecek.

## Taban çizgisi: tepe kuralı

Arıza bir sıçrama; en basit kural "penceredeki en büyük mutlak değer bir
eşiği aşıyorsa arıza". Eşiği **doğrulama** verisinde seçip testte ölçüyoruz:

```python
def rule(xs, threshold):
    return (xs.abs().amax(dim=(1, 2)) > threshold).long()


def accuracy(pred, ys):
    return (pred == ys).float().mean().item()


val, test = splits["val"], splits["test"]
candidates = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
best_t = max(candidates, key=lambda t: accuracy(rule(x[val], t), y[val]))
rule_acc = accuracy(rule(x[test], best_t), y[test])
print(best_t, round(rule_acc, 2))
```

```text
3.0 0.93
```

Kural fena değil ama kazanç farkı onu bozuyor: büyük kazançlı sağlam bir
sensörün normal dalgası, küçük kazançlı arızalı bir sensörün sıçramasından
büyük olabiliyor. Bir ağın işi bunu aşmak: sıçramayı değerin büyüklüğünden
değil, **dalganın biçiminden** tanımak.

## 1B evrişimli ağ

```python
def make_net():
    return nn.Sequential(
        nn.Conv1d(1, 16, 5, padding=2), nn.ReLU(), nn.MaxPool1d(2),
        nn.Conv1d(16, 32, 5, padding=2), nn.ReLU(), nn.AdaptiveMaxPool1d(1),
        nn.Flatten(), nn.Linear(32, 2))


def predict(model, xs):
    with torch.no_grad():
        return model(xs).argmax(dim=1)


torch.manual_seed(0)
model = make_net()
opt = torch.optim.Adam(model.parameters(), lr=0.003)
loader = torch.utils.data.DataLoader(
    torch.utils.data.TensorDataset(x[splits["train"]], y[splits["train"]]),
    batch_size=32, shuffle=True, generator=torch.Generator().manual_seed(1))
best_val, best_state = -1.0, None
for epoch in range(15):
    model.train()
    for xb, yb in loader:
        opt.zero_grad()
        F.cross_entropy(model(xb), yb).backward()
        opt.step()
    model.eval()
    val_acc = accuracy(predict(model, x[val]), y[val])
    if val_acc > best_val:
        best_val = val_acc
        best_state = {k: v.clone() for k, v in model.state_dict().items()}
model.load_state_dict(best_state)
print(sum(p.numel() for p in model.parameters()), best_val > 0.95)
```

```text
2754 True
```

- `AdaptiveMaxPool1d(1)`: her kanalın penceredeki en büyük tepkisini alır.
  Sıçrama pencerenin neresinde olursa olsun yakalanır ve ağ farklı
  uzunluktaki pencerelerde de çalışır.
- En iyi doğrulama doğruluğunu veren dönemin ağırlıklarını sakladık
  (`state_dict`'in kopyası) ve sonunda onları yükledik: erken durdurmanın
  basit bir biçimi.

## Değerlendirme

Arıza kaçırmanın bedeli büyük; o yüzden arıza sınıfı için **kesinlik**
(precision: "arıza dediklerimizin ne kadarı gerçekten arıza") ve
**duyarlılık** (recall: "gerçek arızaların ne kadarını yakaladık") ayrı
ayrı ölçülür.

```python
def precision_recall(pred, ys):
    tp = ((pred == 1) & (ys == 1)).sum().item()
    return tp / max(1, (pred == 1).sum().item()), tp / (ys == 1).sum().item()


pred = predict(model, x[test])
precision, recall = precision_recall(pred, y[test])
print(accuracy(pred, y[test]) > rule_acc, precision > 0.9, recall > 0.9)
print(precision_recall(rule(x[test], best_t), y[test])[1] < recall)
```

```text
True True True
True
```

- Ağ testte kuralı geçiyor; kesinlik ve duyarlılık ikisi de 0,9'un üstünde.
- Son satır: kural arızaların daha çoğunu kaçırıyor (duyarlılığı düşük).
  Doğruluk farkı küçük görünse de asıl kazanç burada.

## Teslim paketi

Modeli Dışa Aktarmak bölümündeki gibi: dışa aktarılmış model, açıklama ve
altın çıktı.

```python
batch = torch.export.Dim("batch")
ep = torch.export.export(model, (x[test][:4],), dynamic_shapes=({0: batch},))
torch.export.save(ep, "sensor.pt2")
meta = {"classes": ["healthy", "fault"], "length": 64, "test_recall": recall}
with open("sensor.json", "w") as f:
    json.dump(meta, f)
with torch.no_grad():
    golden = model(x[test][:8])
loaded = torch.export.load("sensor.pt2").module()
print(torch.allclose(loaded(x[test][:8]), golden, atol=1e-5), loaded(x[test]).shape)
```

```text
True torch.Size([100, 2])
```

Paket hazır: `sensor.pt2` sınıf kodu olmadan yükleniyor, altın çıktıyla
denetleniyor ve 100 pencereyi tek çağrıda sınıflandırıyor.

## Özet

- Önce veriyi tanı: sınıf dengesi, doğru bölme (eğitim / doğrulama / test).
- Önce basit bir kural: eşik doğrulamada seçilir, testte bir kez ölçülür.
- 1B evrişim + `AdaptiveMaxPool1d`: sıçramayı yerinden ve kazançtan
  bağımsız tanır.
- En iyi doğrulama dönemini sakla; testi en sona bırak.
- Azınlık sınıfında doğruluk değil kesinlik ve duyarlılık.
- Teslim: dışa aktarılmış model + açıklama + altın çıktı.
