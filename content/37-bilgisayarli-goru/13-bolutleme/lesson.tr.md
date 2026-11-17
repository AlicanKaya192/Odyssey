# Anlamsal Bölütleme

Sınıflandırma resme tek bir etiket verir ("bu bir kare"). Algılama her nesneye
bir kutu çizer. **Anlamsal bölütleme** (semantic segmentation) bir adım daha
ileri gider: resmin **her pikseline** bir sınıf verir. Sonuç resimle aynı
boyda bir **maske**dir. Tıbbi görüntüde bir tümörün sınırı, uydu resminde
yollar ve tarlalar, sürücüsüz araçta yol ile kaldırımın ayrımı böyle bulunur.

Bu bölümde sahnelerimizin maskelerini kullanıp her pikseli sınıflandıran küçük
bir ağ eğiteceğiz, onu doğru ölçmeyi (piksel doğruluğu, IoU, Dice) ve
**sınıf dengesizliği** sorununu göreceğiz.

## Maske

`make_scenes` her sahne için kutuların yanında bir maske de veriyor:
`(32, 32)`'lik bir tam sayı tablosu. 0 arka plan, 1 daire, 2 kare, 3 üçgen.

```python
import torch
from dl_data import make_scenes

images, boxes, masks = make_scenes(500, size=32, seed=7)
x = torch.tensor(images)
y = torch.tensor(masks)
print(x.shape, y.shape, y.dtype)
counts = torch.bincount(y.flatten(), minlength=4)
print(counts.tolist())
print([round(v, 3) for v in (counts / counts.sum()).tolist()])
```

```text
torch.Size([500, 1, 32, 32]) torch.Size([500, 32, 32]) torch.int64
[459166, 20808, 18703, 13323]
[0.897, 0.041, 0.037, 0.026]
```

- Görüntü `(500, 1, 32, 32)`, maske `(500, 32, 32)`: kanal yok, her pikselde
  bir sınıf numarası. Tür `int64`, çünkü kayıp fonksiyonu sınıf numarasını
  böyle bekliyor.
