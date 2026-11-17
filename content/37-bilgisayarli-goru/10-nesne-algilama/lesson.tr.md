# Nesne Algılamaya Giriş

Şimdiye kadar her resimde tek bir şekil vardı ve soru "hangisi?" idi.
Gerçek resimlerde birden çok nesne olur: bir sokak fotoğrafında insanlar,
arabalar, bisikletler. **Nesne algılama** (object detection) iki soruyu
birden cevaplar: **ne** var ve **nerede**? Cevap bir liste: her nesne için
bir **sınırlayıcı kutu** (bounding box), bir sınıf ve bir **güven puanı**
(confidence). Videoda insanları sayan ya da takip eden sistemler bu listeyi
her karede üretir. Bu bölümde kutuları tanıyacağız: nasıl yazıldıklarını,
nasıl karşılaştırıldıklarını (IoU) ve resim değişince nasıl güncellendiklerini.

## Sahneler ve kutular

`make_scenes` birden çok şekil içeren 32 × 32 sahneler üretiyor. Her sahne
için kutuların listesi geliyor: `[x1, y1, x2, y2, sınıf]`. `x` sütun, `y`
satır; `(x1, y1)` sol üst köşe, `(x2, y2)` sağ alt köşe (bu iki değer kutuya
**dahil değil**: son pikselin bir fazlası).

```python
import torch
from dl_data import make_scenes, SHAPES

images, boxes, masks = make_scenes(100, size=32, seed=7)
print(images.shape)
print(boxes[0])
counts = torch.bincount(torch.tensor([len(b) for b in boxes]))
print(counts.tolist())
```

```text
(100, 1, 32, 32)
[[17, 7, 26, 16, 1], [21, 20, 27, 27, 0], [8, 7, 15, 15, 2]]
[0, 38, 27, 35]
```

- İlk sahnede üç nesne var; her biri bir kutu ve bir sınıf numarası.
- Sahnelerde 1, 2 ya da 3 nesne bulunuyor. Liste uzunluğu resimden resme
  değiştiği için kutular tek bir tensör değil, bir **liste** olarak tutuluyor.

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="371.52pt" height="92.034783pt" viewBox="0 0 371.52 92.034783" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 92.034783 
L 371.52 92.034783 
L 371.52 -0 
L 0 -0 
L 0 92.034783 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g clip-path="url(#p1efc4b1fc3)">
    <image xlink:href="data:image/png;base64,
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" id="imagefa31a97080" transform="scale(1 -1) translate(0 -77.76)" x="7.2" y="-7.074783" width="77.76" height="77.76"/>
   </g>
   <g id="patch_2">
    <path d="M 48.443478 24.182609 
