# Bitirme: Şekil Algılayıcı

Bu modülde parça parça kurduklarımızı birleştirip **kendi algılayıcımızı**
sıfırdan eğiteceğiz: sahnelerdeki daireleri, kareleri ve üçgenleri hem
**bulan** (kutu) hem **tanıyan** (sınıf) küçük bir YOLO benzeri ağ. Yol
haritası:

1. Veri ve hedef tensörü (YOLO Mantığı bölümü).
2. Izgara çıktısı veren bir CNN (İlk CNN bölümü).
3. Üç parçalı kayıp: nesnellik, kutu, sınıf.
4. Eğitim.
5. Çözme, güven eşiği ve sınıfa göre NMS (NMS bölümü).
6. Kesinlik ve duyarlılık ile değerlendirme; hataların nereden geldiği.

## 1. Veri ve hedef

600 sahne: 500 eğitim, 100 test. Izgara 4 × 4, her hücre 8 × 8 piksel.
Hedef tensörü YOLO Mantığı'ndaki gibi; tek fark, aynı hücreye ikinci bir
nesne merkezi düşerse onu **sayıyoruz**: bu basit biçimde ikinci nesne
kaybolur.

```python
import torch
import torch.nn.functional as F
from torch import nn
from torchvision.ops import batched_nms, box_iou
from dl_data import make_scenes, SHAPES

S, SIZE, C = 4, 32, 3
CELL = SIZE / S
images, boxes, masks = make_scenes(600, size=SIZE, seed=7)


def encode(scene):
    target = torch.zeros(S, S, 5 + C)
    lost = 0
    for x1, y1, x2, y2, label in scene:
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        row, col = int(cy // CELL), int(cx // CELL)
        if target[row, col, 0] == 1:
            lost += 1
        target[row, col] = 0
        target[row, col, 0] = 1
        target[row, col, 1:3] = torch.tensor([cx / CELL - col, cy / CELL - row])
        target[row, col, 3:5] = torch.tensor([(x2 - x1) / SIZE, (y2 - y1) / SIZE])
        target[row, col, 5 + label] = 1
    return target, lost


encoded = [encode(scene) for scene in boxes]
x = torch.tensor(images)
y = torch.stack([target for target, lost in encoded])
lost = sum(lost for target, lost in encoded)
objects = sum(len(scene) for scene in boxes)
print(x.shape, y.shape)
print(objects, lost, round(lost / objects, 3))
x_train, y_train, x_test, y_test = x[:500], y[:500], x[500:], y[500:]
test_boxes = boxes[500:]
```

```text
torch.Size([600, 1, 32, 32]) torch.Size([600, 4, 4, 8])
1232 87 0.071
```

- 1232 nesnenin 87'si (%7) başka bir nesneyle aynı hücreye düşüyor ve hedefte
  yer bulamıyor. Bu nesneleri model **hiçbir eşikte** bulamaz: algılayıcının
  tavanı daha veriye bakarken belli.
- Hücreye ikinci nesne gelince eskisinin sınıfı da silinsin diye hücre önce
  sıfırlanıyor (`target[row, col] = 0`).

## 2. Izgara çıktısı veren ağ

Üç evrişim + havuzlama 32'yi 16'ya, 8'e, 4'e indiriyor: tam da ızgaranın boyu.
Son katman 1 × 1 evrişimle her hücreye 5 + C = 8 sayı veriyor. Ağın çıktısı
`(N, 8, 4, 4)`; hedefle karşılaştırmak için kanal eksenini sona alacağız
(`permute`).

```python
def make_model():
    torch.manual_seed(0)
    return nn.Sequential(
        nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(32, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(32, 5 + C, 1),
    )


model = make_model()
print(model(x[:2]).shape, model(x[:2]).permute(0, 2, 3, 1).shape)
print(sum(p.numel() for p in model.parameters()))
```

