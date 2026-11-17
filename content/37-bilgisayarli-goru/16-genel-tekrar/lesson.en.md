# Overall Review

You have reached the end of the Computer Vision module. Starting from how a
picture sits as a tensor, you walked through convolution, CNNs, data
augmentation, evaluation, ready-made architectures, transfer learning, object
detection, segmentation and explaining a model; in the end you trained your
own detector. This section walks the road once more and finishes with a
model-free **pipeline check**.

<figure class="fig">
  <div class="flow">
    <span class="node">Pictures and convolution</span><span class="arrow">→</span>
    <span class="node">CNNs and training</span><span class="arrow">→</span>
    <span class="node">Ready-made networks</span><span class="arrow">→</span>
    <span class="node">Detection</span><span class="arrow">→</span>
    <span class="node acc">Segmentation and explanation</span>
  </div>
  <figcaption>The module's road: understand pictures and convolution, train and measure a CNN, use ready-made networks, find objects, separate pixel by pixel and explain the model's decision.</figcaption>
</figure>

## 1. Pictures, convolution, pooling

| Topic | Remember |
|---|---|
| Picture tensor | PyTorch `(N, C, H, W)`; Pillow and NumPy `(H, W, C)`; `ToTensor` / `ToImage` to the 0–1 range |
| Convolution | the kernel slides over the picture; output size `(H + 2p − k) / s + 1`, rounded down |
| Channels | `Conv2d(in, out, k)`: each output channel looks at all input channels |
| Pooling | `MaxPool2d(2)` halves the size and gives robustness to small shifts |
| Receptive field | grows layer by layer; a deep layer sees a wide region of the picture |

## 2. CNNs, data augmentation, evaluation

| Topic | Remember |
|---|---|
| First CNN | blocks of convolution + ReLU + pooling, `Flatten` + `Linear` at the end; far fewer parameters than an MLP doing the same job |
| Data augmentation | training set only; transforms that do not change the meaning (a rotated 6 becomes a 9) |
| `train()` / `eval()` | Dropout and BatchNorm behave differently; when measuring, `eval()` and `torch.no_grad()` |
| Evaluation | confusion matrix, per-class precision and recall, top-k; accuracy alone is not enough |
| Data sets | `ImageFolder` takes the label from the folder name; `DataLoader` shuffles and batches |

## 3. Ready-made architectures and transfer learning

| Topic | Remember |
|---|---|
| From VGG to ResNet | going deeper, the gradient vanishes; residual connection (`x + f(x)`) and BatchNorm |
| Ready-made model | `resnet18(weights=None)`: the structure is ready, the weights are random |
| Transfer | freeze the body (`requires_grad_(False)`), replace the head, only the head trains; small learning rate when fine-tuning |
| Similar / distant target | freezing works for a target like the source; a distant target needs fine-tuning |
| Feature extraction | the vector before the last layer; similarity search, kNN, a small head |

## 4. Object detection

| Topic | Remember |
|---|---|
| Box formats | xyxy, xywh, cxcywh; `box_convert` |
| IoU | common area / union; `box_iou` |
| NMS | sort by score, drop what overlaps a kept box beyond the threshold; `nms`, per class `batched_nms` |
| Matching | greedy (in score order) or the Hungarian method (`linear_sum_assignment`) |
| Measures | TP / FP / FN, precision, recall, AP (area under the envelope), mAP |
| YOLO | grid, responsible cell, target tensor, decoding, anchors |

## 5. Segmentation and explanation

| Topic | Remember |
|---|---|
| Segmentation | a class for every pixel; encoder–decoder, transposed convolution, U-Net skip connection |
| Measures | pixel accuracy misleads; per-class IoU, mIoU, Dice |
| Imbalance | class weights, Dice loss |
| Explanation | saliency map (gradient with respect to the input), Grad-CAM (hook + mean gradient), occlusion |

## A model-free pipeline check

Before training a detector it is a good habit to test **the pipeline
itself**: write the true boxes into the target and decode them back, add fake
"predictions" (a second box on the same object, a wrong class, a stray box),
pass them through NMS and match them. The result is known; if it does not
hold, the mistake is in the code, not the model.

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

- Writing into the target and decoding back gives exactly the true boxes:
  encoding and decoding are inverses of each other.
- NMS kept five of the six boxes: the second box shifted by one pixel on the
  same object (same class) was dropped; the **wrong-class** copy stayed
  because it is a separate class in `batched_nms`, and the small stray box
  stayed too.
- Matching: three true positives, two false positives (the wrong-class copy
  and the stray box), zero missed.

## What next?

Two notes are waiting for you: **Quick Reference** (a one-page summary of the
module's code) and **Where to Go Next** (real data sets, ready-made
detectors, going to production). Then the quiz and five mixed exercises.