- Piksellerin **yaklaşık %90'ı arka plan**. Şekiller %2,6 ile %4,1
  arasında. Bu dengesizlik bölümün asıl konusu.

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="371.52pt" height="194.850783pt" viewBox="0 0 371.52 194.850783" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 194.850783 
L 371.52 194.850783 
L 371.52 0 
L 0 0 
L 0 194.850783 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g clip-path="url(#p78f8f83102)">
    <image xlink:href="data:image/png;base64,
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" id="imagec5048a0eab" transform="scale(1 -1) translate(0 -77.76)" x="7.2" y="-6.930783" width="77.76" height="77.76"/>
   </g>
  </g>
  <g id="axes_2">
   <g clip-path="url(#p0a38b7e3cf)">
    <image xlink:href="data:image/png;base64,
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" id="image44e27cc75a" transform="scale(1 -1) translate(0 -77.76)" x="100.08" y="-6.930783" width="77.76" height="77.76"/>
   </g>
  </g>
  <g id="axes_3">
   <g clip-path="url(#pd020ce5409)">
    <image xlink:href="data:image/png;base64,
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" id="image4d6fdc49a9" transform="scale(1 -1) translate(0 -77.76)" x="193.68" y="-6.930783" width="77.76" height="77.76"/>
   </g>
  </g>
  <g id="axes_4">
   <g clip-path="url(#pffde2f1ef8)">
    <image xlink:href="data:image/png;base64,
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" id="image874322d1d9" transform="scale(1 -1) translate(0 -77.76)" x="286.56" y="-6.930783" width="77.76" height="77.76"/>
   </g>
  </g>
  <g id="axes_5">
   <g clip-path="url(#p788f9df2c9)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAGwAAABsCAYAAACPZlfNAAABl0lEQVR4nO3csU3DUBRAUQdRM0m2YBE6GnZA7EBDxyJs4UlYILSRBVICdpyLzylTxJGu3s+TY2U3DMNhIONm7Q/AeQSLESxGsBjBYgSLESxGsBjBYgSLESxGsBjBYgSLESxGsJjbtT9A1evjx7evP73dL3pdExYjWMzOMx1/OwLPMcdxacJiBIsRLMZav/D31txMWIxgMYLFCBYjWIxgMYLFCBYjWIw7HSfeXb+Wux4mLEawGD9g/pJnOjiJIzHGkRhjwmIEixEsRrAYwWIEixEsRrAYwWIEixEsRrAYwWI28UzH4flutWvvXj5nfT8TFiNYzEWPxP37ftH3Hx/G4b8zYTGCxQgWI1iMYDGCxVx0rT9eu+dY8ccNrPFTJixGsBjBYgSLESxGsJjVfsCcruSnrvnjBlf5YyYsRrAYwWIEixEs5moec/vpxvDWt8IpExYjWIxgMYLFCBYjWIz/mooxYTGCxQgWI1iMYDGCxQgWI1iMYDGCxQgWI1iMYDGCxQgWI1iMYDGCxQgWI1iMYDGCxQg2tHwBLooor8fDTskAAAAASUVORK5CYII=" id="imagec7d3615a86" transform="scale(1 -1) translate(0 -77.76)" x="7.2" y="-109.890783" width="77.76" height="77.76"/>
   </g>
  </g>
  <g id="axes_6">
   <g clip-path="url(#p8f87ea6593)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAGwAAABsCAYAAACPZlfNAAABiklEQVR4nO3cQUrDQBiA0am49giC+/RO3kS8Se9k94JH8AJ1WwpKhbTNa763bQmBj38Ykk43Y4zDCOPh1jeQ/ykYpmCYgmEKhikYpmCYgmEKhikYpmCYgmEKhikYpmCYgmEKhikYpmCYx7FAh7eni15/8/49VE0YpmCYgmEKhikYpmCYgmEKhikYpmCYgmEKhikYZpFP6+ewfXn+9bNpd7372L/uZ71eE4YpGOZul8SPz6+zl8ilL4PHmjBMwTAFwxQMUzBMwTCbNf7X1LSbmG38qSYMUzBMwTAFwxQMUzDMKrf1c2zxr7mVP9aEYQqGudsXmOee6tyO+U+JXvKEZxOGKRhmNUviHL/9OP3uLTRhmIJhCoYpGKZgmIJhVr+tX+LW/S9NGKZgmIJhCoYpGKZgmIJhCoYpGKZgmIJhCoYpGKZgmIJhCoYpGKZgmIJhVn+gT9OEYQqGKRimYJiCYQqGKRimYJiCYQqGKRimYJiCYQqGKRimYJiCYQqGKRimYJiCYQqGKdiw/AD/CiMGkGdjEQAAAABJRU5ErkJggg==" id="image271b313538" transform="scale(1 -1) translate(0 -77.76)" x="100.08" y="-109.890783" width="77.76" height="77.76"/>
   </g>
  </g>
  <g id="axes_7">
   <g clip-path="url(#pd4fbf0edd0)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAGwAAABsCAYAAACPZlfNAAABWUlEQVR4nO3dwY3CQBAAwQU5HAd1oRGU84GvxY/PWTXuSgCk1syO+PBYa71XGM+rv0B+UzBMwTAFwxQMUzBMwTAFwxQMUzBMwTAFwxQMUzBMwTAFwxQMUzBMwTAFwxQMUzBMwTAFwxQMUzBMwTAFwxQMUzBMwTAFwxQMsy3Y/tov+dzj71hXacIwBcPQK/Eua/CsCcMUDLNNWVP7RRfjf2vCMAXDFAxDv2F3OeXPmjBMwTDb1PW1Dz3zmzBMwTAFw4x5w6ae8d+aMEzBMGNX4jH0l/wmDFMwzNiVOOkyPGvCMAXDFAxzizfsGHTiN2GYgmEe/X+YpQnDFAxTMEzBMAXDFAxTMEzBMAXDFAxTMEzBMAXDFAxTMEzBMAXDFAxTMEzBMAXDFAxTMEzBMAXDFAxTMEzBMAXDFAxTMEzBMAXDFAxTMEzBMAXDFAxTMEzBMAXDFAxTsGX5AMdWGgcveuT6AAAAAElFTkSuQmCC" id="imagec9164f33db" transform="scale(1 -1) translate(0 -77.76)" x="193.68" y="-109.890783" width="77.76" height="77.76"/>
   </g>
  </g>
  <g id="axes_8">
   <g clip-path="url(#p06993a159c)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAGwAAABsCAYAAACPZlfNAAABXklEQVR4nO3dwQnCUBRFwa9YjkVZmkX9fnQbXKkYzTEzBUjg8MLdBA9jjNsg4/jrB+A1gsUIFiNYjGAxgsUIFiNYjGAxgsUIFiNYjGAxgsUIFiNYjGAxgsUIFiNYjGAxgsUIFiNYjGAxgsUIFiNYjGAxgsUIFiNYjGAxgsUIFiNYjGAxgsUIFiNYjGAxgsUIFiNYjGAxgsUIFiNYjGAxgsUIFiNYjGAxp0//4Pl6HlswL3P8IxcWI1iMYDGCxQgWI1jMYe0/y/nmzJ9/OuWXXFiMYDGCxQgWI1jM6itxzcU4d7AKH7mwGMFiBIsRLEawGMFivjrrPzHz5w6n/JILixEsRrAYwWIEixEs5qez/tmJv/cpv+TCYgTb+9cr71q+9rbyBcwWubAYwWIEi9nMrOc5LixGsBjBYgSLESxGsBjBYgSLESxGsBjBYgSLESxGsBjBYgSLESxGsBjBRssdKU0Y0Y9dqZMAAAAASUVORK5CYII=" id="image3c00faeaa5" transform="scale(1 -1) translate(0 -77.76)" x="286.56" y="-109.890783" width="77.76" height="77.76"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p78f8f83102">
   <rect x="7.2" y="7.2" width="77.634783" height="77.634783"/>
  </clipPath>
  <clipPath id="p0a38b7e3cf">
   <rect x="100.361739" y="7.2" width="77.634783" height="77.634783"/>
  </clipPath>
  <clipPath id="pd020ce5409">
   <rect x="193.523478" y="7.2" width="77.634783" height="77.634783"/>
  </clipPath>
  <clipPath id="pffde2f1ef8">
   <rect x="286.685217" y="7.2" width="77.634783" height="77.634783"/>
  </clipPath>
  <clipPath id="p788f9df2c9">
   <rect x="7.2" y="110.016" width="77.634783" height="77.634783"/>
  </clipPath>
  <clipPath id="p8f87ea6593">
   <rect x="100.361739" y="110.016" width="77.634783" height="77.634783"/>
  </clipPath>
  <clipPath id="pd4fbf0edd0">
   <rect x="193.523478" y="110.016" width="77.634783" height="77.634783"/>
  </clipPath>
  <clipPath id="p06993a159c">
   <rect x="286.685217" y="110.016" width="77.634783" height="77.634783"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Üstte dört sahne, altta maskeleri: siyah arka plan, mor daire, turuncu kare, yeşil üçgen.</figcaption>
