# 1B Evrişim

Bilgisayarlı Görü modülünde evrişim (convolution) bir görüntünün üstünde
kayan küçük bir çekirdekti (kernel): her konumda aynı ağırlıklarla yerel bir
desen arar. Aynı fikir tek boyutta da çalışır: çekirdek bir **zaman
dizisinin** üstünde kayar. Sensör sinyali, ses, kalp ritmi kaydı ya da
kelime gömmeleri dizisi bu yolla okunabilir.

1B evrişimin LSTM'e göre iki büyük farkı var: bütün konumlar **aynı anda**
hesaplanır (LSTM adım adım bekler) ve ağ bir deseni **nerede olursa
olsun** tanır. Bu bölümde bir sensör kaydında ani bir arızayı yakalayan
küçük bir 1B evrişimli ağ eğitiyoruz.

## `nn.Conv1d`: şekiller

```python
import torch
from torch import nn

torch.manual_seed(0)
conv = nn.Conv1d(in_channels=1, out_channels=4, kernel_size=5)
x = torch.randn(2, 1, 64)
print(conv(x).shape)
print(nn.Conv1d(1, 4, 5, padding=2)(x).shape)
print(nn.Conv1d(1, 4, 5, stride=2)(x).shape)
print(conv.weight.shape, sum(p.numel() for p in conv.parameters()))
```

```text
torch.Size([2, 4, 60])
torch.Size([2, 4, 64])
torch.Size([2, 4, 30])
torch.Size([4, 1, 5]) 24
```

- Girdi `(B, C, T)`: grup, **kanal**, zaman. Kanal her adımdaki sayı
  sayısı (tek sensör 1, üç eksenli ivmeölçer 3). Dikkat: LSTM `(B, T, D)`
  istiyordu, `Conv1d` kanalı **önde** ister.
- Dolgusuz, adım 1: çıkış uzunluğu `64 − 5 + 1 = 60`. `padding=2` iki uca
  ikişer sıfır ekler, uzunluk 64 kalır. `stride=2` çekirdeği ikişer
  kaydırır, uzunluk yarıya iner: `(64 − 5) // 2 + 1 = 30`.
- Ağırlık `(çıkış kanalı, giriş kanalı, çekirdek)` = `(4, 1, 5)`; 20
  ağırlık + 4 yanlılık = 24 parametre. Dizinin uzunluğu parametre sayısını
  hiç etkilemez.

## Elle bir çekirdek

Çekirdeği kendimiz verelim: `[-1, 1]` her konumda "sonraki değer eksi bu
değer" hesaplar, yani **değişimi** bulur.

```python
diff = nn.Conv1d(1, 1, kernel_size=2, bias=False)
with torch.no_grad():
    diff.weight[:] = torch.tensor([[[-1.0, 1.0]]])
signal = torch.tensor([[[0.0, 0.0, 1.0, 3.0, 3.0, 1.0, 0.0]]])
print(diff(signal).tolist())
```

```text
[[[0.0, 1.0, 2.0, 0.0, -2.0, -1.0]]]
```

Sinyal yükselirken çıkış pozitif, düşerken negatif, düzken sıfır. PyTorch'un
evrişimi çekirdeği ters çevirmeden kaydırır (matematikte buna çapraz
ilinti, cross-correlation, denir); öğrenilen çekirdekte bu fark önemsizdir.
Eğitimde ağ kendi çekirdeklerini böyle bulur: biri sıçramaya, biri
titreşime duyarlı olur.

## Veri: sensör pencereleri

`make_sensor` 64 adımlık sensör pencereleri üretiyor: sağlam pencere
dalga ve gürültü; arızalı pencerede **rastgele bir yerde** kısa, sert bir
sıçrama ve titreşim var.

```python
from dl_data import make_sensor

xs, ys = make_sensor(400, length=64, seed=7)
x = torch.from_numpy(xs).unsqueeze(1)
y = torch.from_numpy(ys)
x_train, y_train, x_test, y_test = x[:300], y[:300], x[300:], y[300:]
print(x.shape, y.sum().item(), len(y))
```

```text
torch.Size([400, 1, 64]) 119 400
```

`unsqueeze(1)` kanal boyutunu ekler: `(400, 64)` → `(400, 1, 64)`.
Pencerelerin 119 tanesi arızalı.

## Model: evrişim, ReLU, en büyüğü almak

```python
class FaultNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv1d(1, 8, kernel_size=5, padding=2), nn.ReLU(),
            nn.Conv1d(8, 8, kernel_size=5, padding=2), nn.ReLU(),
            nn.AdaptiveMaxPool1d(1))
        self.head = nn.Linear(8, 2)

    def forward(self, x):
        return self.head(self.features(x).squeeze(-1))


def fit(model, epochs=15):
    loader = torch.utils.data.DataLoader(
        torch.utils.data.TensorDataset(x_train, y_train), batch_size=32, shuffle=True,
        generator=torch.Generator().manual_seed(0))
    opt = torch.optim.Adam(model.parameters(), lr=0.01)
    for epoch in range(epochs):
        model.train()
        for xb, yb in loader:
            opt.zero_grad()
            nn.functional.cross_entropy(model(xb), yb).backward()
            opt.step()
    model.eval()
    with torch.no_grad():
        return (model(x_test).argmax(dim=1) == y_test).float().mean().item()


torch.manual_seed(0)
cnn_acc = fit(FaultNet())
print(round(cnn_acc, 2), cnn_acc > 0.9)
```

```text
0.99 True
```

- `nn.AdaptiveMaxPool1d(1)` her kanalın bütün zaman boyunca **en büyük**
  değerini alır: `(B, 8, 64)` → `(B, 8, 1)`. "Sıçrama dedektörü bu
  pencerenin herhangi bir yerinde öttü mü?" sorusunun cevabı. Arızanın yeri
  önemsizleşir.
- Ağ testte %99 doğru. Bu bilgisayarda eğitim birkaç saniye
  sürdü.

## Konumu bilen ama deseni bilmeyen

Karşılaştırma için 64 değeri doğrudan alan doğrusal bir model eğitelim:

```python
class Flat(nn.Module):
    def __init__(self):
        super().__init__()
        self.head = nn.Linear(64, 2)

    def forward(self, x):
        return self.head(x.squeeze(1))


torch.manual_seed(0)
flat_acc = fit(Flat())
print(round(flat_acc, 1), flat_acc < cnn_acc)
```

```text
0.7 True
```

Doğrusal model her konum için ayrı bir ağırlık öğrenir; sıçrama her
pencerede başka yerde olduğu için tutarlı bir ağırlık bulamaz ve
%70 civarında kalır. Evrişim aynı çekirdeği her konumda
kullandığı için deseni bir kez öğrenir ve her yerde tanır.

## Özet

- `nn.Conv1d` girdisi `(B, C, T)`: kanal önde. LSTM'den gelen
  `(B, T, D)`'yi `x.transpose(1, 2)` ile çevir.
- Çıkış uzunluğu `(T + 2·dolgu − çekirdek) // adım + 1`; parametre sayısı
  dizi uzunluğuna bağlı değil.
- Çekirdek her konumda aynı: desen nerede olursa olsun tanınır.
  `AdaptiveMaxPool1d(1)` ile "herhangi bir yerde var mı" sorusu sorulur.
- Bütün konumlar aynı anda hesaplanır; uzun dizilerde LSTM'den çok daha
  hızlıdır.