```text
torch.Size([2, 8, 4, 4]) torch.Size([2, 4, 4, 8])
14312
```

Yalnızca 14 bin parametre: hazır algılayıcıların milyonlarca parametresinin
yanında çok küçük, ama bu sahneler için yeterli.

## 3. Üç parçalı kayıp

Her hücrenin sekiz sayısı üç ayrı soruya cevap veriyor; her soru kendi kaybıyla
ölçülüyor:

- **Nesnellik** (her hücrede): ikili çapraz entropi (`binary_cross_entropy_with_logits`).
- **Kutu** (yalnızca nesnesi olan hücrelerde): dört sayı 0–1 arası olduğu için
  `sigmoid`'den geçip ortalama kare hata. Nesnesi olmayan hücrenin kutusu
  anlamsız; ona ceza verilmez.
- **Sınıf** (yalnızca nesnesi olan hücrelerde): çapraz entropi.

```python
def detection_loss(output, target):
    output = output.permute(0, 2, 3, 1)
    has_object = target[..., 0] == 1
    objectness = F.binary_cross_entropy_with_logits(output[..., 0], target[..., 0])
    box_pred = torch.sigmoid(output[..., 1:5][has_object])
    box = F.mse_loss(box_pred, target[..., 1:5][has_object])
    labels = target[..., 5:][has_object].argmax(dim=1)
    label = F.cross_entropy(output[..., 5:][has_object], labels)
    return objectness + 5 * box + label


print(int(y_train[:32, ..., 0].sum().item()), 32 * S * S)
print(round(detection_loss(model(x_train[:32]), y_train[:32]).item(), 1))
```

```text
52 512
2.2
```

- İlk 32 sahnenin 512 hücresinden yalnızca 52'sinde nesne var; kutu ve sınıf
  kaybı bu 52 hücreden hesaplanıyor.
- Kutu kaybı `5 ×` ile büyütüldü: değerleri küçük (0–1 arası kare farklar)
  ve öbür ikisinin yanında kayboluyordu. Bu katsayılar algılayıcı
  tasarımının ayarlanan parçalarıdır.
- Eğitilmemiş ağda kayıp 2,2.

## 4. Eğitim

```python
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
generator = torch.Generator().manual_seed(1)
history = []
for epoch in range(30):
    order = torch.randperm(500, generator=generator)
    total = 0.0
    for start in range(0, 500, 32):
        batch = order[start:start + 32]
        optimizer.zero_grad()
        loss = detection_loss(model(x_train[batch]), y_train[batch])
        loss.backward()
        optimizer.step()
        total += loss.item() * len(batch)
    history.append(total / 500)
model.eval()
print(len(history), history[-1] < history[0] / 3)
```

```text
30 True
```

30 turdan sonra ortalama kayıp ilk turun üçte birinin altında.

## 5. Algılamak: çöz, eşikle, NMS

```python
def detect(image, threshold=0.5, iou=0.5):
    with torch.no_grad():
        output = model(image[None])[0].permute(1, 2, 0)
    objectness = torch.sigmoid(output[..., 0])
    probs = F.softmax(output[..., 5:], dim=-1)
    score, label = (objectness[..., None] * probs).max(dim=-1)
    rows, cols = torch.nonzero(score >= threshold, as_tuple=True)
    found = []
    for row, col in zip(rows.tolist(), cols.tolist()):
        ox, oy, w, h = torch.sigmoid(output[row, col, 1:5]).tolist()
        cx, cy = (col + ox) * CELL, (row + oy) * CELL
        w, h = w * SIZE, h * SIZE
        found.append([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2])
    if not found:
        return torch.zeros(0, 4), torch.zeros(0), torch.zeros(0, dtype=torch.long)
    found = torch.tensor(found)
    score, label = score[rows, cols], label[rows, cols]
    keep = batched_nms(found, score, label, iou)
    return found[keep], score[keep], label[keep]


found, score, label = detect(x_test[3])
print(sorted(SHAPES[k] for k in label.tolist()))
print(sorted(SHAPES[b[4]] for b in test_boxes[3]))
```

