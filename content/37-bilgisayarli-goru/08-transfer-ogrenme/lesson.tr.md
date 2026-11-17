# Transfer Öğrenme

Büyük ağları sıfırdan eğitmek çok veri ve çok zaman ister. Pratikte çoğu
görüntü projesi başka bir görevde, büyük bir veri setinde **önceden
eğitilmiş** bir ağla başlar. Örneğin ImageNet'te eğitilmiş bir ResNet-50'nin
son katmanı değiştirilir ve birkaç yüz kedi ile köpek fotoğrafıyla "kedi mi,
köpek mi" sınıflandırıcısı kurulur. Buna **transfer öğrenme** (transfer
learning) denir: bir görevde öğrenilen özellikler başka bir göreve taşınır.

Hazır ağırlık indirmiyoruz; onun yerine aynı fikri küçük ölçekte kendimiz
kuracağız: önce **kaynak görevde** (şekil sınıflandırma) bir ağı bol veriyle
eğiteceğiz, sonra onu az verili iki **hedef göreve** taşıyacağız. Bir hedef
kaynağa yakın, öteki uzak olacak.

## Kaynak görev: bol veriyle eğitmek

Ağı iki parçaya ayırıyoruz: resmi bir özellik vektörüne çeviren **gövde**
(`features`) ve vektörden sınıf puanı veren **baş** (head). Gövde, ResNet
gibi BatchNorm'lu ve sonunda küresel ortalama havuzlama var: her resim 64
sayılık bir özellik vektörüne iniyor.

```python
import torch
import torch.nn.functional as F
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from dl_data import make_shapes


def make_features():
    return nn.Sequential(
        nn.Conv2d(1, 16, 3, padding=1), nn.BatchNorm2d(16), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(16, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(),
        nn.AdaptiveAvgPool2d(1), nn.Flatten(),
    )


def fit(model, x, y, epochs, lr, params=None, seed=0, batch_size=32):
    params = model.parameters() if params is None else params
    optimizer = torch.optim.Adam(params, lr=lr)
    loader = DataLoader(TensorDataset(x, y), batch_size=batch_size, shuffle=True,
                        generator=torch.Generator().manual_seed(seed))
    for epoch in range(epochs):
        model.train()
        for xb, yb in loader:
            optimizer.zero_grad()
            F.cross_entropy(model(xb), yb).backward()
            optimizer.step()


def accuracy(model, x, y):
    model.eval()
    with torch.no_grad():
        return (model(x).argmax(dim=1) == y).float().mean().item()


x_src, y_src = map(torch.from_numpy, make_shapes(600, seed=1))
x_chk, y_chk = map(torch.from_numpy, make_shapes(300, seed=2))
torch.manual_seed(0)
source = nn.Sequential(make_features(), nn.Linear(64, 3))
fit(source, x_src, y_src, epochs=5, lr=0.005)
print(accuracy(source, x_chk, y_chk) > 0.95)
torch.save(source[0].state_dict(), "source_features.pt")
print(len(source[0].state_dict()))
```

```text
True
21
```

- Kaynak görevde ağ şekilleri neredeyse kusursuz ayırıyor.
- Yalnızca gövdenin ağırlıklarını (`state_dict`) bir dosyaya kaydettik:
  hazır eğitilmiş bir model indirmek de tam olarak böyle bir dosya almaktır.
  Sözlükte 21 kayıt var: üç evrişimin ağırlık ve sabitleri (6) ve üç
  BatchNorm'un ölçek, kaydırma, iki kayan istatistik ve bir sayacı (15).

## Üç yol

Yeni bir görev için üç seçenek var:

1. **Sıfırdan:** rastgele başlayan ağı yalnızca yeni verinin üstünde eğitmek.
2. **Özellik çıkarma** (feature extraction): kaynaktan gelen gövdeyi
   **dondurmak** (`requires_grad = False`), yalnızca yeni başı eğitmek.
3. **İnce ayar** (fine-tuning): gövdeyi de eğitmek, ama küçük bir öğrenme
   oranıyla; öğrenileni bozmadan yeni göreve kaydırmak.

