# Havuzlama ve CNN Mimarisi

Evrişim katmanı bir resimden özellik haritaları çıkarıyor. Bir sınıflandırıcı
için iki şey daha gerekiyor: haritaları **küçültmek** (hem hesap azalsın hem
de sonraki katmanlar daha geniş bir alana baksın) ve sonunda haritalardan
**sınıf puanlarına** geçmek. Bu bölümde havuzlama katmanını ve bunları bir
araya getiren **evrişimli sinir ağının** (convolutional neural network, CNN)
iskeletini kuracağız. Henüz eğitmeyeceğiz; her katmandan sonra verinin
şeklini izlemeyi öğreneceğiz.

## Maksimum havuzlama

**Havuzlama** (pooling) haritayı küçük karelere böler ve her kareden tek
sayı bırakır. **Maksimum havuzlama** (max pooling) karenin en büyüğünü,
**ortalama havuzlama** (average pooling) ortalamasını alır. 2 × 2'lik
havuzlama haritanın boyunu yarıya indirir.

```python
import torch
import torch.nn.functional as F

fmap = torch.tensor([
    [1, 3, 2, 0],
    [4, 6, 1, 1],
    [0, 2, 9, 5],
    [1, 1, 3, 7],
], dtype=torch.float32).reshape(1, 1, 4, 4)
print(F.max_pool2d(fmap, 2)[0, 0].tolist())
print(F.avg_pool2d(fmap, 2)[0, 0].tolist())
```

```text
[[6.0, 2.0], [2.0, 9.0]]
[[3.5, 1.0], [1.0, 6.0]]
```

- Sol üst kare `1, 3, 4, 6`: en büyüğü 6, ortalaması 3,5.
- Havuzlamanın öğrenilecek bir ağırlığı yok; yalnızca bir kural.

## Küçük kaymalara dayanıklılık

Maksimum havuzlama "bu karede desen bir yerde var mı?" sorusunu cevaplıyor;
**tam olarak nerede** olduğunu bir ölçüde unutuyor. Bu da küçük kaymaları
zararsız kılıyor:

```python
a = torch.zeros(1, 1, 4, 4)
b = torch.zeros(1, 1, 4, 4)
c = torch.zeros(1, 1, 4, 4)
a[0, 0, 0, 0] = 1
b[0, 0, 1, 1] = 1
c[0, 0, 2, 2] = 1
print(torch.equal(F.max_pool2d(a, 2), F.max_pool2d(b, 2)))
print(torch.equal(F.max_pool2d(a, 2), F.max_pool2d(c, 2)))
```

```text
True
False
```

- `a` ile `b`'deki nokta aynı 2 × 2 karenin içinde kaydı: havuzlanmış harita
  aynı.
- `c`'deki nokta başka kareye geçti: harita değişti. Havuzlama kaymaya
  **tamamen** değil, **biraz** dayanıklılık katıyor. Katmanlar üst üste
  bindikçe bu dayanıklılık büyüyor.

## Bir CNN'in iskeleti

Tipik bir sınıflandırıcı CNN birkaç kez tekrarlanan bir kalıptan oluşur:
**evrişim → ReLU → havuzlama**. Her tekrarda harita küçülür, kanal sayısı
artar: resim küçüldükçe her konumda daha çok ve daha karmaşık desen tutulur.
Sonunda harita düzleştirilir (`Flatten`) ve tam bağlı bir katman sınıf
puanlarını verir. ReLU, eksi değerleri sıfıra çeviren aktivasyon
fonksiyonu; Derin Öğrenmenin Temelleri modülünden tanıyorsun.

```python
from torch import nn

model = nn.Sequential(
    nn.Conv2d(1, 8, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Conv2d(8, 16, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(16 * 4 * 4, 3),
)
x = torch.zeros(1, 1, 16, 16)
for layer in model:
    x = layer(x)
    print(f"{type(layer).__name__:<10} {tuple(x.shape)}")
```

```text
Conv2d     (1, 8, 16, 16)
ReLU       (1, 8, 16, 16)
MaxPool2d  (1, 8, 8, 8)
Conv2d     (1, 16, 8, 8)
ReLU       (1, 16, 8, 8)
MaxPool2d  (1, 16, 4, 4)
Flatten    (1, 256)
Linear     (1, 3)
```

- Evrişimler `padding=1` ile boyu koruyor; her `MaxPool2d(2)` boyu yarıya
  indiriyor: 16 → 8 → 4.
