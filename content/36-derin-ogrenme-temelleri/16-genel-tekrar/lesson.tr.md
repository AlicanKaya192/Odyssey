# Genel Tekrar

Derin Öğrenmenin Temelleri modülünün sonuna geldin. Tek bir sayıdan
(tensör) başlayıp türevini otomatik alan, katmanları kendin tanımladığın,
veriyi kümelerle besleyen, aşırı öğrenmeye karşı korunan, öğrenme oranını
plana bağlayan, kaydedilip yeniden yüklenebilen ve hatası ayıklanabilen
eksiksiz bir eğitim düzeneğine geldin. Bu bölüm yolu bir kez daha yürüyor;
sonunda bütün parçaların birlikte çalıştığı tek bir örnek var.

<figure class="fig">
  <div class="flow">
    <span class="node">Tensör<br><small>00–03</small></span><span class="arrow">→</span>
    <span class="node">Model<br><small>04–06</small></span><span class="arrow">→</span>
    <span class="node">Öğrenme<br><small>07–09</small></span><span class="arrow">→</span>
    <span class="node">Sağlamlık<br><small>10–12</small></span><span class="arrow">→</span>
    <span class="node acc">Kullanım<br><small>13–15</small></span>
  </div>
  <figcaption>Modülün yolu: sayılarla hesap, model kurmak, eğitmek, eğitimi sağlamlaştırmak, modeli kullanmak.</figcaption>
</figure>

## 1. Tensörler ve türev (Bölüm 0–3)

| İş | Araç |
|---|---|
| Tensör kurmak | `torch.tensor`, `zeros`, `randn`, `arange`; `dtype`, `shape` |
| Şekil değiştirmek | `view`, `reshape`, `unsqueeze`, `squeeze`, `permute` |
| Hesap | öğe öğe işlemler, `@` (matris çarpımı), yayınlama, `sum(dim=...)` |
| Türev | `requires_grad=True`, `backward()`, `.grad`, `torch.no_grad()`, `detach()` |

Yayınlama, şekiller sağdan hizalanınca 1 olan boyutu uzatır; tutmazsa hata
verir. `backward()` gradyanı `.grad`'a **ekler**.

## 2. Model kurmak (Bölüm 4–6)

| İş | Araç |
|---|---|
| Elle gradyan inişi | `w -= lr * w.grad` (`no_grad` içinde), sonra `w.grad.zero_()` |
| Katmanlar | `nn.Linear`, `nn.Sequential`, kendi `nn.Module` sınıfın, `parameters()` |
| Aktivasyon | `ReLU` (gizli katmanlarda), `Sigmoid`, `Softmax` (yalnızca olasılık gerekince) |
| Kayıp | `MSELoss` (regresyon), `CrossEntropyLoss` (sınıflandırma, logits ister), `BCEWithLogitsLoss` |

Çıkışta softmax yok, `CrossEntropyLoss` onu kendisi uygular.

## 3. Öğrenmek (Bölüm 7–9)

| İş | Araç |
|---|---|
| Optimizer | `SGD` (+`momentum`), `Adam`; `zero_grad`, `backward`, `step` |
| Veri | `Dataset` (`__len__`, `__getitem__`), `TensorDataset`, `DataLoader(batch_size, shuffle)` |
| Döngü | tur ve küme döngüsü, `model.train()` / `model.eval()`, doğrulama kaybı |
| Seçim | en iyi doğrulama turunun `copy.deepcopy(state_dict())` kopyası |

## 4. Sağlamlaştırmak (Bölüm 10–12)

| İş | Araç |
|---|---|
| Aşırı öğrenmeye karşı | `Dropout`, `weight_decay`, erken durdurma, daha çok veri |
| Başlatma ve normalizasyon | `kaiming_normal_`, `BatchNorm1d`, `LayerNorm` |
| Öğrenme oranı | `StepLR`, `CosineAnnealingLR`, `LinearLR`, `ReduceLROnPlateau` |
| Büyük gradyan | `nn.utils.clip_grad_norm_` (`backward` ile `step` arasında) |