</figure>

## Hep "arka plan" diyen model

Hiçbir şey öğrenmeyen, her piksele 0 diyen bir "model" ne kadar doğru olur?

```python
x_train, y_train = x[:400], y[:400]
x_test, y_test = x[400:], y[400:]
always_background = torch.zeros_like(y_test)
print(round((always_background == y_test).float().mean().item(), 2))
```

```text
0.9
```

Piksel doğruluğu %90, ama tek bir şekil bile bulunmadı. Bölütlemede **piksel
doğruluğu yanıltır**; her sınıfa ayrı bakan ölçüler gerekiyor (aşağıda).

## Her pikseli sınıflandıran ağ

Sınıflandırma ağı sonda resmi tek bir vektöre indiriyordu. Bölütleme ağı ise
resmin boyunu **geri** kurmalı: çıktı `(N, 4, 32, 32)`, her pikselde dört
sınıfın puanı. Basit bir **kodlayıcı–çözücü** (encoder–decoder): önce
evrişim ve havuzlama ile küçült (bağlamı gör), sonra **ters evrişim**
(`ConvTranspose2d`) ile büyüt (konumu geri kur), en sonda 1 × 1 evrişimle her
piksele sınıf puanları.

```python
from torch import nn


def make_model():
    torch.manual_seed(0)
    return nn.Sequential(
        nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(),
        nn.Conv2d(16, 16, 3, padding=1), nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(),
        nn.ConvTranspose2d(32, 16, 2, stride=2), nn.ReLU(),
        nn.Conv2d(16, 4, 1),
    )


model = make_model()
print(model(x[:8]).shape)
print(nn.ConvTranspose2d(32, 16, 2, stride=2)(torch.zeros(1, 32, 16, 16)).shape)
```

