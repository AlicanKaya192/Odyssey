# Hata Ayıklama

Derin öğrenmede hatalar iki türlüdür. **Gürültülü** hatalar programı durdurur
ve bir mesaj bırakır: şekil tutmaz, tür tutmaz. Bunlar can sıkıcıdır ama
kolaydır, çünkü mesaj yeri gösterir. **Sessiz** hatalar ise hiçbir mesaj
vermez: program çalışır, kayıp yazdırılır, yalnızca model öğrenmez ya da
beklenenden kötü öğrenir. Bu bölümde ikisini de yakalamanın yollarını,
her biri birkaç satırlık denetimlerle görüyoruz.

## Şekilleri katman katman izlemek

Şekil hatasının yerini bulmanın en kısa yolu girdiyi katmanlardan tek tek
geçirip her adımdaki şekli yazdırmaktır. `nn.Sequential` üzerinde dolaşmak
yeter:

```python
import math

import torch
from torch import nn


def make_model():
    return nn.Sequential(nn.Flatten(), nn.Linear(64, 32), nn.ReLU(),
                         nn.Linear(32, 10))


torch.manual_seed(0)
model = make_model()
x = torch.randn(16, 8, 8)
h = x
for layer in model:
    h = layer(h)
    print(type(layer).__name__, tuple(h.shape))
```

```text
Flatten (16, 64)
Linear (16, 32)
ReLU (16, 32)
Linear (16, 10)
```

16 resim `(8, 8)` geldi, `Flatten` her birini 64 sayıya açtı, iki `Linear`
32'ye ve 10'a indirdi. Bir katman beklemediği şekil alırsa hatanın
**hangi satırda** çıktığını bu döküm söyler.

## Sık görülen üç mesaj

```python
loss_fn = nn.CrossEntropyLoss()
logits = model(x)
attempts = [
    lambda: loss_fn(logits, torch.zeros(16)),
    lambda: model(x.double()),
    lambda: loss_fn(logits, torch.zeros(16, 1, dtype=torch.long)),
]
for attempt in attempts:
    try:
        attempt()
    except RuntimeError as error:
        print(error)
```

```text
expected target dtype to be Long or Byte, but got Float
mat1 and mat2 must have the same dtype, but got Double and Float
0D or 1D target tensor expected, multi-target not supported
```

- **Hedef ondalıklı:** `CrossEntropyLoss` sınıf numarası ister, yani tam
  sayı (`long`). Etiketleri `torch.zeros(16)` gibi ondalıklı kurmak bu
  mesajı verir. Çözüm: `y.long()`.
- **Tür karışık:** NumPy'dan gelen dizi çoğu zaman `float64`'tür (`Double`),
  modelin ağırlıkları `float32` (`Float`). Çözüm: `x.float()`.
- **Hedefin şekli `(16, 1)`:** hedef sınıf numaralarının düz listesi
  olmalı, `(16,)`. Çözüm: `y.squeeze(1)` ya da `y.view(-1)`.

## Sessiz hata 1: başlangıç kaybı

Eğitime başlamadan önce kayba bir kez bakmak çok şey söyler. Rastgele
başlatılmış bir model her sınıfa aşağı yukarı eşit olasılık verir; 10 sınıfta
bu, her doğru sınıfa 1/10 demek ve kayıp `−log(1/10) = log 10 ≈ 2,3`:

```python
y = torch.randint(0, 10, (16,))
print(round(loss_fn(model(x), y).item(), 1), round(math.log(10), 1))

broken = make_model()
with torch.no_grad():
    for p in broken.parameters():
        p.mul_(20)
print(round(loss_fn(broken(x), y).item(), 1))
```

```text
2.3 2.3
92.6
```

- Sağlıklı modelde başlangıç kaybı tam beklenen yerde: 2,3.
- Ağırlıkları 20 katına çıkarılmış (yanlış başlatılmış) modelin kaybı
  92,6: model daha hiçbir şey öğrenmeden rastgele cevaplarından
  çok **emin**. Başlangıç kaybı `log(sınıf sayısı)`'ndan çok uzaksa önce
  başlatmaya, girdinin ölçeğine ve kayıp fonksiyonuna bakılır.