## 5. Kullanmak (Bölüm 13–15)

| İş | Araç |
|---|---|
| Kaydetmek | `torch.save(model.state_dict(), yol)`; kontrol noktasında optimizer da |
| Yüklemek | aynı modeli kur, `load_state_dict(torch.load(yol, weights_only=True))` |
| Hata ayıklamak | şekil dökümü, başlangıç kaybı `log(sınıf)`, tek kümeyi ezberletmek, `.grad` dökümü |
| Değerlendirmek | doğruluk, karışıklık matrisi, sınıf başına doğruluk |

## Hepsi bir arada

Tablo verisinde (3 sınıf) modülün bütün parçaları tek bir düzenekte: türler,
başlangıç kaybı denetimi, BatchNorm ve dropout'lu model, Adam + kosinüs
planı, gradyan kırpma, erken durdurma, en iyi ağırlıkların kaydı ve güvenli
yükleme:

```python
import copy
import math

import torch
from dl_data import make_table
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

x_np, y_np = make_table(1200)
X, Y = torch.from_numpy(x_np).float(), torch.from_numpy(y_np).long()
train, val, test = slice(0, 800), slice(800, 1000), slice(1000, 1200)


def make_model():
    torch.manual_seed(0)
    return nn.Sequential(nn.Linear(6, 32), nn.BatchNorm1d(32), nn.ReLU(),
                         nn.Dropout(0.2), nn.Linear(32, 3))


model, loss_fn = make_model(), nn.CrossEntropyLoss()
model.eval()
with torch.no_grad():
    start = loss_fn(model(X[train]), Y[train]).item()
print("start", round(start, 1), round(math.log(3), 1))

loader = DataLoader(TensorDataset(X[train], Y[train]), batch_size=32,
                    shuffle=True, generator=torch.Generator().manual_seed(0))
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=40)
best_loss, best_epoch, waited = math.inf, 0, 0
for epoch in range(1, 41):
    model.train()
    for xb, yb in loader:
        optimizer.zero_grad()
        loss_fn(model(xb), yb).backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
    scheduler.step()
    model.eval()
    with torch.no_grad():
        val_loss = loss_fn(model(X[val]), Y[val]).item()
    if val_loss < best_loss:
        best_loss, best_epoch, waited = val_loss, epoch, 0
        torch.save(copy.deepcopy(model.state_dict()), "best.pt")
    else:
        waited += 1
        if waited == 5:
            break
print("stop", epoch, "best", best_epoch)

final = make_model()
final.load_state_dict(torch.load("best.pt", weights_only=True))
final.eval()
with torch.no_grad():
    hits = final(X[test]).argmax(dim=1) == Y[test]
print("test", round(100 * hits.float().mean().item(), 1))
```

```text
start 1.2 1.1
stop 8 best 3
test 87.0
```

- Başlangıç kaybı (1,2) `log 3 ≈ 1,1`'e yakın: türler ve
  başlatma sağlıklı.
- Eğitim 8. turda durdu; en iyi doğrulama kaybı
  3. turdaydı, sonraki beş tur onu geçemedi. Son turun
  değil, o turun ağırlıkları diskten güvenli kipte yüklendi.
- Test doğruluğu %87,0. Kod kısa değil, ama artık her satırın
  neden orada olduğunu ve çıkarılırsa neyin bozulacağını biliyorsun.

## Sırada ne var

Bu modülde modeller hep düz bir sayı listesi aldı: 64 piksel ya da 6
özellik. Bir sonraki modül **Bilgisayarlı Görü**: resmin iki boyutlu
yapısını kullanan evrişimli ağlar, hazır modellerle aktarımlı öğrenme ve
nesne algılama. Bu modülde kurduğun eğitim döngüsü orada da aynen
kullanılıyor; değişen yalnızca modelin içi.