```text
['square', 'square', 'triangle']
['square', 'square', 'triangle']
```

Dördüncü test sahnesinde (iki kare, bir üçgen) algılayıcı üç nesneyi de doğru
sınıflarla buldu; şekilde kutuları da görülüyor.

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
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" id="imageeec54f7f1e" transform="scale(1 -1) translate(0 -77.76)" x="7.2" y="-7.074783" width="77.76" height="77.76"/>
   </g>
   <g id="patch_2">
    <path d="M 16.904348 14.478261 
L 41.165217 14.478261 
L 41.165217 36.313043 
L 16.904348 36.313043 
L 16.904348 14.478261 
z
" clip-path="url(#p1efc4b1fc3)" style="fill: none; stroke-dasharray: 3.7,1.6; stroke-dashoffset: 0; stroke: #ffffff; stroke-linejoin: miter"/>
   </g>
   <g id="patch_3">
    <path d="M 26.608696 24.182609 
L 41.165217 24.182609 
L 41.165217 38.73913 
L 26.608696 38.73913 
L 26.608696 24.182609 
z
" clip-path="url(#p1efc4b1fc3)" style="fill: none; stroke-dasharray: 3.7,1.6; stroke-dashoffset: 0; stroke: #ffffff; stroke-linejoin: miter"/>
   </g>
   <g id="patch_4">
    <path d="M 29.034783 55.721739 
L 53.295652 55.721739 
L 53.295652 77.556522 
L 29.034783 77.556522 
L 29.034783 55.721739 
z
" clip-path="url(#p1efc4b1fc3)" style="fill: none; stroke-dasharray: 3.7,1.6; stroke-dashoffset: 0; stroke: #ffffff; stroke-linejoin: miter"/>
   </g>
   <g id="patch_5">
    <path d="M 31.219981 57.161127 
L 51.085683 57.161127 
L 51.085683 76.686012 
L 31.219981 76.686012 
L 31.219981 57.161127 
z
" clip-path="url(#p1efc4b1fc3)" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
   <g id="patch_6">
    <path d="M 22.835193 19.443038 
L 39.320239 19.443038 
L 39.320239 34.484075 
L 22.835193 34.484075 
L 22.835193 19.443038 
z
" clip-path="url(#p1efc4b1fc3)" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
   <g id="patch_7">
    <path d="M 20.66402 16.320747 
L 39.201807 16.320747 
L 39.201807 33.681461 
L 20.66402 33.681461 
L 20.66402 16.320747 
z
" clip-path="url(#p1efc4b1fc3)" style="fill: none; stroke: #2ca02c; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
  </g>
  <g id="axes_2">
   <g clip-path="url(#pb65197308e)">
    <image xlink:href="data:image/png;base64,
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" id="image48eeee268d" transform="scale(1 -1) translate(0 -77.76)" x="100.08" y="-7.074783" width="77.76" height="77.76"/>
   </g>
   <g id="patch_8">
    <path d="M 122.196522 29.034783 
L 139.17913 29.034783 
L 139.17913 46.017391 
L 122.196522 46.017391 
L 122.196522 29.034783 
z
" clip-path="url(#pb65197308e)" style="fill: none; stroke-dasharray: 3.7,1.6; stroke-dashoffset: 0; stroke: #ffffff; stroke-linejoin: miter"/>
   </g>
   <g id="patch_9">
    <path d="M 148.883478 16.904348 
L 170.718261 16.904348 
L 170.718261 41.165217 
L 148.883478 41.165217 
L 148.883478 16.904348 
z
" clip-path="url(#pb65197308e)" style="fill: none; stroke-dasharray: 3.7,1.6; stroke-dashoffset: 0; stroke: #ffffff; stroke-linejoin: miter"/>
   </g>
   <g id="patch_10">
    <path d="M 119.770435 48.443478 
L 139.17913 48.443478 
L 139.17913 67.852174 
L 119.770435 67.852174 
L 119.770435 48.443478 
z
" clip-path="url(#pb65197308e)" style="fill: none; stroke-dasharray: 3.7,1.6; stroke-dashoffset: 0; stroke: #ffffff; stroke-linejoin: miter"/>
   </g>
   <g id="patch_11">
    <path d="M 120.21671 44.400899 
L 140.917207 44.400899 
L 140.917207 65.12439 
L 120.21671 65.12439 
L 120.21671 44.400899 
z
" clip-path="url(#pb65197308e)" style="fill: none; stroke: #2ca02c; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
   <g id="patch_12">
    <path d="M 115.783297 30.39624 
L 133.58454 30.39624 
L 133.58454 47.908288 
L 115.783297 47.908288 
L 115.783297 30.39624 
z
" clip-path="url(#pb65197308e)" style="fill: none; stroke: #2ca02c; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
   <g id="patch_13">
    <path d="M 150.700253 20.717616 
L 169.467601 20.717616 
L 169.467601 39.007401 
L 150.700253 39.007401 
L 150.700253 20.717616 
z
" clip-path="url(#pb65197308e)" style="fill: none; stroke: #9467bd; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
  </g>
  <g id="axes_3">
   <g clip-path="url(#p32ce17a9bc)">
    <image xlink:href="data:image/png;base64,
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" id="image29bd2730c0" transform="scale(1 -1) translate(0 -77.76)" x="193.68" y="-7.074783" width="77.76" height="77.76"/>
   </g>
   <g id="patch_14">
    <path d="M 198.375652 60.573913 
L 217.784348 60.573913 
L 217.784348 79.982609 
L 198.375652 79.982609 
L 198.375652 60.573913 
z
" clip-path="url(#p32ce17a9bc)" style="fill: none; stroke-dasharray: 3.7,1.6; stroke-dashoffset: 0; stroke: #ffffff; stroke-linejoin: miter"/>
   </g>
   <g id="patch_15">
    <path d="M 234.766957 24.182609 
L 261.453913 24.182609 
L 261.453913 50.869565 
L 234.766957 50.869565 
L 234.766957 24.182609 
z
" clip-path="url(#p32ce17a9bc)" style="fill: none; stroke-dasharray: 3.7,1.6; stroke-dashoffset: 0; stroke: #ffffff; stroke-linejoin: miter"/>
   </g>
   <g id="patch_16">
    <path d="M 197.702097 58.786517 
L 218.184506 58.786517 
L 218.184506 78.567746 
L 197.702097 78.567746 
L 197.702097 58.786517 
z
" clip-path="url(#p32ce17a9bc)" style="fill: none; stroke: #2ca02c; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
   <g id="patch_17">
    <path d="M 237.065679 26.321553 
L 257.734724 26.321553 
L 257.734724 46.536835 
L 237.065679 46.536835 
L 237.065679 26.321553 
z
" clip-path="url(#p32ce17a9bc)" style="fill: none; stroke: #9467bd; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
  </g>
  <g id="axes_4">
   <g clip-path="url(#p55762b2e18)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAGwAAABsCAYAAACPZlfNAAAI3klEQVR4nO2dSW8USRCF3Qu4jW0MzQ5iORhxQuIXIARHnxBn/h8HTvwFDvwBQBwAsRqbxSwGjI2NkQ9T8+WjIibpsUYTJt6p7MrurqpUvnjxMjKrMzY2tjkGdDqd5nhzszhV4MCBA83xyspKc/z169ei3Z49e8xzxPj4uPm7a2trzfHu3btb/z8qut2u+TevY2Njo+r7du3aVfz9/fv35nh6ero49/nz5+a43++3fuaX6626isT/BtlhwfD3OPwHGhwOh+Zw5hDm0P4drK6uVrVbc2jQol/SrdLWt2/finPr6+vN8WAw+G1KJGXrs/Gune30enlfOcKCITssGLLDgmFLwxdBy5LNGpvI9Z6sZUy0PqM87bXrQnZrO/49OTlpxh/GCy829Xq9qnYemCZpfOM9UxPwM/pMc4QFQ3ZYdEocBaSpHz9+mO32799f/P3+/ftWylVZS6pbdeQ/aZA0cuTIkaLdkydPzO+rvRfSJamOro+e0+/zqN9CjrBgyA6LTomkLVKWBzoC6hxYNOIpLzVkVV1Zv7V3797m+NOnT2M1oFLTa1xeXjaVG9UvjXA1br3ruHDhQnN8//590xFJlRgYSYnBkB22U2W9Sm3KYSvG6Oe+fPlSnJuYmGjlbW8Cz8PDhw+b40OHDpnSnd/vTTjymjTWvX79ujWGzc7OmnHWSxNqkSMsGLLDguGX2UZSBKnuxo0bRbuZmZnWVODRo0dFO36HToIuLS21ymal32vXrlWlGlNTU1X1GJTuSlP79u1rNWSfPXtWtDt69GjrM/PqVmqhIYbUnCMsGLLDgiE7LHoMo6zlMTl7C3fv3m2OT548afIv44BX5/ju3bvm+Pr168U51vONI76pXGesYqyjZaWWk9pARcELLDJ1/CnXGZu19pDXWFtHqbGecTFHWDBkhwVDXx100gAp8fLly0W7mzdvtjoYdBi2cPjw4eb46dOnxbkzZ85UXSQpbAi6UEo8ePBgK8UuLCwU7UiRdFt0UpGTkbwGTWV4/+rmeO7GiRMnWlMcvS86/jnCgiE7LBj66gLUTipyqHM4q8IhDaqC4lCfm5urmiBdwm8pPnz40EorqvBevHjRHJ86dao4d+/eveb4/PnzrS6KOjP8LY8CGR628PLly9Z71LoQfi5HWDBkhwVDdlgwdAaDgVmEw3jGCTvF7du3zXN0Jhg71Bln2sCZAHVLNpySabobVozdAlMZjbmU5UxrPn78WLRjXGSMoVTXeKTxjTHcW/nK1CNHWDBkhwVDX2v7FhcXW4emOgIc6t4qF9LR8ePHi3MXL16sqgupXTmyCnlNp0MdFboW3goYUraWmZPeWPr96tUrMyR498EwwPREn3WOsGDIDguGvpYgc6h7pWIcpleuXGmO79y5YyqhN2/emGqN1KGUYGEAd0Aphwav0vTjx49N94H3z3kopWxeL5+TR+0e6CSpI0QKzxEWDNlhwZAdFj2GUcqTw2vLpzXWUSZfvXrV/BzbecuS+s5KTcYBrsZ88OBB0Y7phZZgE7wOTWsYZ/mcvLqNc+fOFX/Pz8+3fk7lf26sEhhJicHQ58oLld5an2CB1HTp0qXi3K1bt35byqpZS/neA02pIUsjlxSjaQIdDKV60g9rQbTMj587duxY6zVo+vP8+fPinOUQeatYc4QFQ3ZYMGSH7aQVmLR3VK6SZ1mgwslGXYqjE3i0cRgTtOCHMXJZ6gP/LXTCkVKb0ElFax8qjXWcNdBCHt6zPjeC8S1HWDBkhwVDp9frbVpDv3YRtVW2rJLc22SEUlsXiqvLb7kUpG06J97CcwVlOalOUwiCLohSpyfRLdCl0WeaIywYssOCoTM5OblpKTI6DjrRZy2KUyVUTL6J+qP6If2qImW7DsxqrccgHXkL/7yXH9C18FaU8D6tSU+lWG9li0fTdIFyhAVDdlgwZIdFdzrIl3SaNV4wlrBsmZm9xgtNEyzXQidVrZ2pN5wNUyinPZmsqQElut7Ldu+4zZSH16FpSNYlBkZSYvTVK6Qfr86AEp30oNKdcphuhlIi6UEpkcZoz6hl1Gvk73q7eSusFy1orSBp1XOERtnW1kOOsGDIDguGvmbYHN7eVkNcbeFRDBd96xZ21n4Z3pzXhlHy5m19p5TlKTyqNVKiXhOVHN0MVZa183csvdM5uZwPC4ykxGDIDguGTrfbLQLVduz8TFBSa30gHQivpoGpQtdIJ7bAGku208XwdNp1Afzbt29bY7i2o6xn7NSaDqYXmvIw3nkv1clS7cBIStxJZW6Uk7XvuvJ2hPZgyWn9znG4G5pO1BqytS/3IdRV4bMhPSp1erUgBCeIvT1RcoQFQ3ZYdEr0qni3G3QLvJoGuiAdGMPepv50H5T2vM+R+nh93rOgElYl6P0uqZmKVN0R0nuOsGDIDguG7LDoMYyylHJVnXHGBfK+SnK6GToxSa7m72pNA92HaUwkaq0GV0xaE5EK3QWcbWsluQfes24Ew1oNpjXeCxRyhAVDdthOcjpqnQOWN+v2cx5YHkfa836r4+zcWQtux8et87TupHbPK6+Ub5TVK3xhgj6bHGHBkB0WDNlh0esSKdFrZS3tGOVwymYtUKmdLLXiypQsbaKU994gwRRF4yDjJ9MLTTV4z/wOTSE8y6121oDPMEdYMGSHBUNnOBwWnEAq8VYxjiJ/dR8m0gfdcG8H7ylnNsFbWUnQIfH209qOFIK1l1qqrnWaf0H3/8pXKgZGUuKfWNNBR+Ts2bPFOToJSqsWzXi7pE6ALvU9WwTNZE/tqiFLtbYdK094L6dPnzafTe1kbo6wYMgOC4bssOivBaZTzBfnePV2lNMqVb0Mnr9N10N/i2nDihO3RoHWG/J6KfnVVWE7L74z/nopBAt5si5xByEp8U+ZwLRcAO/1wQpKdH6/V4MxjZoOpRhSM10Qj871nWZMPegwKBVbaYP3optRJzDpPuUIC4bssGD4T0u1VZGRLpnpe8atB8sF8dwMBe/f29W0luo8t4j0yRCjVJ9lboGRlBgM2WFjsfAT44faRMUWRIkAAAAASUVORK5CYII=" id="imaged1be666195" transform="scale(1 -1) translate(0 -77.76)" x="286.56" y="-7.074783" width="77.76" height="77.76"/>
   </g>
   <g id="patch_18">
    <path d="M 293.963478 48.443478 
L 315.798261 48.443478 
L 315.798261 70.278261 
L 293.963478 70.278261 
L 293.963478 48.443478 
z
" clip-path="url(#p55762b2e18)" style="fill: none; stroke-dasharray: 3.7,1.6; stroke-dashoffset: 0; stroke: #ffffff; stroke-linejoin: miter"/>
   </g>
   <g id="patch_19">
    <path d="M 323.076522 48.443478 
L 347.337391 48.443478 
L 347.337391 72.704348 
L 323.076522 72.704348 
L 323.076522 48.443478 
z
" clip-path="url(#p55762b2e18)" style="fill: none; stroke-dasharray: 3.7,1.6; stroke-dashoffset: 0; stroke: #ffffff; stroke-linejoin: miter"/>
   </g>
   <g id="patch_20">
    <path d="M 327.982281 53.026199 
L 343.570753 53.026199 
L 343.570753 67.234153 
L 327.982281 67.234153 
L 327.982281 53.026199 
z
" clip-path="url(#p55762b2e18)" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
   <g id="patch_21">
    <path d="M 294.368572 49.014869 
L 313.47564 49.014869 
L 313.47564 67.76454 
L 294.368572 67.76454 
L 294.368572 49.014869 
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
<figcaption>Dört test sahnesi: kesikli beyaz gerçek kutular, renkli algılayıcının kutuları (mor daire, turuncu kare, yeşil üçgen).</figcaption>
</figure>

## 6. Değerlendirmek

NMS ve Değerlendirme bölümündeki açgözlü eşleştirme, bu kez **sınıf da
tutmalı**: tahmin, aynı sınıftan ve henüz eşleşmemiş bir gerçek kutuyla
IoU ≥ 0,5 ise doğru pozitif.

```python
def evaluate(threshold=0.5):
    tp = fp = fn = 0
    matched_iou = []
    for index, scene in enumerate(test_boxes):
        found, score, label = detect(x_test[index], threshold)
        truth = torch.tensor([b[:4] for b in scene], dtype=torch.float32)
        used = set()
        for k in score.argsort(descending=True).tolist():
            overlaps = box_iou(found[k:k + 1], truth)[0]
            best, best_j = 0.0, -1
            for j, b in enumerate(scene):
                free = j not in used and b[4] == label[k].item()
                if free and overlaps[j].item() > best:
                    best, best_j = overlaps[j].item(), j
            if best >= 0.5:
                tp += 1
                used.add(best_j)
                matched_iou.append(best)
            else:
                fp += 1
        fn += len(scene) - len(used)
    mean_iou = sum(matched_iou) / len(matched_iou)
    return tp / (tp + fp), tp / (tp + fn), mean_iou


precision, recall, mean_iou = evaluate()
print(round(precision, 1), round(recall, 1), round(mean_iou, 1))
strict, loose = evaluate(0.7), evaluate(0.3)
print(strict[0] > loose[0], strict[1] < loose[1])
```

```text
0.8 0.7 0.7
True True
```

- Eşik 0,5'te kesinlik yaklaşık 0,8, duyarlılık yaklaşık 0,7; eşleşen
  kutuların IoU ortalaması yaklaşık 0,7.
- Eşiği yükseltmek (0,7) kesinliği artırıyor, duyarlılığı düşürüyor; eşiği
  indirmek (0,3) tersini yapıyor. Hangisinin seçileceği uygulamaya bağlı:
  kaçırmanın pahalı olduğu yerde düşük eşik.

## Hatalar nereden geliyor?

Kaçırılan nesnelerin bir kısmını model öğrenemezdi bile: hedefte yerleri yoktu.

```python
test_lost = sum(lost for target, lost in encoded[500:])
test_objects = sum(len(scene) for scene in test_boxes)
print(test_objects, test_lost)
```

```text
213 17
```

Test setindeki 213 nesnenin 17'si aynı hücreyi paylaştığı için hiçbir eşikte
bulunamaz; duyarlılığın tavanı bu yüzden 1 değil 0,92. Geri kalan
hatalar modelin kendi hataları: kutu biraz kaydığı için IoU 0,5'in altında
kalan tahminler, karıştırılan sınıflar, üst üste binen şekiller.

## Özet

- Algılayıcı: veri → hedef tensörü → ızgara çıktısı veren CNN → üç parçalı
  kayıp → eğitim → çözme + eşik + sınıfa göre NMS → kesinlik ve duyarlılık.
- Hedefin biçimi algılayıcının tavanını belirliyor (aynı hücredeki ikinci
  nesne).
- Kayıp parçalarının katsayıları ayarlanan tasarım kararlarıdır.
- Güven eşiği kesinlik ile duyarlılık arasında seçim yapar.
