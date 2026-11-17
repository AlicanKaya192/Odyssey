# NMS and Evaluating Detection

A detector often proposes several boxes very close to each other for the same
object: they all surround the same person with small differences. In this
section we learn two jobs. First **non-maximum suppression** (**NMS**), which
weeds out these extra boxes. Then measuring the detector: **matching**
predictions to true boxes, counting the right and wrong ones, and computing
**precision**, **recall** and **average precision** (**AP**). Evaluating a
system that detects people in a video takes exactly these steps in every
frame.

## Several boxes for the same object

Let us build a detector output by hand: two objects, five boxes. Each box has
a confidence score.

```python
import torch
from torchvision.ops import box_iou, nms

boxes = torch.tensor([
    [10.0, 10, 20, 20],
    [11, 11, 21, 21],
    [9, 10, 19, 21],
    [30, 30, 40, 40],
    [31, 29, 41, 39],
])
scores = torch.tensor([0.9, 0.8, 0.7, 0.85, 0.6])
overlap = box_iou(boxes, boxes)
print([round(v, 2) for v in overlap[0].tolist()])
```

```text
[1.0, 0.68, 0.75, 0.0, 0.0]
```

The first box overlaps a lot with the second and third (the same object) and
not at all with the fourth and fifth (the other object).

## Writing NMS by hand

The idea is plain: sort the boxes by score; **keep** the highest-scoring one;
**drop** every box whose IoU with it is above the threshold; repeat with the
rest.

```python
def my_nms(boxes, scores, threshold):
    order = scores.argsort(descending=True).tolist()
    keep = []
    while order:
        best = order.pop(0)
        keep.append(best)
        ious = box_iou(boxes[best:best + 1], boxes[order])[0] if order else []
        order = [i for i, value in zip(order, ious) if value <= threshold]
    return keep


print(my_nms(boxes, scores, 0.5))
print(nms(boxes, scores, 0.5).tolist())
```

```text
[0, 3]
[0, 3]
```

Two objects, two boxes: each object's most confident box remained. Our own
function gives the same result as torchvision's `nms`. If the threshold is
small (such as 0.3), boxes of **different** objects that stand close may also
erase each other; if it is large (such as 0.8), several boxes remain for the
same object.

## The confidence threshold and per-class NMS

In a real detector, low-scoring boxes are dropped before NMS (the confidence
threshold). And NMS is usually done **class by class**: the boxes of a person
and a bicycle on top of each other must not erase each other.
`torchvision.ops.batched_nms` treats each class separately:

```python
from torchvision.ops import batched_nms

labels = torch.tensor([0, 0, 1, 1, 1])
confident = scores >= 0.65
print(confident.tolist())
kept = batched_nms(boxes[confident], scores[confident], labels[confident], 0.5)
print(kept.tolist(), labels[confident][kept].tolist())
```

```text
[True, True, True, True, False]
[0, 3, 2] [0, 1, 1]
```

- The last box, with a score of 0.6, was dropped by the confidence threshold.
- The third box overlaps a lot with the first but its class is different (1):
  per-class NMS did not erase it. In the end one box of class 0 and two of
  class 1 remained.

## Matching predictions to true boxes

To measure a detector we match each prediction with at most one true box:

- **True positive (TP):** IoU ≥ 0.5 with a true box that has not already been
  matched by another prediction.
- **False positive (FP):** a prediction that cannot be matched (a box drawn on
  empty space or on an object already found).
- **False negative (FN):** a true box matched by no prediction (a missed
  object).

The most common way is **greedy** matching: go through the predictions in
score order; each takes the not-yet-matched true box with the highest IoU.

