The module's most used code on one page.

## Pictures and transforms

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

Data augmentation only in training; normalisation is the same in both.

## A CNN block and the training loop

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

## Transfer learning

```python
from torchvision.models import resnet18

model = resnet18(weights=None)
model.load_state_dict(source_weights)
for p in model.parameters():
    p.requires_grad_(False)
model.fc = nn.Linear(model.fc.in_features, num_classes)
optimizer = torch.optim.Adam(model.fc.parameters(), lr=1e-3)
```

The new head is born trainable; the body is frozen. When fine-tuning, the
last block of the body is opened too and given a small learning rate.

## Boxes

```python
from torchvision.ops import box_convert, box_iou, nms, batched_nms

xyxy = box_convert(cxcywh, in_fmt="cxcywh", out_fmt="xyxy")
overlaps = box_iou(predicted, truth)
keep = batched_nms(xyxy, scores, labels, iou_threshold=0.5)
```

## A segmentation measure

```python
def iou_per_class(predicted, truth, num_classes):
    scores = []
    for c in range(num_classes):
        p, t = predicted == c, truth == c
        scores.append((p & t).sum().item() / max((p | t).sum().item(), 1))
    return scores
```

## Hook and Grad-CAM

```python
store = {}
handle = layer.register_forward_hook(lambda m, i, o: store.update(maps=o))
scores = model(image[None])
grads = torch.autograd.grad(scores[0, target], store["maps"])[0]
cam = torch.relu((grads.mean(dim=(2, 3), keepdim=True) * store["maps"]).sum(dim=1))
handle.remove()
```

## Checklist

- Do training and test go through the same preprocessing (normalisation,
  size)?
- Are `model.eval()` and `torch.no_grad()` there when measuring?
- Is there a per-class measure (confusion matrix, IoU) next to accuracy?
- In detection, are the thresholds (confidence, NMS, matching IoU) recorded?
- Are the hooks removed?
