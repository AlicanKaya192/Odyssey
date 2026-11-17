# Tensörler

PyTorch'ta her şey bir **tensör** (tensor): girdi görüntüsü, etiketler,
modelin ağırlıkları, kayıp. Tensör, NumPy dizisine çok benzeyen çok
boyutlu bir sayı dizisidir. İki farkı var: tensör türev bilgisi
taşıyabilir (Otomatik Türev bölümünde) ve ekran kartında (GPU) da
yaşayabilir. Bu bölümde tensör kurmayı, şeklini ve türünü okumayı,
şeklini değiştirmeyi öğreneceğiz.

## Tensör kurmak

En kolay yol bir Python listesinden kurmak:

```python
import torch

a = torch.tensor([1, 2, 3])
b = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print(a, a.dtype, a.shape)
print(b.dtype, b.shape, b.ndim)
print(b[1, 2], b[1, 2].item())
```

```text
tensor([1, 2, 3]) torch.int64 torch.Size([3])
torch.float32 torch.Size([2, 3]) 2
tensor(6.) 6.0
```

- `shape` her boyuttaki eleman sayısı: `b` 2 satır, 3 sütun. `ndim` boyut
  sayısı.
- Tam sayılardan kurulan tensör `int64`, ondalıklı sayılardan kurulan
  `float32` oluyor. Sinir ağlarının ağırlıkları `float32`.
- `b[1, 2]` tek elemanlı bir tensör; içindeki Python sayısını `.item()`
  veriyor.

Boyutlara verilen adlar: tek sayı **skaler** (0 boyut), sayı listesi
**vektör** (1 boyut), tablo **matris** (2 boyut). Daha fazlası için
yalnızca "tensör" deniyor.

## Hazır kurucular

Çoğu zaman tensörü elle yazmayız; belli bir şekilde sıfır, bir, sıra ya
da rastgele sayılarla kurarız:

```python
print(torch.zeros(2, 3))
print(torch.ones(2, dtype=torch.int64))
print(torch.arange(0, 10, 3))
print(torch.linspace(0, 1, 5))
torch.manual_seed(0)
print(torch.rand(2, 2).shape, torch.randn(3).shape)
```

```text
tensor([[0., 0., 0.],
        [0., 0., 0.]])
tensor([1, 1])
tensor([0, 3, 6, 9])
tensor([0.0000, 0.2500, 0.5000, 0.7500, 1.0000])
torch.Size([2, 2]) torch.Size([3])
```

- `arange(başlangıç, bitiş, adım)` bitişi dahil etmiyor; `linspace`
  başlangıçla bitiş arasına eşit aralıklı 5 sayı koyuyor.
- `rand` 0–1 arası düzgün, `randn` ortalaması 0, standart sapması 1 olan
  rastgele sayılar veriyor. `torch.manual_seed(0)` rastgele üreteci sabitliyor:
  aynı tohumla aynı sayılar gelir.

## NumPy ile gidip gelmek

Veri çoğu zaman NumPy dizisi olarak gelir (scikit-learn, pandas). İki
yol var ve farkları önemli:

```python
import numpy as np

arr = np.array([1.0, 2.0, 3.0])
copied = torch.tensor(arr)
shared = torch.from_numpy(arr)
arr[0] = 100.0
print(copied.tolist(), shared.tolist())
print(copied.dtype, shared.numpy().dtype)
```

```text
[1.0, 2.0, 3.0] [100.0, 2.0, 3.0]
torch.float64 float64
```

- `torch.tensor(arr)` veriyi **kopyalıyor**; diziyi değiştirmek kopyayı
  etkilemiyor.
- `torch.from_numpy(arr)` aynı belleği **paylaşıyor**: dizideki değişiklik
  tensörde de görünüyor. Büyük veride kopyadan kaçmak için iyi, ama
  farkında olmadan değiştirmek kolay.
- NumPy'nin ondalık türü `float64`; tensör de `float64` oluyor. `.numpy()`
  tensörü NumPy dizisine geri çeviriyor.

## Tür (dtype) dönüştürmek

`float64` veriyi `float32` ağırlıklı bir katmana verirsek PyTorch hata
veriyor:

```python
layer = torch.nn.Linear(3, 1)
x = torch.from_numpy(np.ones((2, 3)))
try:
    layer(x)
except RuntimeError as error:
    print(error)
print(layer(x.float()).shape, x.float().dtype)
```

```text
mat1 and mat2 must have the same dtype, but got Double and Float
torch.Size([2, 1]) torch.float32
```

