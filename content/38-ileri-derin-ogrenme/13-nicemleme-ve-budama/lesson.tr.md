# Nicemleme ve Budama

Eğitilmiş bir modeli küçültmenin iki yaygın yolu var. **Nicemleme**
(quantisation) her ağırlığı daha az bitle yazar: 32 bitlik `float32`
yerine 8 bitlik bir tam sayı. **Budama** (pruning) önemsiz ağırlıkları
sıfırlar ya da tamamen çıkarır. İkisi de modeli küçültür ve uygun donanımda
hızlandırır; bedeli biraz doğruluk olabilir. Bu bölümde ikisini de
ölçüyoruz: ne kadar küçüldü, ne kadar doğruluk gitti.

## Başlangıç modeli

```python
import warnings
import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_table

x, y = map(torch.tensor, make_table(1000, seed=7))


def train():
    torch.manual_seed(0)
    net = nn.Sequential(nn.Linear(6, 64), nn.ReLU(), nn.Linear(64, 64), nn.ReLU(),
                        nn.Linear(64, 3))
    opt = torch.optim.Adam(net.parameters(), lr=0.01)
    gen = torch.Generator().manual_seed(1)
    for _ in range(30):
        perm = torch.randperm(800, generator=gen)
        for i in range(0, 800, 50):
            idx = perm[i:i + 50]
            opt.zero_grad()
            F.cross_entropy(net(x[idx]), y[idx]).backward()
            opt.step()
    return net.eval()


def accuracy(model):
    with torch.no_grad():
        return (model(x[800:]).argmax(1) == y[800:]).float().mean().item()


net = train()
acc = accuracy(net)
print(acc > 0.8, sum(p.numel() for p in net.parameters()))
```

```text
True 4803
```

`train()` her çağrıda aynı tohumla aynı modeli kuruyor; aşağıda her yöntemi
aynı modelin kendi kopyası üzerinde deneyeceğiz.

## Elle nicemleme: ölçek ve yuvarlama

En basit biçim **simetrik, tensör başına** nicemleme: tensördeki en büyük
mutlak değer 127'ye denk gelsin diye bir **ölçek** seçilir, her ağırlık
ölçeğe bölünüp yuvarlanır ve `int8` olarak saklanır. Kullanırken ölçekle
çarpılıp geri açılır.

```python
def quantize(w):
    scale = w.abs().max() / 127
    q = torch.round(w / scale).clamp(-127, 127).to(torch.int8)
    return q, scale


w = net[2].weight.detach()
q, scale = quantize(w)
restored = q.float() * scale
print(q.dtype, q.shape, w.element_size() // q.element_size())
print(bool((w - restored).abs().max() <= scale / 2 + 1e-6))
```

```text
torch.int8 torch.Size([64, 64]) 4
True
```

- Şekil aynı, tür `int8`: sayı başına 4 bayt yerine 1 bayt, **4 kat**
  küçük. Ölçek tensör başına tek bir sayı; yükü yok denecek kadar az.
- Yuvarlama hatası en fazla yarım ölçek: her ağırlık en yakın "basamağa"
  yuvarlandı.

## Doğruluk ne kadar gitti?

Bütün doğrusal katmanların ağırlığını nicemleyip geri açalım ve aynı test
verisinde ölçelim:

```python
qnet = train()
with torch.no_grad():
    for m in qnet:
        if isinstance(m, nn.Linear):
            q, scale = quantize(m.weight)
            m.weight.copy_(q.float() * scale)
print(abs(accuracy(qnet) - acc) < 0.02)
```

```text
True
```

8 bitle doğruluk neredeyse hiç değişmedi (bu bilgisayarda fark yüzde birden
az). Ağırlıkları 256 basamağa indirmek, bu modelin kararlarını
pek etkilemiyor. Büyük modellerde de 8 bit çoğu zaman güvenli; 4 bit ve
altında dikkatli yöntemler gerekir.

## PyTorch'un dinamik nicemlemesi

PyTorch'ta aynı işin hazır bir yolu var: **dinamik nicemleme** ağırlıkları
önceden `int8`'e çevirir, etkinlikleri (activations) çalışırken nicemler.
Doğrusal katmanlar için en kolay yöntem budur.

```python
warnings.simplefilter("ignore")
from torch.ao.quantization import quantize_dynamic

dnet = quantize_dynamic(train(), {nn.Linear}, dtype=torch.qint8)
kind = type(dnet[0])
print(kind.__name__, "quantized" in kind.__module__, dnet[0].weight().dtype)
print(dnet(x[:5]).dtype, abs(accuracy(dnet) - acc) < 0.05)
```

```text
Linear True torch.qint8
torch.float32 True
```

- Doğrusal katmanlar nicemlenmiş sürümleriyle değişti: adı yine `Linear`
  ama `torch.ao.nn.quantized` içinden geliyor; ağırlık türü `qint8`. Giriş ve çıkış yine `float32`: model dışarıdan aynı görünüyor.
- `warnings.simplefilter("ignore")` bilerek: bu sürümde `torch.ao.quantization`
  "kullanımdan kalkıyor" uyarısı veriyor. PyTorch nicemlemeyi ayrı bir pakete
  (`torchao`) taşıyor; bu programda kurulu değil. Fikir ve sonuç aynı.
- Nicemlenmiş katmanların hesabı işlemciye özgü bir arka uçta yapılır (bu
  bilgisayarda `onednn`, Mac'lerde başka bir arka uç). Bu yüzden ayrıntılı
  sonuç makineye göre biraz değişebilir; yalnızca doğruluğun yakın kaldığını
  yazdırdık.

## Budama

`torch.nn.utils.prune.l1_unstructured` bir katmanın mutlak değerce en küçük
ağırlıklarını sıfırlar. Önce yarısını, sonra onda dokuzunu budayalım:

```python
import torch.nn.utils.prune as prune

half = train()
prune.l1_unstructured(half[2], "weight", amount=0.5)
print(int((half[2].weight == 0).sum()), half[2].weight.numel())
print(abs(accuracy(half) - acc) < 0.05)
most = train()
prune.l1_unstructured(most[2], "weight", amount=0.9)
print(accuracy(most) < acc - 0.05)
```

```text
2048 4096
True
True
```

- Orta katmanın 4096 ağırlığının 2048'i sıfır; doğruluk yakın kaldı.
- Onda dokuzu budanınca doğruluk belirgin biçimde düştü. Ne kadar
  budanabileceği ölçülerek bulunur; çoğu zaman budamadan sonra kısa bir
  yeniden eğitim (ince ayar) kaybın bir kısmını geri getirir.

Budamanın bir tuzağı var: sıfırlar hâlâ yer kaplıyor. Ağırlık matrisi aynı
boyda, yalnızca içi seyrek. Gerçekten küçültmek için ya seyrek matris
biçimleri ve onları kullanan donanım gerekir ya da bütün bir nöronu
(satırı) çıkaran **yapısal budama**; notlarda ikincisini yapıyoruz.

## Özet

- Nicemleme: ölçek = en büyük |w| / 127, `round(w / ölçek)` → `int8`;
  4 kat küçük, 8 bitte doğruluk neredeyse aynı.
- `quantize_dynamic`: doğrusal katmanlar `qint8`, giriş ve çıkış `float32`;
  sonuç arka uca göre biraz değişebilir.
- Budama: küçük ağırlıkları sıfırlar; ne kadar budanacağı ölçülerek seçilir.
- Seyrek budama boyutu kendiliğinden küçültmez; yapısal budama küçültür.