L 70.278261 24.182609 
L 70.278261 46.017391 
L 48.443478 46.017391 
L 48.443478 24.182609 
z
" clip-path="url(#p1efc4b1fc3)" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
   <g id="patch_3">
    <path d="M 58.147826 55.721739 
L 72.704348 55.721739 
L 72.704348 72.704348 
L 58.147826 72.704348 
L 58.147826 55.721739 
z
" clip-path="url(#p1efc4b1fc3)" style="fill: none; stroke: #9467bd; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
   <g id="patch_4">
    <path d="M 26.608696 24.182609 
L 43.591304 24.182609 
L 43.591304 43.591304 
L 26.608696 43.591304 
L 26.608696 24.182609 
z
" clip-path="url(#p1efc4b1fc3)" style="fill: none; stroke: #2ca02c; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
  </g>
  <g id="axes_2">
   <g clip-path="url(#pb65197308e)">
    <image xlink:href="data:image/png;base64,
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" id="imagec0d7aeba41" transform="scale(1 -1) translate(0 -77.76)" x="100.08" y="-7.074783" width="77.76" height="77.76"/>
   </g>
   <g id="patch_5">
    <path d="M 141.605217 24.182609 
L 161.013913 24.182609 
L 161.013913 46.017391 
L 141.605217 46.017391 
L 141.605217 24.182609 
z
" clip-path="url(#pb65197308e)" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
   <g id="patch_6">
    <path d="M 127.048696 53.295652 
L 144.031304 53.295652 
L 144.031304 70.278261 
L 127.048696 70.278261 
L 127.048696 53.295652 
z
" clip-path="url(#pb65197308e)" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
   <g id="patch_7">
    <path d="M 139.17913 38.73913 
L 163.44 38.73913 
L 163.44 60.573913 
L 139.17913 60.573913 
L 139.17913 38.73913 
z
" clip-path="url(#pb65197308e)" style="fill: none; stroke: #2ca02c; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
  </g>
  <g id="axes_3">
   <g clip-path="url(#p32ce17a9bc)">
    <image xlink:href="data:image/png;base64,
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" id="imagea14e5026e8" transform="scale(1 -1) translate(0 -77.76)" x="193.68" y="-7.074783" width="77.76" height="77.76"/>
   </g>
   <g id="patch_8">
    <path d="M 227.488696 38.73913 
L 249.323478 38.73913 
L 249.323478 60.573913 
L 227.488696 60.573913 
L 227.488696 38.73913 
z
" clip-path="url(#p32ce17a9bc)" style="fill: none; stroke: #2ca02c; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
  </g>
  <g id="axes_4">
   <g clip-path="url(#p55762b2e18)">
    <image xlink:href="data:image/png;base64,
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" id="image8cd93ba0f8" transform="scale(1 -1) translate(0 -77.76)" x="286.56" y="-7.074783" width="77.76" height="77.76"/>
   </g>
   <g id="patch_9">
    <path d="M 301.241739 21.756522 
L 325.502609 21.756522 
L 325.502609 46.017391 
L 301.241739 46.017391 
L 301.241739 21.756522 
z
" clip-path="url(#p55762b2e18)" style="fill: none; stroke: #2ca02c; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
   <g id="patch_10">
    <path d="M 301.241739 26.608696 
L 320.650435 26.608696 
L 320.650435 43.591304 
L 301.241739 43.591304 
L 301.241739 26.608696 
z
" clip-path="url(#p55762b2e18)" style="fill: none; stroke: #2ca02c; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p1efc4b1fc3">
   <rect x="7.2" y="7.2" width="77.634783" height="77.634783"/>
  </clipPath>
  <clipPath id="pb65197308e">
   <rect x="100.361739" y="7.2" width="77.634783" height="77.634783"/>
  </clipPath>
  <clipPath id="p32ce17a9bc">
   <rect x="193.523478" y="7.2" width="77.634783" height="77.634783"/>
  </clipPath>
  <clipPath id="p55762b2e18">
   <rect x="286.685217" y="7.2" width="77.634783" height="77.634783"/>
  </clipPath>
 </defs>
</svg>
<figcaption>İlk dört sahne ve kutuları: mor daire, turuncu kare, yeşil üçgen.</figcaption>
</figure>

## Kutu biçimleri

Aynı kutu üç farklı biçimde yazılabilir; algılama kütüphaneleri farklı
biçimler kullanır ve karıştırmak en sık hatalardan biridir:

- **xyxy:** sol üst ve sağ alt köşe: `[x1, y1, x2, y2]`.
- **xywh:** sol üst köşe, genişlik ve yükseklik: `[x1, y1, w, h]`.
- **cxcywh:** merkez, genişlik ve yükseklik: `[cx, cy, w, h]`. YOLO ailesi
  bunu kullanır.

```python
from torchvision.ops import box_convert

box = torch.tensor([[4.0, 6.0, 14.0, 12.0]])
x1, y1, x2, y2 = box[0].tolist()
print([x1, y1, x2 - x1, y2 - y1])
print([(x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1])
print(box_convert(box, "xyxy", "xywh").tolist())
print(box_convert(box, "xyxy", "cxcywh").tolist())
```

```text
[4.0, 6.0, 10.0, 6.0]
[9.0, 9.0, 10.0, 6.0]
[[4.0, 6.0, 10.0, 6.0]]
[[9.0, 9.0, 10.0, 6.0]]
```

Elle yaptığımız dönüşüm torchvision'ın `box_convert`'iyle aynı. Bir kütüphane
kutu döndürdüğünde ilk soru hep şu olmalı: **hangi biçimde?**

## Kesişim bölü birleşim (IoU)

İki kutunun ne kadar örtüştüğünü ölçmenin standart yolu **IoU**
(intersection over union): ortak alan ÷ toplam alan. Tam üst üste binen
kutularda 1, hiç değmeyenlerde 0.

```python
def area(b):
    return max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])


def iou(a, b):
    inter = [max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])]
    common = area(inter)
    return common / (area(a) + area(b) - common)


truth = [10, 10, 20, 20]
print(iou(truth, [10, 10, 20, 20]))
print(round(iou(truth, [15, 10, 25, 20]), 3))
print(round(iou(truth, [12, 12, 22, 22]), 3))
print(iou(truth, [30, 30, 40, 40]))
```

```text
1.0
0.333
0.471
0.0
```

- Ortak bölge, iki kutunun sol üst köşelerinin **büyüğü** ile sağ alt
  köşelerinin **küçüğü** arasında kalan kutu. Kutular değmiyorsa bu kutunun
  genişliği eksi çıkar; `max(0, ...)` onu sıfıra indiriyor.
- Yarısı örtüşen iki eşit kutunun IoU'su 0,5 değil, **1/3**: ortak alan 50,
  birleşim 100 + 100 − 50 = 150.
- İki kenardan 2 piksel kaymak bile IoU'yu 0,47'ye düşürüyor. IoU sert bir
  ölçü: küçük nesnelerde birkaç piksellik hata büyük fark yaratır.

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="349.2pt" height="125.708479pt" viewBox="0 0 349.2 125.708479" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 125.708479 
L 349.2 125.708479 
L 349.2 0 
L 0 0 
L 0 125.708479 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 7.2 118.508479 
L 105.670588 118.508479 
L 105.670588 20.037891 
L 7.2 20.037891 
L 7.2 118.508479 
z
" style="fill: none"/>
   </g>
   <g id="patch_3">
    <path d="M 20.506836 33.344727 
L 47.120509 33.344727 
L 47.120509 59.958399 
L 20.506836 59.958399 
L 20.506836 33.344727 
z
" clip-path="url(#p6e0bd2c647)" style="fill: none; stroke: #9467bd; stroke-width: 2; stroke-linejoin: miter"/>
   </g>
   <g id="patch_4">
    <path d="M 33.813672 33.344727 
L 60.427345 33.344727 
L 60.427345 59.958399 
L 33.813672 59.958399 
L 33.813672 33.344727 
z
" clip-path="url(#p6e0bd2c647)" style="fill: none; stroke: #ff7f0e; stroke-width: 2; stroke-linejoin: miter"/>
   </g>
   <g id="matplotlib.axis_1"/>
   <g id="matplotlib.axis_2"/>
   <g id="patch_5">
    <path d="M 7.2 118.508479 
L 7.2 20.037891 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 105.670588 118.508479 
L 105.670588 20.037891 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_7">
    <path d="M 7.2 118.508479 
L 105.670588 118.508479 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_8">
    <path d="M 7.2 20.037891 
L 105.670588 20.037891 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_1">
    <text style="font-size: 9px; font-family:inherit; text-anchor: middle; fill: currentColor" x="56.435294" y="14.037891" transform="rotate(-0 56.435294 14.037891)">IoU = 1/3</text>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_9">
    <path d="M 125.364706 118.508479 
L 223.835294 118.508479 
L 223.835294 20.037891 
L 125.364706 20.037891 
L 125.364706 118.508479 
z
" style="fill: none"/>
   </g>
   <g id="patch_10">
    <path d="M 138.671542 33.344727 
L 165.285215 33.344727 
L 165.285215 59.958399 
L 138.671542 59.958399 
L 138.671542 33.344727 
z
" clip-path="url(#p40495c46c4)" style="fill: none; stroke: #9467bd; stroke-width: 2; stroke-linejoin: miter"/>
   </g>
   <g id="patch_11">
    <path d="M 143.994277 38.667461 
L 170.607949 38.667461 
L 170.607949 65.281134 
L 143.994277 65.281134 
L 143.994277 38.667461 
z
" clip-path="url(#p40495c46c4)" style="fill: none; stroke: #ff7f0e; stroke-width: 2; stroke-linejoin: miter"/>
   </g>
   <g id="matplotlib.axis_3"/>
   <g id="matplotlib.axis_4"/>
   <g id="patch_12">
    <path d="M 125.364706 118.508479 
L 125.364706 20.037891 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_13">
    <path d="M 223.835294 118.508479 
L 223.835294 20.037891 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_14">
    <path d="M 125.364706 118.508479 
L 223.835294 118.508479 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_15">
    <path d="M 125.364706 20.037891 
L 223.835294 20.037891 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_2">
    <text style="font-size: 9px; font-family:inherit; text-anchor: middle; fill: currentColor" x="174.6" y="14.037891" transform="rotate(-0 174.6 14.037891)">IoU = 0.47</text>
   </g>
  </g>
  <g id="axes_3">
   <g id="patch_16">
    <path d="M 243.529412 118.508479 
L 342 118.508479 
L 342 20.037891 
L 243.529412 20.037891 
L 243.529412 118.508479 
z
" style="fill: none"/>
   </g>
   <g id="patch_17">
    <path d="M 256.836248 33.344727 
L 283.449921 33.344727 
L 283.449921 59.958399 
L 256.836248 59.958399 
L 256.836248 33.344727 
z
" clip-path="url(#pc7053ffcd3)" style="fill: none; stroke: #9467bd; stroke-width: 2; stroke-linejoin: miter"/>
   </g>
   <g id="patch_18">
    <path d="M 310.063593 86.572072 
L 336.677266 86.572072 
L 336.677266 113.185744 
L 310.063593 113.185744 
L 310.063593 86.572072 
z
" clip-path="url(#pc7053ffcd3)" style="fill: none; stroke: #ff7f0e; stroke-width: 2; stroke-linejoin: miter"/>
   </g>
   <g id="matplotlib.axis_5"/>
   <g id="matplotlib.axis_6"/>
   <g id="patch_19">
    <path d="M 243.529412 118.508479 
L 243.529412 20.037891 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_20">
    <path d="M 342 118.508479 
L 342 20.037891 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_21">
    <path d="M 243.529412 118.508479 
L 342 118.508479 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_22">
    <path d="M 243.529412 20.037891 
L 342 20.037891 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_3">
    <text style="font-size: 9px; font-family:inherit; text-anchor: middle; fill: currentColor" x="292.764706" y="14.037891" transform="rotate(-0 292.764706 14.037891)">IoU = 0</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p6e0bd2c647">
   <rect x="7.2" y="20.037891" width="98.470588" height="98.470588"/>
  </clipPath>
  <clipPath id="p40495c46c4">
   <rect x="125.364706" y="20.037891" width="98.470588" height="98.470588"/>
  </clipPath>
  <clipPath id="pc7053ffcd3">
   <rect x="243.529412" y="20.037891" width="98.470588" height="98.470588"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Gerçek kutu (mor) ve üç tahmin (turuncu): yarı örtüşme, 2 piksel kayma, hiç değmeme.</figcaption>
</figure>

## Bütün çiftler: box_iou

Bir algılayıcı birden çok kutu tahmin eder ve resimde birden çok gerçek kutu
vardır. `torchvision.ops.box_iou` bütün çiftlerin IoU'sunu tek bir matris
olarak veriyor: satır tahmin, sütun gerçek kutu.

```python
from torchvision.ops import box_iou

truth_boxes = torch.tensor([[10.0, 10, 20, 20], [0, 0, 6, 6]])
predicted = torch.tensor([[11.0, 10, 21, 20], [1, 1, 6, 7], [25, 25, 30, 30]])
matrix = box_iou(predicted, truth_boxes)
print(matrix.shape)
for row in matrix.tolist():
    print([round(v, 2) for v in row])
print([round(v, 2) for v in matrix.max(dim=1).values.tolist()])
```

```text
torch.Size([3, 2])
[0.82, 0.0]
[0.0, 0.61]
[0.0, 0.0]
[0.82, 0.61, 0.0]
```

- İlk tahmin birinci gerçek kutuyla, ikinci tahmin ikinci gerçek kutuyla
  örtüşüyor; üçüncü tahminin hiçbir gerçek kutuyla ortak alanı yok.
- Her tahminin en iyi IoU'su (`max(dim=1)`) bir sonraki bölümün konusunun
  başlangıcı: bir tahmin "doğru" sayılmak için genellikle IoU ≥ 0,5 ister.

## Resim değişince kutu da değişir

Resmi büyütür, küçültür ya da kırparsan kutuları da aynı dönüşümle
güncellemen gerekir; yoksa kutular yanlış yeri gösterir. Büyütmede
koordinatlar aynı oranla çarpılır; kesilen resimde kutular resmin içine
kırpılır:

```python
from torchvision.ops import clip_boxes_to_image

b = torch.tensor([[4.0, 6.0, 14.0, 12.0], [25.0, 20.0, 36.0, 30.0]])
scale = 64 / 32
print((b * scale).tolist())
print(clip_boxes_to_image(b, (32, 32)).tolist())
```

```text
[[8.0, 12.0, 28.0, 24.0], [50.0, 40.0, 72.0, 60.0]]
[[4.0, 6.0, 14.0, 12.0], [25.0, 20.0, 32.0, 30.0]]
```

- 32 × 32'lik resmi 64 × 64'e büyütünce bütün koordinatlar iki katına çıktı.
- İkinci kutu resmin sağından taşıyordu (`x2 = 36`); `clip_boxes_to_image`
  onu resmin sınırına (32) çekti. `(32, 32)` resmin (yükseklik, genişlik)
  boyutu.

## Özet

- Algılayıcının çıktısı: her nesne için kutu, sınıf ve güven puanı.
- Biçimler: xyxy, xywh, cxcywh; `box_convert` arasında çevirir.
- IoU = ortak alan ÷ birleşim; `box_iou` bütün çiftleri verir.
- Resim dönüşünce kutu da dönüşür: ölçekle, sınırlara kırp.