```python
def make_model(mode, num_classes):
    features = make_features()
    if mode != "scratch":
        features.load_state_dict(torch.load("source_features.pt", weights_only=True))
    if mode == "frozen":
        for p in features.parameters():
            p.requires_grad = False
    return nn.Sequential(features, nn.Linear(64, num_classes))


def trainable(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


print(trainable(make_model("scratch", 2)), trainable(make_model("frozen", 2)))
```

```text
23650 130
```

Dondurulmuş modelde eğitilecek parametre yalnızca başınkiler: 64 × 2 + 2 =
130. `weights_only=True` dosyadan yalnızca tensörleri okuyor; başkasından
gelen bir dosyada kod çalıştırılmasını önlüyor.

## Yakın hedef: yuvarlak mı, köşeli mi?

İlk hedef görev kaynağa çok benziyor: aynı tür resimler, ama soru farklı
("daire mi, değil mi?") ve elimizde yalnızca **24** etiketli resim var. Tek
bir eğitimin sonucu tohuma göre oynayabildiği için her yolu üç tohumla
deneyip ortalamaya bakıyoruz.

```python
def compare(x_train, y_train, x_test, y_test, num_classes, epochs):
    results = {}
    for mode in ("scratch", "frozen", "finetune"):
        scores = []
        for seed in (0, 1, 2):
            torch.manual_seed(seed)
            model = make_model(mode, num_classes)
            params = model[1].parameters() if mode == "frozen" else None
            lr = 0.002 if mode == "finetune" else 0.005
            fit(model, x_train, y_train, epochs, lr, params, seed, batch_size=8)
            scores.append(accuracy(model, x_test, y_test))
        results[mode] = round(sum(scores) / 3, 2)
    return results


x_a, y_a = map(torch.from_numpy, make_shapes(24, seed=5))
x_at, y_at = map(torch.from_numpy, make_shapes(300, seed=6))
y_a, y_at = (y_a != 0).long(), (y_at != 0).long()
print(compare(x_a, y_a, x_at, y_at, num_classes=2, epochs=20))
```

```text
{'scratch': 0.88, 'frozen': 1.0, 'finetune': 0.95}
```

- **Özellik çıkarma** test resimlerinin hepsini doğru biliyor: kaynakta
  öğrenilen özellikler bu soru için zaten yeterli; 130 parametreyi 24
  resimle öğrenmek kolay.
- **Sıfırdan** eğitim 24 resimle geride kalıyor; sonuç tohumdan tohuma da
  çok oynuyor.
- İnce ayar ikisinin arasında: az veride bütün gövdeyi oynatmak bir miktar
  risk taşıyor.

## Uzak hedef: rakamlar

