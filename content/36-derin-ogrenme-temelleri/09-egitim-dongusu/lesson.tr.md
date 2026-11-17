# Eğitim Döngüsü

Şimdiye kadarki döngüler tek bir parça kod hâlindeydi ve sonunda test
verisine bir kez bakıyorduk. Gerçek projelerde eğitim döngüsü biraz daha
düzenlidir: bir turu eğiten ve modeli değerlendiren iki fonksiyon, her
turda **doğrulama** (validation) verisine bakmak, kayıpları bir geçmişte
tutmak ve en iyi modeli saklamak. Bu bölümde bu iskeleti kuracağız; modülün
geri kalanında hep bunu kullanacağız.

## Üç parça veri

Veriyi üçe bölüyoruz: **eğitim** (model bununla öğrenir), **doğrulama**
(turlar boyunca modeli izleriz, karar veririz) ve **test** (en sonda bir
kez, gerçek başarıyı ölçmek için).

```python
import copy

import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader, random_split
from dl_data import make_table

x_np, y_np = make_table(1000)
data = TensorDataset(torch.from_numpy(x_np), torch.from_numpy(y_np))
train_set, val_set, test_set = random_split(
    data, [600, 200, 200], generator=torch.Generator().manual_seed(0))
train_loader = DataLoader(train_set, batch_size=32, shuffle=True,
                          generator=torch.Generator().manual_seed(0), num_workers=0)
val_loader = DataLoader(val_set, batch_size=100, num_workers=0)
test_loader = DataLoader(test_set, batch_size=100, num_workers=0)
print(len(train_loader), len(val_loader), len(test_loader))
```

```text
19 2 2
```

Eğitim yükleyicisi karıştırıyor; doğrulama ve test yükleyicileri karıştırmıyor
(Dataset ve DataLoader bölümündeki kural).

## İki fonksiyon: eğit ve değerlendir

```python
def train_one_epoch(model, loader, optimizer, loss_fn):
    model.train()
    total, count = 0.0, 0
    for xb, yb in loader:
        optimizer.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        optimizer.step()
        total += loss.item() * len(yb)
        count += len(yb)
    return total / count


def evaluate(model, loader, loss_fn):
    model.eval()
    total, correct, count = 0.0, 0, 0
    with torch.no_grad():
        for xb, yb in loader:
            logits = model(xb)
            total += loss_fn(logits, yb).item() * len(yb)
            correct += (logits.argmax(dim=1) == yb).sum().item()
            count += len(yb)
    return total / count, correct / count
```

<figure class="fig">
  <div class="versus">
    <div><h5><code>train_one_epoch</code></h5><code>model.train()</code>, bütün kümelerde dört adım, ortalama eğitim kaybı.</div>
    <div><h5><code>evaluate</code></h5><code>model.eval()</code> ve <code>torch.no_grad()</code>; güncelleme yok; ortalama kayıp ve doğruluk.</div>
  </div>
  <figcaption>Eğitim ve değerlendirme ayrı fonksiyonlarda: biri modeli değiştirir, öteki yalnızca ölçer.</figcaption>
</figure>

- Kayıp ve doğruluk örnek sayısıyla ağırlıklandırılıyor: kümelerin
  ortalamasının ortalaması, son küme küçükken yanlış olur.
- `evaluate` modeli `eval()` kipine alıyor; `train_one_epoch` her çağrıda
  geri `train()`'e alıyor. Kip değişimini unutmak, Dropout ve BatchNorm
  kullanan modellerde sessiz hata demek.

## Döngü, geçmiş ve en iyi model

```python
torch.manual_seed(3)
model = nn.Sequential(nn.Linear(6, 32), nn.ReLU(), nn.Linear(32, 3))
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
loss_fn = nn.CrossEntropyLoss()
history, best_loss, best_state, best_epoch = [], float("inf"), None, 0

for epoch in range(1, 31):
    train_loss = train_one_epoch(model, train_loader, optimizer, loss_fn)
    val_loss, val_acc = evaluate(model, val_loader, loss_fn)
    history.append((train_loss, val_loss))
    if val_loss < best_loss:
        best_loss, best_epoch = val_loss, epoch
        best_state = copy.deepcopy(model.state_dict())
    if epoch % 10 == 0:
        print(epoch, round(train_loss, 2), round(val_loss, 2), round(100 * val_acc, 1))

model.load_state_dict(best_state)
test_loss, test_acc = evaluate(model, test_loader, loss_fn)
print("best", best_epoch, "test", round(100 * test_acc, 1))
```

```text
10 0.21 0.36 87.5
20 0.21 0.41 86.5
30 0.18 0.43 85.5
best 5 test 84.0
```

- Her turda eğitim kaybı ve doğrulama kaybı geçmişe yazılıyor; ikisini
  yan yana görmek modelin nasıl gittiğini anlatıyor (ikinci not).
- Doğrulama kaybı en düşük olduğu anda modelin **durumunu**
  (`state_dict`, bütün parametrelerin bir sözlüğü) kopyalıyoruz.
  `copy.deepcopy` şart: kopyalamazsak sözlük modelle birlikte değişmeye
  devam eder.
- Eğitim bitince en iyi duruma geri dönüp test verisine **bir kez**
  bakıyoruz. En iyi tur 5, test doğruluğu %84.
- Dikkat: eğitim kaybı 30 tur boyunca düşerken doğrulama kaybı erken
  turlardan sonra **yükseliyor**. Model eğitim verisini ezberlemeye
  başladı (aşırı öğrenme). En iyi durumu saklamak bizi bundan korudu; bir
  sonraki bölüm aşırı öğrenmenin kendisini ele alıyor.

<figure class="fig">
  <div class="flow">
    <span class="node">Eğitim<br><small>öğren</small></span><span class="arrow">→</span>
    <span class="node">Doğrulama<br><small>izle, seç</small></span><span class="arrow">→</span>
    <span class="node">En iyi durum<br><small>state_dict</small></span><span class="arrow">→</span>
    <span class="node acc">Test<br><small>bir kez</small></span>
  </div>
  <figcaption>Kararlar (hangi tur, hangi ayar) doğrulamayla verilir; test en sona, dokunulmadan kalır.</figcaption>
</figure>

## Neden doğrulama ayrı?

En iyi turu **test** kaybına bakarak seçseydik, test verisi de modeli
seçmek için kullanılmış olurdu. O zaman test sonucu iyimser çıkar: model,
test verisine göre ayarlanmıştır. Makine öğrenmesi patikasındaki kural
aynı: kararlar doğrulama verisiyle, nihai ölçüm hiç dokunulmamış test
verisiyle.

## Özet

- Veri üçe bölünür: eğitim, doğrulama, test.
- `train_one_epoch` (`model.train()`, dört adım) ve `evaluate`
  (`model.eval()`, `torch.no_grad()`) ayrı fonksiyonlar.
- Ortalamalar örnek sayısıyla ağırlıklandırılır.
- Her turda doğrulama ölçülür; en iyi `state_dict` `copy.deepcopy` ile
  saklanır, sonunda yüklenip test bir kez ölçülür.