```python
def greedy_match(pred_boxes, pred_scores, truth_boxes, threshold=0.5):
    order = pred_scores.argsort(descending=True).tolist()
    ious = box_iou(pred_boxes, truth_boxes)
    used = set()
    tp = []
    for i in order:
        free = [j for j in range(len(truth_boxes)) if j not in used]
        candidates = [(ious[i, j].item(), j) for j in free]
        best_iou, best_j = max(candidates, default=(0.0, -1))
        if best_iou >= threshold:
            used.add(best_j)
            tp.append(True)
        else:
            tp.append(False)
    return tp, len(truth_boxes) - len(used)


truth = torch.tensor([[10.0, 10, 20, 20], [30, 30, 40, 40], [50, 5, 60, 15]])
tp, fn = greedy_match(boxes, scores, truth)
print(tp, fn)
precision = sum(tp) / len(tp)
recall = sum(tp) / len(truth)
print(round(precision, 2), round(recall, 2))
```

```text
[True, True, False, False, False] 1
0.4 0.67
```

- Of the five predictions without NMS, two are right; the other three boxes
  drawn on the same objects counted as false positives. The third real object
  was never found: one false negative.
- **Precision** = TP ÷ number of predictions = 2 / 5; **recall** = TP ÷ number
  of real objects = 2 / 3.
- Had the same measurement been made after NMS, precision would be 2 / 2: NMS
  keeps the extra boxes from counting as false positives.

## When greedy is not enough: the Hungarian algorithm

Greedy matching takes the best at each step but may not give the best result
overall. The **Hungarian algorithm** considers all matches together and finds
the one with the largest total IoU. SciPy has it as `linear_sum_assignment`;
since it minimises a cost, we give it minus the IoU.

```python
from scipy.optimize import linear_sum_assignment

truth_pair = torch.tensor([[0.0, 0, 10, 10], [4, 0, 14, 10]])
pred_pair = torch.tensor([[3.0, 0, 13, 10], [5, 0, 15, 10]])
pair_scores = torch.tensor([0.9, 0.8])
ious = box_iou(pred_pair, truth_pair)
print([[round(v, 2) for v in row] for row in ious.tolist()])
print(greedy_match(pred_pair, pair_scores, truth_pair))
rows, cols = linear_sum_assignment(-ious.numpy())
matched = [(int(r), int(c)) for r, c in zip(rows, cols) if ious[r, c] >= 0.5]
print(matched)
```

```text
[[0.54, 0.82], [0.33, 0.82]]
([True, False], 1)
[(0, 0), (1, 1)]
```

- The high-scoring first prediction greedily took the second true box, with
  which its IoU is largest (0.82); the first true box left for the second
  prediction has an IoU of only 0.33 with it: one right, one wrong.
- The Hungarian algorithm gave the first prediction the first box (0.54) and
  the second the second (0.82): two right.
- Real detection measures (such as AP below) usually use the greedy way; the
  Hungarian algorithm is common especially in **tracking** (matching the boxes
  of one frame with those of the next).

## The precision–recall curve and AP

Precision and recall depend on the confidence threshold: if the threshold
drops, more boxes are accepted, recall rises and precision usually falls.
Instead of choosing a single threshold, the measure that sums up a detector
over **all thresholds** is **AP**: the area under the precision–recall curve.

Suppose we have sorted all predictions on a dataset by score and know whether
each one is a TP or an FP (6 real objects in total):

```python
hits = torch.tensor([1, 1, 0, 1, 1, 0, 0, 1, 0, 0], dtype=torch.float32)
total_truth = 6
tp_cum = hits.cumsum(0)
fp_cum = (1 - hits).cumsum(0)
precision = tp_cum / (tp_cum + fp_cum)
recall = tp_cum / total_truth
print([round(v, 2) for v in precision.tolist()])
print([round(v, 2) for v in recall.tolist()])

envelope = precision.flip(0).cummax(0).values.flip(0)
steps = torch.cat([torch.tensor([0.0]), recall])
ap = ((steps[1:] - steps[:-1]) * envelope).sum().item()
print(round(ap, 3))
```

```text
[1.0, 1.0, 0.67, 0.75, 0.8, 0.67, 0.57, 0.62, 0.56, 0.5]
[0.17, 0.33, 0.33, 0.5, 0.67, 0.67, 0.67, 0.83, 0.83, 0.83]
0.704
```