- `Flatten` `(16, 4, 4)`'lük haritayı 256 sayılık bir listeye çeviriyor.
  `Linear(16 * 4 * 4, 3)`'teki 256 sayısı tam olarak buradan geliyor;
  yanlış yazılırsa ağ ilk çalıştırmada şekil hatası verir.
- Çıktı her sınıf için bir puan: `(1, 3)`.

## Parametreler nerede?

```python
for name, p in model.named_parameters():
    print(f"{name:<9} {tuple(p.shape)}")
print(sum(p.numel() for p in model.parameters()))

mlp = nn.Sequential(nn.Flatten(), nn.Linear(256, 64), nn.ReLU(), nn.Linear(64, 3))
print(sum(p.numel() for p in mlp.parameters()))
```

```text
0.weight  (8, 1, 3, 3)
0.bias    (8,)
3.weight  (16, 8, 3, 3)
3.bias    (16,)
7.weight  (3, 256)
7.bias    (3,)
2019
16643
```

- `0.weight`: `nn.Sequential` katmanları sıra numarasıyla adlandırıyor;
  `0` ilk evrişim, `7` son `Linear`.
- CNN'in toplam parametresi tek gizli katmanlı küçük bir tam bağlı ağdan
  (MLP) yaklaşık sekiz kat az (2019 ile 16 643). Üstelik CNN'in parametreleri desenleri her
  konumda arayan çekirdeklerde.

## Alıcı alan

Bir katmandaki tek bir sayı, girdi resminin ne kadarlık bir parçasından
etkileniyor? Bu alana **alıcı alan** (receptive field) denir. İlk 3 × 3
evrişimde 3 × 3 piksel; havuzlamadan sonra gelen her katman daha geniş bir
alanı görür. Hesap basit: her katman alıcı alanı `(çekirdek − 1) × atlama`
kadar büyütür; "atlama" o ana kadarki adımların çarpımı.

```python
layers = [("conv", 3, 1), ("pool", 2, 2), ("conv", 3, 1), ("pool", 2, 2)]
field, jump = 1, 1
for name, k, s in layers:
    field += (k - 1) * jump
    jump *= s
    print(name, field)
```

```text
conv 3
pool 4
conv 8
pool 10
```

İkinci evrişimden sonra her sayı 16 × 16'lık resmin 8 × 8'lik bir parçasını
görüyor. Derin ağlarda son katmanlar neredeyse bütün resmi görür; ilk
katmanlar kenar gibi küçük desenleri, son katmanlar şekil gibi büyük
desenleri yakalar.

## Her boyda resim: küresel ortalama havuzlama

Yukarıdaki ağ yalnızca 16 × 16 resimle çalışır: `Linear` katmanı tam 256
sayı bekliyor. Modern ağlar düzleştirmeden önce **küresel ortalama
havuzlama** (global average pooling) kullanır: her kanalın bütün haritası
tek bir sayıya, ortalamasına iner. `nn.AdaptiveAvgPool2d(1)` bunu yapıyor ve
çıktının boyu girdinin boyundan bağımsız oluyor.

```python
flexible = nn.Sequential(
    nn.Conv2d(1, 8, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Conv2d(8, 16, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.AdaptiveAvgPool2d(1),
    nn.Flatten(),
    nn.Linear(16, 3),
)
for size in (16, 24, 32):
    print(size, tuple(flexible(torch.zeros(2, 1, size, size)).shape))
```

```text
16 (2, 3)
24 (2, 3)
32 (2, 3)
```

Son `Linear` artık yalnızca 16 sayı istiyor (kanal başına bir ortalama). Aynı
ağ üç farklı boydaki resmi kabul ediyor. ResNet gibi ünlü mimariler de böyle
biter; ileride göreceğiz.

## Özet

- Havuzlama haritayı küçültür; maksimum havuzlama küçük kaymalara biraz
  dayanıklılık katar, öğrenilen ağırlığı yoktur.
- CNN kalıbı: (evrişim → ReLU → havuzlama) × birkaç, sonra `Flatten` ve
  `Linear`. Harita küçülür, kanal artar.
- Katmanlardan geçen şekli izlemek: `for layer in model: x = layer(x)`.
- Alıcı alan katman katman büyür; `AdaptiveAvgPool2d(1)` ağı girdi boyundan
  bağımsız yapar.
