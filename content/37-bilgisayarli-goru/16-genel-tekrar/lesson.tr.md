# Genel Tekrar

Bilgisayarlı Görü modülünün sonuna geldin. Bir resmin tensör olarak nasıl
durduğundan başlayıp evrişim, CNN, veri artırma, değerlendirme, hazır
mimariler, transfer öğrenme, nesne algılama, bölütleme ve modeli açıklamaya
kadar yürüdün; sonunda kendi algılayıcını eğittin. Bu bölüm yolu bir kez daha
yürüyor ve sonunda modelsiz bir **hat sağlaması** yapıyor.

<figure class="fig">
  <div class="flow">
    <span class="node">Resim ve evrişim</span><span class="arrow">→</span>
    <span class="node">CNN ve eğitim</span><span class="arrow">→</span>
    <span class="node">Hazır ağlar</span><span class="arrow">→</span>
    <span class="node">Algılama</span><span class="arrow">→</span>
    <span class="node acc">Bölütleme ve açıklama</span>
  </div>
  <figcaption>Modülün yolu: resmi ve evrişimi anla, CNN eğit ve ölç, hazır ağları kullan, nesneleri bul, piksel piksel ayır ve modelin kararını açıkla.</figcaption>
</figure>

## 1. Resim, evrişim, havuzlama

| Konu | Hatırla |
|---|---|
| Resim tensörü | PyTorch `(N, C, H, W)`; Pillow ve NumPy `(H, W, C)`; `ToTensor` / `ToImage` 0–1 aralığına |
| Evrişim | çekirdek resim üstünde kayar; çıktı boyu `(H + 2p − k) / s + 1`, aşağı yuvarlanır |
| Kanallar | `Conv2d(giriş, çıkış, k)`: her çıkış kanalı bütün giriş kanallarına bakar |
| Havuzlama | `MaxPool2d(2)` boyu yarıya indirir, küçük kaymalara dayanıklılık verir |
| Alıcı alan | katman katman büyür; derin katman resmin geniş bir bölgesini görür |

## 2. CNN, veri artırma, değerlendirme

| Konu | Hatırla |
|---|---|
| İlk CNN | evrişim + ReLU + havuzlama blokları, sonda `Flatten` + `Linear`; aynı işi gören MLP'den çok daha az parametre |
| Veri artırma | yalnızca eğitim setine; anlamı bozmayan dönüşümler (6 döndürülünce 9 olur) |
| `train()` / `eval()` | Dropout ve BatchNorm farklı davranır; ölçerken `eval()` ve `torch.no_grad()` |
| Değerlendirme | karışıklık matrisi, sınıf başına kesinlik ve duyarlılık, top-k; doğruluk tek başına yetmez |
| Veri setleri | `ImageFolder` klasör adından etiket; `DataLoader` karıştırma ve toplu yükleme |

## 3. Hazır mimariler ve transfer öğrenme

| Konu | Hatırla |
|---|---|
| VGG'den ResNet'e | derinleşince gradyan kayboluyor; artık bağlantı (`x + f(x)`) ve BatchNorm |
| Hazır model | `resnet18(weights=None)`: yapı hazır, ağırlıklar rastgele |
| Transfer | gövdeyi dondur (`requires_grad_(False)`), başı değiştir, yalnızca baş eğitilir; ince ayarda küçük öğrenme oranı |
| Benzer / uzak hedef | kaynağa benzeyen hedefte dondurmak iyi; uzak hedefte ince ayar gerekir |
| Özellik çıkarma | son katmandan önceki vektör; benzerlik araması, kNN, küçük baş |

## 4. Nesne algılama

| Konu | Hatırla |
|---|---|
| Kutu biçimleri | xyxy, xywh, cxcywh; `box_convert` |
| IoU | ortak alan / birleşim; `box_iou` |
| NMS | puana göre sırala, tutulanla IoU'su eşiği aşanı at; `nms`, sınıfa göre `batched_nms` |
| Eşleştirme | açgözlü (puan sırasıyla) ya da Macar yöntemi (`linear_sum_assignment`) |
| Ölçüler | TP / FP / FN, kesinlik, duyarlılık, AP (zarfın altındaki alan), mAP |
| YOLO | ızgara, sorumlu hücre, hedef tensörü, çözme, çapalar |

