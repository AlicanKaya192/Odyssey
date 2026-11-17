Modülün en sık kullanılan kodları tek sayfada.

## Resim ve dönüşüm

```python
from torchvision.transforms import v2

train_tf = v2.Compose([
    v2.ToImage(), v2.ToDtype(torch.float32, scale=True),
    v2.RandomHorizontalFlip(), v2.RandomRotation(10),
    v2.Normalize([0.5], [0.5]),
])
test_tf = v2.Compose([v2.ToImage(), v2.ToDtype(torch.float32, scale=True),
                      v2.Normalize([0.5], [0.5])])
```

Veri artırma yalnızca eğitimde; normalleştirme ikisinde de aynı.

## CNN bloğu ve eğitim döngüsü

```python
block = nn.Sequential(nn.Conv2d(16, 32, 3, padding=1), nn.BatchNorm2d(32),
                      nn.ReLU(), nn.MaxPool2d(2))

model.train()
for images, labels in loader:
    optimizer.zero_grad()
    loss = loss_fn(model(images), labels)
    loss.backward()
    optimizer.step()

model.eval()
with torch.no_grad():
    predictions = model(x_test).argmax(dim=1)
```

## Transfer öğrenme

```python
from torchvision.models import resnet18

model = resnet18(weights=None)
model.load_state_dict(source_weights)
for p in model.parameters():
    p.requires_grad_(False)
model.fc = nn.Linear(model.fc.in_features, num_classes)
optimizer = torch.optim.Adam(model.fc.parameters(), lr=1e-3)
```

Yeni baş eğitilebilir doğar; gövde donuk. İnce ayarda gövdenin son bloğu da
açılır ve küçük bir öğrenme oranı verilir.

## Kutular

```python
from torchvision.ops import box_convert, box_iou, nms, batched_nms

xyxy = box_convert(cxcywh, in_fmt="cxcywh", out_fmt="xyxy")
overlaps = box_iou(predicted, truth)
keep = batched_nms(xyxy, scores, labels, iou_threshold=0.5)
```

## Bölütleme ölçüsü

```python
def iou_per_class(predicted, truth, num_classes):
    scores = []
    for c in range(num_classes):
        p, t = predicted == c, truth == c
        scores.append((p & t).sum().item() / max((p | t).sum().item(), 1))
    return scores
```

## Kanca ve Grad-CAM

```python
store = {}
handle = layer.register_forward_hook(lambda m, i, o: store.update(maps=o))
scores = model(image[None])
grads = torch.autograd.grad(scores[0, target], store["maps"])[0]
cam = torch.relu((grads.mean(dim=(2, 3), keepdim=True) * store["maps"]).sum(dim=1))
handle.remove()
```

## Kontrol listesi

- Eğitim ve test aynı ön işlemeden mi geçiyor (normalleştirme, boy)?
- Ölçerken `model.eval()` ve `torch.no_grad()` var mı?
- Doğruluğun yanında sınıf başına ölçü (karışıklık matrisi, IoU) var mı?
- Algılamada eşikler (güven, NMS, eşleştirme IoU'su) kayıtlı mı?
- Kancalar sökülüyor mu?