```text
torch.Size([8, 4, 32, 32])
torch.Size([1, 16, 32, 32])
```

- `MaxPool2d(2)` 32'yi 16'ya indiriyor, `ConvTranspose2d(..., 2, stride=2)`
  16'yı yeniden 32'ye çıkarıyor.
- Son katman 1 × 1 evrişim: her pikselin 16 özelliğinden 4 sınıf puanı.
- Tam bağlı katman yok: bu yüzden bu tür ağlara **tam evrişimli ağ** (fully
  convolutional network, FCN) deniyor; istenen boyda resim alabilir.

## Eğitmek: piksel başına çapraz entropi

`CrossEntropyLoss` bölütlemeyi kendiliğinden tanıyor: çıktı `(N, C, H, W)`,
hedef `(N, H, W)` olunca her piksel için kaybı hesaplayıp ortalamasını alıyor.

```python
def train(model, weight=None, epochs=15):
    loss_fn = nn.CrossEntropyLoss(weight=weight)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    generator = torch.Generator().manual_seed(1)
    for epoch in range(epochs):
        order = torch.randperm(400, generator=generator)
        for start in range(0, 400, 32):
            batch = order[start:start + 32]
            optimizer.zero_grad()
            loss = loss_fn(model(x_train[batch]), y_train[batch])
            loss.backward()
            optimizer.step()
    return model


plain = train(make_model())
with torch.no_grad():
    predicted = plain(x_test).argmax(dim=1)
print(predicted.shape)
print(round((predicted == y_test).float().mean().item(), 2))
```

```text
torch.Size([100, 32, 32])
0.96
```

Tahmin `argmax(dim=1)` ile: her pikselde puanı en yüksek sınıf. Piksel
doğruluğu %96. Hep arka plan diyen modelden yalnızca 6 puan iyi; bu sayı tek
başına çok az şey söylüyor.

## IoU, mIoU ve Dice

Her sınıf için tahmin edilen pikseller ile gerçek pikselleri iki küme gibi
düşün. Algılamadaki IoU burada piksel kümelerine uygulanıyor:

- **IoU** = ortak piksel / birleşim pikseli.
- **mIoU** (mean IoU): sınıfların IoU ortalaması. Her sınıf eşit sayılır; küçük
  sınıfın kötü sonucu gizlenemez.
- **Dice** = 2 × ortak / (tahmin + gerçek). Tıbbi bölütlemede yaygın; IoU ile
  aynı sırayı verir, değeri biraz daha yüksektir.