- The list is sorted by score: row k means the threshold has dropped to the
  k-th prediction's score. Recall never falls; precision goes up and down.
- The **envelope**: at each point, the highest precision from that point on.
  It smooths out the zigzags of the curve.
- AP is the sum of steps, each recall increase multiplied by the envelope's
  height. This detector, which finds 5 of the 6 objects, has an AP of 0.704.
- A real object never found (here one) cuts off the right end of the curve:
  recall stays at 5/6 and AP cannot reach 1.

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="260.135469pt" height="189.544781pt" viewBox="0 0 260.135469 189.544781" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 189.544781 
L 260.135469 189.544781 
L 260.135469 0 
L 0 0 
L 0 189.544781 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 44.103906 151.344 
L 244.983906 151.344 
L 244.983906 7.2 
L 44.103906 7.2 
L 44.103906 151.344 
z
" style="fill: none"/>
   </g>
   <g id="matplotlib.axis_1">
    <g id="xtick_1">
     <g id="line2d_1">
      <defs>
       <path id="m15aed4d867" d="M 0 0 
L 0 3.5 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m15aed4d867" x="44.103906" y="151.344" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="44.103906" y="165.941656" transform="rotate(-0 44.103906 165.941656)">0.0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="84.279906" y="151.344" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="84.279906" y="165.941656" transform="rotate(-0 84.279906 165.941656)">0.2</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="124.455906" y="151.344" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="124.455906" y="165.941656" transform="rotate(-0 124.455906 165.941656)">0.4</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="164.631906" y="151.344" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="164.631906" y="165.941656" transform="rotate(-0 164.631906 165.941656)">0.6</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="204.807906" y="151.344" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="204.807906" y="165.941656" transform="rotate(-0 204.807906 165.941656)">0.8</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="244.983906" y="151.344" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="244.983906" y="165.941656" transform="rotate(-0 244.983906 165.941656)">1.0</text>
     </g>
    </g>
    <g id="text_7">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="144.543906" y="179.942438" transform="rotate(-0 144.543906 179.942438)">recall</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_7">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103906" y="151.344" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103906" y="155.142828" transform="rotate(-0 37.103906 155.142828)">0.0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103906" y="123.888" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103906" y="127.686828" transform="rotate(-0 37.103906 127.686828)">0.2</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103906" y="96.432" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103906" y="100.230828" transform="rotate(-0 37.103906 100.230828)">0.4</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103906" y="68.976" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103906" y="72.774828" transform="rotate(-0 37.103906 72.774828)">0.6</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103906" y="41.52" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103906" y="45.318828" transform="rotate(-0 37.103906 45.318828)">0.8</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103906" y="14.064" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103906" y="17.862828" transform="rotate(-0 37.103906 17.862828)">1.0</text>
     </g>
    </g>
    <g id="text_14">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="79.272" transform="rotate(-90 14.798438 79.272)">precision</text>
    </g>
   </g>
   <g id="line2d_13">
    <path d="M 44.103906 14.064 
