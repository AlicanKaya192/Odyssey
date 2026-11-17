# Dataset ve DataLoader

Şimdiye kadar her adımda **bütün** eğitim verisini modele verdik. 1200
küçük rakamda sorun değil; ama yüz binlerce görüntü belleğe sığmaz, sığsa
bile her küçük adım için hepsini işlemek çok yavaştır. Çözüm veriyi küçük
**kümelere** (mini-batch) bölmek: her adımda 32 ya da 64 örnek. PyTorch
bunun için iki parça veriyor: veriye tek tek erişmeyi tanımlayan
**Dataset** ve onu kümeler hâlinde dolaşan **DataLoader**.

## TensorDataset

Veri zaten tensörse en kolay yol `TensorDataset`:

```python
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader, random_split
from sklearn.datasets import load_digits

digits = load_digits()
X = torch.tensor(digits.data, dtype=torch.float32) / 16
y = torch.tensor(digits.target)
data = TensorDataset(X, y)
image, label = data[0]
print(len(data), image.shape, label.item())
```

```text
1797 torch.Size([64]) 0
```

Bir Dataset'in iki işi var: kaç örnek olduğunu söylemek (`len`) ve
`data[i]` ile `i`'nci örneği vermek. `TensorDataset` her örneği
`(girdi, etiket)` çifti olarak veriyor.

## Kendi Dataset sınıfın

Veri tensör değilse (dosyalar, metinler, kendi ürettiğin örnekler) Dataset'i
kendin yazarsın: `torch.utils.data.Dataset`'ten türeyen, `__len__` ve
`__getitem__` yazan bir sınıf. `dl_data.make_shapes` görüntüleri için:

```python
from torch.utils.data import Dataset
from dl_data import make_shapes


class ShapesDataset(Dataset):
    def __init__(self, n, size=16):
        self.images, self.labels = make_shapes(n, size=size)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, i):
        image = torch.from_numpy(self.images[i])
        return image, int(self.labels[i])


shapes = ShapesDataset(100)
image, label = shapes[3]
print(len(shapes), image.shape, image.dtype, label)
```

```text
100 torch.Size([1, 16, 16]) torch.float32 2
```

`__getitem__` her çağrıda **tek** örnek veriyor. Büyük veri setlerinde
burada diskten bir dosya okunur; her şeyi baştan belleğe almak gerekmez.

## DataLoader: kümeler hâlinde

`DataLoader` bir Dataset'i alıp her turda onu kümeler hâlinde dolaşır.
Örnekleri toplayıp `(küme, ...)` şekilli tensörlere dizer:

```python
loader = DataLoader(data, batch_size=64, shuffle=True,
                    generator=torch.Generator().manual_seed(0), num_workers=0)
xb, yb = next(iter(loader))
print(xb.shape, yb.shape, len(loader))
sizes = [len(yb) for _, yb in loader]
print(sizes[:3], sizes[-1], sum(sizes))
```

```text
torch.Size([64, 64]) torch.Size([64]) 29
[64, 64, 64] 5 1797
```

- `batch_size=64`: her küme 64 örnek. 1797 örnek 29 kümeye bölünüyor;
  sonuncusu artanlar, yalnızca 5 örnek. İstersen
  `drop_last=True` onu atar.
- `shuffle=True`: her turda örnekler karıştırılıyor. Ardışık örnekler
  benzerse (önce bütün 0'lar, sonra bütün 1'ler) karıştırmadan eğitim
  bozulur.
- `generator=...manual_seed(0)` karıştırma sırasını sabitliyor; aynı tohumla
  her çalıştırmada aynı sıra.
- `num_workers=0` veriyi ana süreçte hazırlar. Büyük veride birkaç işçi
  süreç hızlandırır; bu patikadaki küçük verilerde gerek yok.

## Eğitim ve test ayırmak

`random_split` bir Dataset'i rastgele iki (ya da daha çok) parçaya böler:

```python
train_set, test_set = random_split(data, [1500, 297],
                                   generator=torch.Generator().manual_seed(0))
print(len(train_set), len(test_set), type(train_set).__name__)
```

```text
1500 297 Subset
```

Parçalar `Subset`: veriyi kopyalamıyor, yalnızca hangi sıraların kendisine
ait olduğunu tutuyor.

## Kümelerle eğitim döngüsü

Döngü artık iki katlı: dışarıda turlar (epoch), içeride kümeler. Dört adım
her **küme** için yapılıyor:

```python
torch.manual_seed(0)
train_loader = DataLoader(train_set, batch_size=32, shuffle=True,
                          generator=torch.Generator().manual_seed(0), num_workers=0)
model = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 10))
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
loss_fn = nn.CrossEntropyLoss()
for epoch in range(5):
    total = 0.0
    for xb, yb in train_loader:
        optimizer.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        optimizer.step()
        total += loss.item() * len(yb)
    print(epoch, round(total / len(train_set), 2))

x_test, y_test = test_set[:]
with torch.no_grad():
    correct = (model(x_test).argmax(dim=1) == y_test).sum().item()
print(correct > 270, len(train_loader) * 5)
```

```text
0 1.77
1 0.61
2 0.31
3 0.23
4 0.18
True 235
```

- 32'lik kümelerle bir turda 47 küme var; 5 turda model
  235 kez güncellendi.
  Giriş bölümündeki tam veri eğitimi 200 turda 200 güncelleme yapıyordu.
  Kümeler, verinin üzerinden bir kez geçerken bile çok sayıda adım atmayı
  sağlıyor.
- Turun kaybını, kümelerin kayıplarını küme büyüklüğüyle ağırlıklandırıp
  toplayarak hesapladık (son küme küçük).
- 297 test görüntüsünün 270'ten fazlası doğru.
- `test_set[:]` bütün test örneklerini tek seferde alıyor; değerlendirmede
  küme gerekmiyorsa böyle.

## Özet

- `Dataset`: `__len__` ve `__getitem__`; tek örnek verir.
- `DataLoader`: Dataset'i kümeler hâlinde, istersen karıştırarak dolaşır.
- Tekrarlanabilirlik için karıştırmada `generator=torch.Generator().manual_seed(...)`.
- `random_split` ile eğitim ve test ayrılır.
- Eğitim döngüsü iki katlı; dört adım her küme için.