```python
def class_scores(predicted, truth, num_classes=4):
    ious, dices = [], []
    for c in range(num_classes):
        p, t = predicted == c, truth == c
        common = (p & t).sum().item()
        ious.append(common / (p | t).sum().item())
        dices.append(2 * common / (p.sum().item() + t.sum().item()))
    return ious, dices


ious, dices = class_scores(predicted, y_test)
print([round(v, 2) for v in ious])
print(round(sum(ious) / 4, 2))
```

```text
[1.0, 0.51, 0.12, 0.69]
0.58
```

- Arka plan neredeyse kusursuz (1,0), üçgen fena değil (0,69), daire yarı
  yarıya (0,51), **kare neredeyse hiç bulunmuyor** (0,12).
- mIoU 0,58: piksel doğruluğunun (%96) gizlediği sorunu bu sayı gösteriyor.

## Dengesizliğe çare: sınıf ağırlıkları

Piksellerin %90'ı arka plan olunca kayıp da büyük ölçüde arka plandan geliyor;
ağ "emin olamadığım yere arka plan derim" diyerek kaybı epey düşürebiliyor.
Çarelerden biri kayıpta **sınıf ağırlıkları**: az görülen sınıfın hatası daha
pahalı olsun. Sık kullanılan bir seçim: toplam piksel / (sınıf sayısı × o
sınıfın pikseli).

```python
weight = counts.sum() / (4 * counts.float())
print([round(v, 2) for v in weight.tolist()])
weighted = train(make_model(), weight=weight)
with torch.no_grad():
    predicted_w = weighted(x_test).argmax(dim=1)
ious_w, dices_w = class_scores(predicted_w, y_test)
print(round((predicted_w == y_test).float().mean().item(), 2))
print([round(v, 2) for v in ious_w])
print(round(sum(ious_w) / 4, 2), [round(v, 2) for v in dices_w])
```

```text
[0.28, 6.15, 6.84, 9.61]
0.98
[0.99, 0.68, 0.7, 0.76]
0.78 [1.0, 0.81, 0.82, 0.86]
```

- Arka planın ağırlığı 0,28, şekillerinki 6–10: bir kare pikselini kaçırmak
  bir arka plan pikselini kaçırmaktan yaklaşık 25 kat pahalı.
- Arka planın IoU'su biraz düştü (ağ artık sınırda şekil demeye daha yatkın),
  ama karenin IoU'su 0,12'den 0,70'e çıktı; mIoU 0,58'den 0,78'e.
- Dice değerleri IoU'dan yüksek, sıraları aynı.

Başka çareler: Dice kaybı (doğrudan örtüşmeyi büyütür), zor pikselleri öne
çıkaran odak kaybı (focal loss), az görülen sınıfı içeren resimleri daha sık
örneklemek.

## Örnek bölütlemeden farkı

Bizim maskemizde iki kare yan yana dursa ikisi de "2" olur: anlamsal
bölütleme **sınıfı** söyler, **hangi nesne** olduğunu söylemez. Her nesneyi
ayrı numaralayan işe **örnek bölütleme** (instance segmentation) denir;
algılama ile bölütlemeyi birleştirir (her kutu için bir maske). Anlamsal ve
örnek bölütlemeyi birleştiren işe de **panoptik bölütleme** denir.

## Özet

- Bölütleme her piksele sınıf verir; hedef `(N, H, W)` tam sayı maske.
- Kodlayıcı–çözücü: küçült (bağlam), ters evrişimle büyüt (konum), 1 × 1
  evrişimle sınıf puanları; `CrossEntropyLoss` her pikselde.
- Piksel doğruluğu dengesiz veride yanıltır: hep arka plan %90.
- Sınıf başına IoU, mIoU ve Dice küçük sınıfın sorununu gösterir.
- Sınıf ağırlıkları küçük sınıfların hatasını pahalılaştırır.