L 77.583907 14.064 
L 111.063908 14.064 
L 111.063908 59.823997 
L 144.543906 48.384 
L 178.02391 41.519998 
L 178.02391 59.823997 
L 178.02391 72.898282 
L 211.503902 65.544 
L 211.503902 75.07733 
L 211.503902 82.704 
" clip-path="url(#p13215483c9)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
    <defs>
     <path id="me559690d41" d="M 0 1.5 
C 0.397805 1.5 0.77937 1.341951 1.06066 1.06066 
C 1.341951 0.77937 1.5 0.397805 1.5 0 
C 1.5 -0.397805 1.341951 -0.77937 1.06066 -1.06066 
C 0.77937 -1.341951 0.397805 -1.5 0 -1.5 
C -0.397805 -1.5 -0.77937 -1.341951 -1.06066 -1.06066 
C -1.341951 -0.77937 -1.5 -0.397805 -1.5 0 
C -1.5 0.397805 -1.341951 0.77937 -1.06066 1.06066 
C -0.77937 1.341951 -0.397805 1.5 0 1.5 
z
" style="stroke: #1f77b4"/>
    </defs>
    <g clip-path="url(#p13215483c9)">
     <use xlink:href="#me559690d41" x="44.103906" y="14.064" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#me559690d41" x="77.583907" y="14.064" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#me559690d41" x="111.063908" y="14.064" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#me559690d41" x="111.063908" y="59.823997" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#me559690d41" x="144.543906" y="48.384" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#me559690d41" x="178.02391" y="41.519998" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#me559690d41" x="178.02391" y="59.823997" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#me559690d41" x="178.02391" y="72.898282" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#me559690d41" x="211.503902" y="65.544" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#me559690d41" x="211.503902" y="75.07733" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#me559690d41" x="211.503902" y="82.704" style="fill: #1f77b4; stroke: #1f77b4"/>
    </g>
   </g>
   <g id="line2d_14">
    <path d="M 77.583907 14.064 
L 77.583907 14.064 
L 111.063908 14.064 
L 111.063908 41.519998 
L 111.063908 41.519998 
L 111.063908 41.519998 
L 144.543906 41.519998 
L 144.543906 41.519998 
L 178.02391 41.519998 
L 178.02391 59.823997 
L 178.02391 59.823997 
L 178.02391 65.544 
L 178.02391 65.544 
L 178.02391 65.544 
L 211.503902 65.544 
L 211.503902 75.07733 
L 211.503902 75.07733 
L 211.503902 82.704 
L 211.503902 82.704 
" clip-path="url(#p13215483c9)" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="patch_3">
    <path d="M 44.103906 151.344 
L 44.103906 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 244.983906 151.344 
L 244.983906 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 44.103906 151.344 
L 244.983906 151.344 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 44.103906 7.2 
L 244.983906 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="patch_7">
     <path d="M 185.51125 33.801094 
L 240.083906 33.801094 
Q 241.483906 33.801094 241.483906 32.401094 
L 241.483906 12.1 
Q 241.483906 10.7 240.083906 10.7 
L 185.51125 10.7 
Q 184.11125 10.7 184.11125 12.1 
L 184.11125 32.401094 
Q 184.11125 33.801094 185.51125 33.801094 
L 185.51125 33.801094 
z
" style="fill: none; opacity: 0.8; stroke: currentColor; stroke-linejoin: miter"/>
    </g>
    <g id="line2d_15">
     <path d="M 186.91125 16.368906 
L 193.91125 16.368906 
L 200.91125 16.368906 
" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
     <g>
      <use xlink:href="#me559690d41" x="193.91125" y="16.368906" style="fill: #1f77b4; stroke: #1f77b4"/>
     </g>
    </g>
    <g id="text_15">
     <text style="font-size: 7px; font-family:inherit; text-anchor: start; fill: currentColor" x="206.51125" y="18.818906" transform="rotate(-0 206.51125 18.818906)">precision</text>
    </g>
    <g id="line2d_16">
     <path d="M 186.91125 26.869453 
L 186.91125 26.869453 
L 193.91125 26.869453 
L 193.91125 26.869453 
L 200.91125 26.869453 
" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
    </g>
    <g id="text_16">
     <text style="font-size: 7px; font-family:inherit; text-anchor: start; fill: currentColor" x="206.51125" y="29.319453" transform="rotate(-0 206.51125 29.319453)">envelope</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p13215483c9">
   <rect x="44.103906" y="7.2" width="200.88" height="144.144"/>
  </clipPath>
 </defs>
</svg>
<figcaption>The precision–recall curve and its envelope; AP is the area under the envelope.</figcaption>
</figure>

## Summary

- NMS: sort by score, keep the best, drop those overlapping it a lot;
  `torchvision.ops.nms`, class by class `batched_nms`.
- Matching: IoU ≥ threshold and each true box at most once; greedy or
  Hungarian (`linear_sum_assignment`).
- TP, FP, FN → precision = TP / predictions, recall = TP / real objects.
- AP: the area under the (envelope of the) precision–recall curve; sums up all
  confidence thresholds at once.