## 5. Bölütleme ve açıklama

| Konu | Hatırla |
|---|---|
| Bölütleme | her piksele sınıf; kodlayıcı–çözücü, ters evrişim, U-Net atlama bağlantısı |
| Ölçüler | piksel doğruluğu yanıltır; sınıf başına IoU, mIoU, Dice |
| Dengesizlik | sınıf ağırlıkları, Dice kaybı |
| Açıklama | duyarlılık haritası (girdiye göre gradyan), Grad-CAM (kanca + gradyan ortalaması), örtme |

## Modelsiz bir hat sağlaması

Bir algılayıcıyı eğitmeden önce **hattın kendisini** sınamak iyi bir
alışkanlık: gerçek kutuları hedefe yazıp geri çöz, sahte "tahmin"ler ekle
(aynı nesneye ikinci bir kutu, yanlış sınıf, boşta bir kutu), NMS'ten geçir ve
eşleştir. Sonuç biliniyor; tutmazsa hata modelde değil kodda.

```python
import torch
from torchvision.ops import batched_nms, box_iou
from dl_data import make_scenes

images, boxes, masks = make_scenes(100, size=32, seed=7)
scene = boxes[0]
S, SIZE, C = 4, 32, 3
CELL = SIZE / S


def encode(scene):
    target = torch.zeros(S, S, 5 + C)
    for x1, y1, x2, y2, label in scene:
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        row, col = int(cy // CELL), int(cx // CELL)
        target[row, col, :5] = torch.tensor(
            [1, cx / CELL - col, cy / CELL - row, (x2 - x1) / SIZE, (y2 - y1) / SIZE])
        target[row, col, 5 + label] = 1
    return target


def decode(target):
    found = []
    for row, col in torch.nonzero(target[..., 0] == 1).tolist():
        _, ox, oy, w, h = target[row, col, :5].tolist()
        cx, cy, w, h = (col + ox) * CELL, (row + oy) * CELL, w * SIZE, h * SIZE
        label = target[row, col, 5:].argmax().item()
        found.append([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, label])
    return found


decoded = decode(encode(scene))
print(sorted(decoded) == sorted([[float(v) for v in b[:4]] + [b[4]] for b in scene]))

x1, y1, x2, y2, label = decoded[0]
shifted = [x1 + 1, y1, x2 + 1, y2, label]
wrong_class = [x1, y1, x2, y2, (label + 1) % 3]
extra = [shifted, wrong_class, [0, 0, 3, 3, 0]]
predicted = decoded + extra
scores = torch.tensor([0.9] * len(decoded) + [0.8, 0.7, 0.6])
xyxy = torch.tensor([b[:4] for b in predicted])
labels = torch.tensor([b[4] for b in predicted])
keep = batched_nms(xyxy, scores, labels, 0.5)
print(len(predicted), len(keep))

truth = torch.tensor([b[:4] for b in scene], dtype=torch.float32)
used, tp, fp = set(), 0, 0
for k in keep.tolist():
    overlaps = box_iou(xyxy[k:k + 1], truth)[0]
    matches = [j for j in range(len(scene)) if j not in used
               and scene[j][4] == labels[k].item() and overlaps[j] >= 0.5]
    if matches:
        used.add(max(matches, key=lambda j: overlaps[j].item()))
        tp += 1
    else:
        fp += 1
print(tp, fp, len(scene) - len(used))
```

```text
True
6 5
3 2 0
```

- Hedefe yazıp geri çözmek gerçek kutuları birebir veriyor: kodlama ve çözme
  birbirinin tersi.
- Altı kutudan NMS beşini tuttu: aynı nesneye bir piksel kaymış ikinci kutu
  (aynı sınıf) atıldı; **yanlış sınıflı** kopya `batched_nms`'te ayrı sınıf
  olduğu için kaldı, boştaki küçük kutu da kaldı.
- Eşleştirme: üç doğru pozitif, iki yanlış pozitif (yanlış sınıflı kopya ve
  boştaki kutu), sıfır kaçırılan.

## Sırada ne var?

İki not seni bekliyor: **Hızlı Başvuru** (modülün kodlarının tek sayfalık
özeti) ve **Buradan Sonrası** (gerçek veri setleri, hazır algılayıcılar,
üretime almak). Sonra sınav ve beş karma alıştırma.