## Sessiz hata 2: tek kümeyi ezberletmek

Bir modelin öğrenip öğrenemediğini anlamanın en hızlı denemesi: **8 örneklik
tek bir kümeyi** yüzlerce adım boyunca eğitmek. Sağlıklı bir model bu kadar
az veriyi ezberler ve kayıp sıfıra iner. İnmiyorsa sorun veride değil
kodda, eğitim döngüsünde ya da kayıptadır:

```python
def overfit_one_batch(bug):
    torch.manual_seed(0)
    net = make_model()
    if bug == "softmax":
        net.append(nn.Softmax(dim=1))
    optimizer = torch.optim.Adam(net.parameters(), lr=0.01)
    for step in range(200):
        optimizer.zero_grad()
        loss = loss_fn(net(x[:8]), y[:8])
        loss.backward()
        if bug != "no step":
            optimizer.step()
    return round(loss.item(), 2)


for bug in ["none", "softmax", "no step"]:
    print(bug, overfit_one_batch(bug))
```

```text
none 0.0
softmax 1.46
no step 2.26
```

- Hatasız model 8 örneği ezberledi: kayıp 0.
- Sonuna softmax eklenen model (`CrossEntropyLoss` logits ister; Aktivasyon
  ve Kayıp bölümü) 1,46'te takıldı: kayıp düşüyor ama sıfıra
  inemiyor.
- `optimizer.step()` unutulan model hiç değişmedi; kayıp başlangıçtaki
  2,26.
- Bu deneme hiçbir mesaj vermeyen üç durumu birbirinden ayırdı. Asıl eğitimi
  başlatmadan önce yapılır, bir dakika bile sürmez.

## Sessiz hata 3: biriken gradyan

`backward()` gradyanı `.grad`'a **ekler**, üzerine yazmaz. `zero_grad()`
unutulursa her adım öncekilerin toplamıyla yürür:

```python
w = torch.tensor(1.0, requires_grad=True)
for step in range(3):
    (3 * w).backward()
    print(w.grad.item())
```

```text
3.0
6.0
9.0
```

Gradyan her seferinde 3 olmalıydı; 3, 6, 9 diye birikti. Adım boyu turdan
tura büyüdüğü için eğitim kararsızlaşır. Ama Adam gibi gradyanı kendi
ölçeğine bölen bir optimizer bunu kısmen saklayabilir; bu yüzden sessiz bir
hatadır ve döngü yazarken alışkanlıkla `zero_grad()` en başa konur.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Şekiller</span><span>Katmanları tek tek geçir, her adımın şeklini yazdır.</span></div>
    <div class="anat-row"><span>Türler</span><span>Girdi <code>float32</code>, sınıf hedefi <code>long</code> ve düz <code>(n,)</code>.</span></div>
    <div class="anat-row"><span>Başlangıç kaybı</span><span>Sınıflandırmada <code>log(sınıf sayısı)</code> civarı mı?</span></div>
    <div class="anat-row"><span>Tek küme</span><span>8 örneği ezberleyebiliyor mu?</span></div>
    <div class="anat-row"><span>Döngü</span><span><code>zero_grad</code>, <code>backward</code>, <code>step</code> sırayla ve hepsi var mı?</span></div>
    <div class="anat-row"><span>Gradyanlar</span><span>Her parametrenin <code>.grad</code>'ı dolu ve sonlu mu?</span></div>
  </div>
  <figcaption>Model öğrenmiyorsa sırayla bakılacaklar.</figcaption>
</figure>

## Özet

- Gürültülü hatada mesajı oku; şekli katman katman yazdırarak yerini bul.
- `CrossEntropyLoss`: hedef `long` ve `(n,)`; girdi `float32`.
- Başlangıç kaybı `log(sınıf sayısı)` civarında olmalı.
- Tek kümeyi ezberletme denemesi kod hatalarını veriden ayırır.
- `zero_grad()` unutulursa gradyan birikir.
