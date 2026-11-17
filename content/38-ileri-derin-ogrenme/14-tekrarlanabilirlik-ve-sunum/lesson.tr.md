# Tekrarlanabilirlik ve Modeli Sunmak

Bir deneyin sonucu ancak **yeniden üretilebiliyorsa** güvenilirdir. "Dün
%91 çıkmıştı, bugün %87" diyorsan iki çalıştırma arasında neyin değiştiğini
bilmen gerekir. Bu bölümün ilk yarısı aynı kodun aynı sonucu vermesini
sağlamak, ikinci yarısı eğitilmiş modeli başkasının kullanabileceği bir
**tahmin fonksiyonunun** arkasına koymak.

## Tohumlar

Eğitimde rastgelelik birçok yerden gelir: ağırlıkların başlangıcı, verinin
karıştırılması, dropout, veri artırma. Hepsinin tohumunu tek bir fonksiyonda
sabitleyelim:

```python
import json
import random
import numpy as np
import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_table


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


x, y = map(torch.tensor, make_table(600, seed=7))


def train(seed, epochs=10):
    set_seed(seed)
    model = nn.Sequential(nn.Linear(6, 32), nn.ReLU(), nn.Dropout(0.2),
                          nn.Linear(32, 3))
    loader = torch.utils.data.DataLoader(
        torch.utils.data.TensorDataset(x[:500], y[:500]), batch_size=50, shuffle=True,
        generator=torch.Generator().manual_seed(seed))
    opt = torch.optim.Adam(model.parameters(), lr=0.01)
    for _ in range(epochs):
        model.train()
        for xb, yb in loader:
            opt.zero_grad()
            F.cross_entropy(model(xb), yb).backward()
            opt.step()
    return model.eval()


def same(a, b):
    return all(torch.equal(p, q) for p, q in zip(a.parameters(), b.parameters()))


print(same(train(0), train(0)), same(train(0), train(1)))
```

```text
True False
```

- Aynı tohumla iki eğitim **bit bit aynı** ağırlıkları verdi; farklı tohumla
  farklı.
- `DataLoader`'ın karıştırma sırası kendi `generator`'ından geliyor; ona da
  tohum verdik. Dropout `torch.manual_seed`'den etkileniyor.
- `random` ve `np.random` bu kodda kullanılmıyor ama bir veri artırma
  kütüphanesi kullanabilir; üçünü birden sabitlemek alışkanlık olmalı.

Aynı makinede aynı sonuç, başka makinede de aynı sonuç demek **değil**.
Farklı işlemciler kayan nokta hesaplarını farklı sırada yapabilir; uzun
eğitimlerde ağırlıklar son basamaklarda ayrışır. Bu programın içerikleri bu
yüzden ağırlık değerleri değil, doğruluk gibi sınırdan uzak sonuçlar
yazdırıyor.

## Deterministik algoritmalar

Bazı işlemlerin (çoğu ekran kartında) hızlı ama **her çalıştırmada biraz
farklı** sonuç veren sürümleri var. `torch.use_deterministic_algorithms(True)`
PyTorch'a yalnızca deterministik sürümleri kullanmasını söyler; böyle bir
sürümü olmayan işlem sessizce çalışmak yerine hata verir.

```python
torch.use_deterministic_algorithms(True)
print(torch.are_deterministic_algorithms_enabled(), same(train(0), train(0)))
torch.use_deterministic_algorithms(False)
```

```text
True True
```

CPU'da hemen her işlem zaten deterministik; ayar asıl ekran kartında fark
eder (orada ayrıca `CUBLAS_WORKSPACE_CONFIG` ortam değişkeni de istenir).
Bedeli biraz hızdır; hata ayıklarken ve sonuçları raporlarken açılır.

## Deney kaydı

Tekrarlanabilirliğin öbür yarısı **ne yaptığını yazmak**: hangi ayarlar,
hangi tohum, hangi veri, hangi sonuç. Bir sözlük ve bir JSON dosyası yeter:

```python
def accuracy(model):
    with torch.no_grad():
        return (model(x[500:]).argmax(1) == y[500:]).float().mean().item()


config = {"seed": 0, "epochs": 10, "lr": 0.01, "hidden": 32, "dropout": 0.2}
model = train(config["seed"], config["epochs"])
record = {"config": config, "torch": torch.__version__,
          "metrics": {"test_accuracy": accuracy(model)}}
with open("run-001.json", "w") as f:
    json.dump(record, f, indent=2)
with open("run-001.json") as f:
    loaded = json.load(f)
print(sorted(loaded), loaded["config"] == config)
print(loaded["metrics"]["test_accuracy"] > 0.8)
```

```text
['config', 'metrics', 'torch'] True
True
```

- Kayıtta PyTorch'un sürümü de var: sürüm değişince sonuç değişebilir.
- Gerçek projelerde buna verinin bir özeti (karması, hash), kodun git
  sürümü ve süre de eklenir; notlarda veri özetini görüyoruz.

## Modeli bir fonksiyona sarmak

Modeli kullanacak kişi PyTorch, tensör ya da `argmax` bilmek zorunda
olmamalı. Ona sade bir **tahmin fonksiyonu** veririz: Python listesi alır,
sözlük döndürür; modeli bir kez yükler, girdiyi denetler.

```python
CLASSES = ["low", "mid", "high"]


def predict(values):
    if len(values) != 6:
        raise ValueError(f"expected 6 values, got {len(values)}")
    with torch.inference_mode():
        logits = model(torch.tensor([values], dtype=torch.float32))
        probs = torch.softmax(logits, dim=1)[0]
    best = int(probs.argmax())
    return {"label": CLASSES[best], "probability": round(probs[best].item(), 2)}


answer = predict([1.5, 1.0, 0.0, 0.0, 1.0, 0.0])
print(answer["label"], 0.5 < answer["probability"] <= 1.0)
try:
    predict([1.0, 2.0])
except ValueError as e:
    print(e)
```

```text
mid True
expected 6 values, got 2
```

- Model fonksiyonun **dışında**, bir kez kuruluyor; her istekte yeniden
  yüklenmiyor.
- Girdinin uzunluğu baştan denetleniyor; yanlış girdi PyTorch'un anlaşılmaz
  şekil hatası yerine açık bir mesajla geri çevriliyor.
- Dönüş bir sözlük: etiketin adı ve olasılığı. Kullanan kodun tensör görmesi
  gerekmiyor.

Bu fonksiyon artık bir web uç noktasının arkasına konmaya hazır. FastAPI ile
REST API Yazmak modülündeki "Bir ML Modelini Sunmak" bölümü tam bunu
yapıyor; orada kabaca şöyle görünür (burada sunucu açmıyoruz):

```
@app.post("/predict")
def predict_endpoint(item: Features):
    return predict(item.values)
```

## Özet

- `set_seed`: `random`, `numpy`, `torch` üçü birden; `DataLoader`'a kendi
  `generator`'ı.
- Aynı tohum aynı makinede aynı sonucu verir; başka makinede son basamaklar
  değişebilir.
- `torch.use_deterministic_algorithms(True)`: deterministik olmayan işlem
  hata verir.
- Her çalıştırmayı kaydet: ayarlar, tohum, sürüm, sonuç.
- Sunarken modeli bir kez yükle, girdiyi denetle, sade bir sözlük döndür.
