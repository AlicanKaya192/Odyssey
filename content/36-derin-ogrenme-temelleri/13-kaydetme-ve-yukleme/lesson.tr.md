# Modeli Kaydetmek ve Yüklemek

Bir modeli saatlerce eğittin; program kapanınca öğrendiği her şey bellekte
kalıp gider. Bu bölümde eğitilmiş bir modeli diske yazmayı, başka bir
programda geri yüklemeyi ve yarıda kalan bir eğitimi kaldığı yerden
sürdürmeyi görüyoruz. Bir de güvenlik konusu var: model dosyası yalnızca
sayı taşıyormuş gibi görünse de, yanlış yüklenirse içinde kod çalıştırılabilen
bir dosyadır.

## state_dict

Modelin öğrendiği her şey parametrelerinde. `model.state_dict()` bunları
ad → tensör sözlüğü olarak verir:

```python
import torch
from torch import nn

torch.manual_seed(0)
model = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 3))
for name, tensor in model.state_dict().items():
    print(name, tuple(tensor.shape))
```

```text
0.weight (8, 4)
0.bias (8,)
2.weight (3, 8)
2.bias (3,)
```

- Adlar katmanın `Sequential` içindeki sırasından geliyor: `0` ilk `Linear`,
  `2` ikincisi. `ReLU`'nun (1) parametresi yok, sözlükte de yok.
- Sözlükte modelin **kodu** yok, yalnızca sayıları var. Yüklerken aynı
  yapıyı kodla yeniden kurup sayıları içine koyarız.

## Kaydetmek ve yüklemek

```python
torch.save(model.state_dict(), "model.pt")

torch.manual_seed(1)
restored = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 3))
x = torch.randn(5, 4)
print(torch.equal(model(x), restored(x)))
result = restored.load_state_dict(torch.load("model.pt", weights_only=True))
print(torch.equal(model(x), restored(x)))
print(result)
```

```text
False
True
<All keys matched successfully>
```

- Yeni model başka bir tohumla kuruldu; tahminleri farklıydı (`False`).
  Sayıları yükleyince birebir aynı oldu (`True`).
- `load_state_dict` her anahtarın eşleştiğini söylüyor. Eşleşmeyen bir
  anahtar olursa hata verir (ilk not).
- Tahmin için yüklenen modelde `model.eval()` unutulmaz (dropout ve
  BatchNorm kipleri).

## weights_only=True neden önemli

`torch.save` Python'un `pickle` biçimini kullanır. `pickle` yalnızca veri
saklamaz: bir dosya, yüklenirken **hangi Python fonksiyonunun çağrılacağını**
da söyleyebilir. Yani başkasından gelen bir model dosyasını körü körüne
yüklemek, o kişinin yazdığı kodu kendi bilgisayarında çalıştırmak demek
olabilir.

`weights_only=True` yükleyiciyi sıkı bir kipe alır: yalnızca tensörlere,
sayılara, metinlere, listelere ve sözlüklere izin verir, başka hiçbir nesne
kurmaz. PyTorch 2.6'dan beri varsayılan budur. Sıradan olmayan bir nesne
taşıyan dosyada ne olduğuna bakalım:

```python
class Note:
    def __init__(self, text):
        self.text = text


torch.save({"weights": model.state_dict(), "note": Note("hello")}, "odd.pt")
try:
    torch.load("odd.pt", weights_only=True)
except Exception as error:
    print(type(error).__name__)
    print(str(error).split(".")[0])
```

```text
UnpicklingError
Weights only load failed
```

- Dosya reddedildi; içindeki `Note` nesnesi kurulmadı.
- Hata mesajı `weights_only=False` ile yüklemenin mümkün olduğunu ama bunun
  **yalnızca dosyanın kaynağına güveniyorsan** yapılması gerektiğini söylüyor.
  Kendi yazdığın dosya için bile önce state_dict yolunu dene.
- Kural: başkasından gelen model dosyasını yalnızca `weights_only=True` ile
  yükle; mümkünse yalnızca tensör saklayan biçimleri (`safetensors` gibi)
  tercih et.

<figure class="fig">
  <div class="versus">
    <div class="ok"><h5>state_dict + weights_only=True</h5>Dosyada yalnızca sayılar var; yükleyici başka nesne kurmuyor. Model kodla yeniden kuruluyor.</div>
    <div class="no"><h5>weights_only=False</h5>Dosya yüklenirken Python nesneleri kurulabiliyor; güvenilmeyen dosyada bu, kod çalıştırmak demek.</div>
  </div>
  <figcaption>Model paylaşırken ve yüklerken varsayılan yol soldaki.</figcaption>
</figure>

## Kontrol noktası: kaldığın yerden sürdürmek

Uzun bir eğitim yarıda kesilebilir. Kaldığı yerden **aynen** sürdürmek
için yalnızca modeli değil, optimizer'ın durumunu ve tur sayısını da
kaydederiz. Adam her parametre için yürüyen ortalamalar tutar
(Optimizasyon bölümü); onlar kaybolursa eğitim aynı yoldan devam etmez:

```python
X = torch.randn(64, 4)
Y = torch.randint(0, 3, (64,))


def make():
    torch.manual_seed(0)
    net = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 3))
    return net, torch.optim.Adam(net.parameters(), lr=0.01)


def train(net, optimizer, epochs):
    for _ in range(epochs):
        optimizer.zero_grad()
        nn.functional.cross_entropy(net(X), Y).backward()
        optimizer.step()


net, optimizer = make()
train(net, optimizer, 4)
straight = net[0].weight.clone()

net, optimizer = make()
train(net, optimizer, 2)
torch.save({"epoch": 2, "model": net.state_dict(),
            "optimizer": optimizer.state_dict()}, "checkpoint.pt")

checkpoint = torch.load("checkpoint.pt", weights_only=True)
net, optimizer = make()
net.load_state_dict(checkpoint["model"])
optimizer.load_state_dict(checkpoint["optimizer"])
train(net, optimizer, 2)
print(checkpoint["epoch"], torch.equal(straight, net[0].weight))

net, optimizer = make()
net.load_state_dict(checkpoint["model"])
train(net, optimizer, 2)
print(torch.equal(straight, net[0].weight))
print(list(checkpoint["optimizer"]["state"][0].keys()))
```

```text
2 True
False
['step', 'exp_avg', 'exp_avg_sq']
```

- Model + optimizer yüklenince 2 + 2 tur, 4 turu birebir verdi (`True`).
- Yalnızca model yüklenince Adam'ın ortalamaları sıfırdan başladı ve
  ağırlıklar farklı çıktı (`False`).
- Adam her parametre için adım sayısını (`step`) ve iki yürüyen ortalamayı
  (`exp_avg`, `exp_avg_sq`) saklıyor. Bir öğrenme oranı zamanlayıcısı
  kullanıyorsan onun `state_dict()`'i de kontrol noktasına girer.
- Kontrol noktası da sıradan bir sözlük; `weights_only=True` ile yüklenebiliyor.

## Özet

- `model.state_dict()` parametreleri ad → tensör sözlüğü olarak verir;
  `torch.save` diske yazar.
- Yüklemek: aynı modeli kodla kur, `load_state_dict(torch.load(yol,
  weights_only=True))`.
- `pickle` dosyası yüklenirken kod çalıştırabilir; başkasından gelen dosyada
  `weights_only=False` kullanma.
- Eğitimi sürdürmek için model, optimizer (ve zamanlayıcı) durumu ile tur
  sayısını birlikte kaydet.
