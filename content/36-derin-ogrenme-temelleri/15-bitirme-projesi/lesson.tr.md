# Bitirme: Uçtan Uca Sınıflandırıcı

Bu modülde parçaları tek tek gördük: tensörler, otomatik türev, `nn.Module`,
kayıp, optimizer, `DataLoader`, eğitim döngüsü, düzenlileştirme,
normalizasyon, öğrenme oranı planı, kaydetme ve hata ayıklama. Bu bölümde
hepsini tek bir işte birleştiriyoruz: el yazısı rakamları (8 × 8 piksel)
tanıyan bir sınıflandırıcıyı baştan sona kuruyoruz. Her adım önceki
bölümlerden birine dayanıyor; yeni bir şey yok, yalnızca hepsi bir arada.

Plan:

<figure class="fig">
  <div class="flow">
    <span class="node">Veri ve bölme</span><span class="arrow">→</span>
    <span class="node">Model ve denetim</span><span class="arrow">→</span>
    <span class="node">Eğitim</span><span class="arrow">→</span>
    <span class="node">Test</span><span class="arrow">→</span>
    <span class="node acc">Kaydet</span>
  </div>
  <figcaption>Her kutu önceki bölümlerden birinin konusu.</figcaption>
</figure>

## 1. Veri ve bölme

Veri, giriş bölümündeki rakamlar: 1797 resim, her biri 64 piksel, piksel
değerleri 0–16. Pikselleri 16'ya bölerek 0–1 arasına alıyoruz (ölçek,
Doğrusal Model bölümü). Sonra veriyi bir kez, sabit tohumla karıştırıp üçe
bölüyoruz: eğitim (%60), doğrulama (%20, erken durdurma ve seçim için) ve
test (%20, yalnızca en sonda bir kez):

```python
import copy
import math

import torch
from sklearn.datasets import load_digits
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

digits = load_digits()
X = torch.tensor(digits.data, dtype=torch.float32) / 16
Y = torch.tensor(digits.target)
order = torch.randperm(len(X), generator=torch.Generator().manual_seed(0))
train_idx, val_idx, test_idx = order[:1078], order[1078:1437], order[1437:]
print(len(train_idx), len(val_idx), len(test_idx))
print(torch.bincount(Y[train_idx]).tolist())
```

```text
1078 359 360
[116, 110, 113, 110, 100, 108, 104, 110, 105, 102]
```

- Üç küme ayrık: aynı resim iki kümede birden yok.
- Eğitim kümesinde her rakamdan 100–116 örnek var; sınıflar aşağı yukarı
  dengeli, doğruluk anlamlı bir ölçü.
- `float32` ve `long` türleri baştan doğru (Hata Ayıklama bölümü).

## 2. Model ve ilk denetim

```python
class DigitNet(nn.Module):
    def __init__(self, hidden=64, p=0.2):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(64, hidden), nn.BatchNorm1d(hidden), nn.ReLU(),
            nn.Dropout(p), nn.Linear(hidden, 10),
        )

    def forward(self, x):
        return self.layers(x)


torch.manual_seed(0)
model = DigitNet()
loss_fn = nn.CrossEntropyLoss()
print(sum(p.numel() for p in model.parameters()))
model.eval()
with torch.no_grad():
    start = loss_fn(model(X[train_idx]), Y[train_idx]).item()
print(round(start, 1), round(math.log(10), 1))
```

```text
4938
2.3 2.3
```

- Model 4938 parametreli: 64 → 64 → 10, arada BatchNorm ve dropout.
- Çıkışta softmax yok; `CrossEntropyLoss` logits istiyor.
- Başlangıç kaybı `log 10`'la aynı: başlatma ve kayıp sağlıklı.

## 3. Eğitim

Adam, kosinüs planı, her turun sonunda doğrulama kaybı; doğrulama kaybı 5
tur iyileşmezse dur ve **en iyi turun** ağırlıklarına dön:

```python
loader = DataLoader(TensorDataset(X[train_idx], Y[train_idx]), batch_size=32,
                    shuffle=True, generator=torch.Generator().manual_seed(0))
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=30)
best_loss, best_state, best_epoch, waited = math.inf, None, 0, 0
for epoch in range(1, 31):
    model.train()
    for xb, yb in loader:
        optimizer.zero_grad()
        loss_fn(model(xb), yb).backward()
        optimizer.step()
    scheduler.step()
    model.eval()
    with torch.no_grad():
        val_loss = loss_fn(model(X[val_idx]), Y[val_idx]).item()
    if val_loss < best_loss:
        best_loss, best_epoch, waited = val_loss, epoch, 0
        best_state = copy.deepcopy(model.state_dict())
    else:
        waited += 1
        if waited == 5:
            break
print(epoch, best_epoch, round(best_loss, 3))
model.load_state_dict(best_state)
```

```text
16 11 0.056
```

- Eğitim 16. turda durdu; en iyi doğrulama kaybı
  11. turdaydı (0,056).
- `copy.deepcopy` şart: `state_dict()` ağırlıkların kendisine bakar, kopya
  alınmazsa eğitim sürdükçe "en iyi" kayıt da değişir (Eğitim Döngüsü
  bölümünün notu).
- Her turda `model.train()` ve `model.eval()` arasında geçiş: dropout ve
  BatchNorm iki kipte farklı çalışıyor.

## 4. Test

Test kümesine yalnızca şimdi, bir kez bakıyoruz:

```python
model.eval()
with torch.no_grad():
    pred = model(X[test_idx]).argmax(dim=1)
truth = Y[test_idx]
accuracy = (pred == truth).float().mean().item()
print(round(100 * accuracy, 1), (pred != truth).sum().item())

matrix = torch.zeros(10, 10, dtype=torch.long)
for t, p in zip(truth.tolist(), pred.tolist()):
    matrix[t, p] += 1
off = matrix.clone()
off.fill_diagonal_(0)
t, p = divmod(off.argmax().item(), 10)
print(f"{t} -> {p}: {off[t, p].item()}")
```

```text
96.7 12
3 -> 8: 4
```

- 360 test resminin 12 tanesi yanlış: doğruluk %96,7.
- **Karışıklık matrisi** (confusion matrix) `matrix[gerçek, tahmin]`
  sayar; köşegen doğrular, geri kalanı hatalar. En sık hata 3'ü 8 sanmak
  (4 kez).
- Doğruluk tek bir sayı; matris modelin **nerede** zorlandığını gösteriyor.

## 5. Kaydet ve yeniden yükle

```python
torch.save(model.state_dict(), "digits.pt")
fresh = DigitNet()
fresh.load_state_dict(torch.load("digits.pt", weights_only=True))
fresh.eval()
with torch.no_grad():
    same = torch.equal(fresh(X[test_idx]).argmax(dim=1), pred)
print(same)
```

```text
True
```

Kaydedilen yalnızca state_dict; yükleyen program `DigitNet` sınıfını kodla
kuruyor ve sayıları güvenli kipte okuyor. Yüklenen model test kümesinde
aynı tahminleri verdi.

## Özet

- Veri bir kez, sabit tohumla üçe bölünür; test kümesine en sonda bir kez
  bakılır.
- Eğitimden önce iki denetim: türler ve başlangıç kaybı.
- Eğitim döngüsü: `train()`/`eval()` geçişi, plan, erken durdurma, en iyi
  ağırlıkların kopyası.
- Doğruluğun yanında karışıklık matrisi.
- Kaydetmek: state_dict + `weights_only=True`.