Hata mesajı iki matrisin (`mat1` girdi, `mat2` ağırlık) türünün aynı
olmadığını söylüyor: `Double` `float64`'ün, `Float` `float32`'nin adı. `.float()` tensörü `float32`'ye, `.long()` `int64`'e
çeviriyor; `x.to(torch.float32)` aynı işin uzun yazımı. Kural:
**girdiler `float32`, sınıf etiketleri `int64`.**

## Dizinleme ve dilimleme

Satır, sütun ve dilim seçmek NumPy'deki gibi:

```python
m = torch.arange(12).reshape(3, 4)
print(m)
print(m[0], m[:, 1].tolist())
print(m[1:, 2:].tolist())
print(m[m > 8].tolist())
```

```text
tensor([[ 0,  1,  2,  3],
        [ 4,  5,  6,  7],
        [ 8,  9, 10, 11]])
tensor([0, 1, 2, 3]) [1, 5, 9]
[[6, 7], [10, 11]]
[9, 10, 11]
```

- `m[0]` ilk satır, `m[:, 1]` ikinci sütun (`:` "bu boyutun hepsi").
- `m[1:, 2:]` ikinci satırdan ve üçüncü sütundan sonrası.
- `m[m > 8]` koşulu tutan elemanlar (maske ile seçmek).

## Şekil değiştirmek

Derin öğrenmede en sık yapılan iş tensörün şeklini değiştirmek: bir
görüntüyü düz bir vektöre çevirmek, başına bir "küme" boyutu eklemek.

```python
t = torch.arange(6)
print(t.reshape(2, 3).tolist())
print(t.reshape(3, -1).shape)
v = t.reshape(1, 6)
print(v.shape, v.squeeze().shape)
print(t.unsqueeze(0).shape, t.unsqueeze(1).shape)
```

```text
[[0, 1, 2], [3, 4, 5]]
torch.Size([3, 2])
torch.Size([1, 6]) torch.Size([6])
torch.Size([1, 6]) torch.Size([6, 1])
```

- `reshape` eleman sayısı aynı kaldıkça şekli değiştiriyor (6 = 2 × 3).
  `-1` "bu boyutu sen hesapla" demek.
- `unsqueeze(0)` başa 1 uzunluklu bir boyut ekliyor, `squeeze()` 1
  uzunluklu boyutları atıyor.

## Görüntü tensörleri

Bu patikanın alıştırmalarındaki `dl_data` modülü sabit tohumla basit şekil
görüntüleri üretiyor (daire, kare, üçgen). Görüntüler PyTorch'un alıştığı
sırada: **(adet, kanal, yükseklik, genişlik)**.

```python
from dl_data import make_shapes

images, labels = make_shapes(100, size=16)
x = torch.from_numpy(images)
print(x.shape, x.dtype, labels[:6].tolist())
flat = x.flatten(start_dim=1)
print(flat.shape, x[0].shape, x[0, 0].shape)
```

```text
torch.Size([100, 1, 16, 16]) torch.float32 [2, 1, 2, 2, 1, 2]
torch.Size([100, 256]) torch.Size([1, 16, 16]) torch.Size([16, 16])
```

<figure class="fig">
  <div class="flow">
    <span class="node">100 görüntü</span><span class="arrow">→</span>
    <span class="node">1 kanal<br><small>gri</small></span><span class="arrow">→</span>
    <span class="node">16 satır</span><span class="arrow">→</span>
    <span class="node acc">16 sütun</span>
  </div>
  <figcaption>(100, 1, 16, 16): ilk boyut görüntü sırası, ikincisi kanal (gri görüntüde 1, renkli görüntüde 3), son ikisi pikseller.</figcaption>
</figure>

`flatten(start_dim=1)` ilk boyutu (görüntü sırası) koruyup gerisini düz bir
vektöre çeviriyor: her görüntü 1 × 16 × 16 = 256 sayı. Giriş bölümündeki
`nn.Linear(64, ...)` katmanı da 8 × 8 rakamları böyle düzleştirilmiş
alıyordu.

## Özet

- Tensör, PyTorch'un çok boyutlu dizisi; `shape`, `dtype`, `ndim` ile
  okunur.
- `torch.tensor` kopyalar, `torch.from_numpy` belleği paylaşır.
- Girdiler `float32` (`.float()`), sınıf etiketleri `int64` (`.long()`).
- `reshape`, `flatten`, `unsqueeze`, `squeeze` şekli değiştirir; eleman
  sayısı aynı kalır.
- Görüntüler (adet, kanal, yükseklik, genişlik) sırasında.