İkinci hedef kaynaktan uzak: el yazısı rakamlar (16 × 16'ya büyütülmüş), her
rakamdan yalnızca **5** eğitim resmi.

```python
from sklearn.datasets import load_digits

digits = load_digits()
x_all = torch.tensor(digits.images, dtype=torch.float32).unsqueeze(1) / 16
x_all = F.interpolate(x_all, size=16, mode="bilinear")
y_all = torch.tensor(digits.target)
order = torch.randperm(len(y_all), generator=torch.Generator().manual_seed(0))
train_idx = torch.cat([order[y_all[order] == d][:5] for d in range(10)])
test_mask = torch.ones(len(y_all), dtype=torch.bool)
test_mask[train_idx] = False
x_b, y_b = x_all[train_idx], y_all[train_idx]
x_bt, y_bt = x_all[test_mask], y_all[test_mask]
print(len(y_b), len(y_bt))
print(compare(x_b, y_b, x_bt, y_bt, num_classes=10, epochs=30))
```

```text
50 1747
{'scratch': 0.72, 'frozen': 0.4, 'finetune': 0.8}
```

- Bu kez **özellik çıkarma** çok kötü: daire ile kareyi ayırmak için
  öğrenilen özellikler, rakamları ayırmaya yetmiyor.
- **İnce ayar** en iyisi: gövde kenar, köşe gibi genel desenleri biliyor; az
  bir kaydırma onları rakamlara uyduruyor. Sıfırdan başlayan ağ 50 resimle
  bu kadar ileri gidemiyor.

Ders şu: **kaynak ile hedef ne kadar benzerse dondurmak o kadar iyi çalışır;
uzaklaştıkça ince ayar gerekir.** ImageNet gibi çok çeşitli bir kaynakta
öğrenilen özellikler çok farklı hedeflere bile iyi taşınır; bizim tek görevli
küçük kaynağımızın sınırı daha dar.

## Dondurmak BatchNorm'u durdurmaz

`requires_grad = False` ağırlıkları dondurur, ama BatchNorm'un kayan
istatistikleri (`running_mean`, `running_var`) ağırlık değil, tampon. Ağ
eğitim kipindeyken onlar her yığında güncellenir:

```python
torch.manual_seed(0)
frozen = make_model("frozen", 2)
weight_before = frozen[0][0].weight.clone()
stats_before = frozen[0][1].running_mean.clone()
fit(frozen, x_a, y_a, 5, 0.005, frozen[1].parameters(), batch_size=8)
print(torch.equal(frozen[0][0].weight, weight_before))
print(torch.equal(frozen[0][1].running_mean, stats_before))

torch.manual_seed(0)
frozen = make_model("frozen", 2)
stats_before = frozen[0][1].running_mean.clone()
optimizer = torch.optim.Adam(frozen[1].parameters(), lr=0.005)
frozen.train()
frozen[0].eval()
for xb, yb in DataLoader(TensorDataset(x_a, y_a), batch_size=8):
    optimizer.zero_grad()
    F.cross_entropy(frozen(xb), yb).backward()
    optimizer.step()
print(torch.equal(frozen[0][1].running_mean, stats_before))
```

```text
True
False
True
```

- Evrişim ağırlığı değişmedi, ama BatchNorm'un istatistiği değişti: gövde
  tam olarak donmamış.
- Gerçek bir dondurma için gövdeyi eğitim sırasında **değerlendirme
  kipinde** tutmak gerekir: `model.train()`'den sonra `model[0].eval()`.
- Bunun bir de sonucu var: hedef verisi küçük ya da kaynaktan farklıysa
  istatistikleri ona göre güncellemek kaynakta öğrenileni bozabilir.

## Ön işleme kaynakla aynı olmalı

Önceden eğitilmiş bir ağ, eğitildiği verinin ön işlemesini bekler. Bizim
kaynağımız [0, 1] aralığında gri resimlerle eğitildi; hedef resimleri de
aynı biçimde verdik (rakamları 16'ya bölüp 16 × 16'ya büyüttük). Hazır
eğitilmiş torchvision modelleri ise kendi ön işlemelerini yanlarında
taşıyor; bunu ağırlık indirmeden okuyabiliriz:

```python
from torchvision import models

info = models.ResNet18_Weights.IMAGENET1K_V1
prep = info.transforms()
print(prep.mean, prep.std)
print(prep.resize_size, prep.crop_size)
print(len(info.meta["categories"]))
```

```text
[0.485, 0.456, 0.406] [0.229, 0.224, 0.225]
[256] [224]
1000
```

ImageNet ağırlıklarıyla çalışırken resimler 256'ya küçültülüp ortadan
224 × 224 kesilir ve bu ortalama ve sapmayla normalleştirilir. Başka bir
normalleştirme verilirse ağ yine çalışır ama özellikleri bozulur.

## Özet

- Transfer öğrenme: kaynak görevde eğitilmiş gövde + yeni görev için yeni baş.
- Özellik çıkarma: gövde donuk, yalnızca baş öğrenir; kaynak yakınsa güçlü.
- İnce ayar: gövde de küçük öğrenme oranıyla öğrenir; kaynak uzaksa gerekir.
- Dondurulmuş gövdede BatchNorm için `eval()`; ön işleme kaynakla aynı.
- Ağırlık dosyası `torch.load(..., weights_only=True)` ile okunur.
