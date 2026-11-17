# Evaluating Classification

So far we measured networks with a single number, accuracy. Accuracy answers
"how good" but not "**where** does it go wrong". In this section we train a
CNN on a ten-class problem (handwritten digits) and examine the result with a
**confusion matrix** and per-class **precision** and **recall**. You know
these measures from the Machine Learning track; the real work here is
extracting them from a network's output with PyTorch. We will need these tools
to compare models before moving on to transfer learning.

## A CNN on digits

We scale the `load_digits` pictures to [0, 1] and make them `(N, 1, 8, 8)`.
The data is 70% training, 30% test; `stratify` keeps each digit in the same
proportion on both sides. Since the pictures are small (8 × 8), the map is
2 × 2 after two poolings.

```python
import torch
import torch.nn.functional as F
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

digits = load_digits()
x = torch.tensor(digits.images, dtype=torch.float32).unsqueeze(1) / 16
y = torch.tensor(digits.target)
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, random_state=0, stratify=y)
loader = DataLoader(TensorDataset(x_train, y_train), batch_size=32, shuffle=True,
                    generator=torch.Generator().manual_seed(0))

torch.manual_seed(0)
model = nn.Sequential(
    nn.Conv2d(1, 16, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(16, 32, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Flatten(), nn.Linear(32 * 2 * 2, 10),
)
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
for epoch in range(6):
    model.train()
    for xb, yb in loader:
        optimizer.zero_grad()
        F.cross_entropy(model(xb), yb).backward()
        optimizer.step()

model.eval()
with torch.no_grad():
    logits = model(x_test)
predictions = logits.argmax(dim=1)
print(len(x_train), len(x_test))
print(round((predictions == y_test).float().mean().item(), 3))
```

```text
1257 540
0.967
```

The large majority of the 540 test pictures are right. So where are the
mistakes?

## The confusion matrix

In a confusion matrix the **row is the true class**, the **column the
prediction**. The diagonal holds the right predictions; every number off the
diagonal is a confusion.

```python
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, predictions)
print(cm)
```

```text
[[54  0  0  0  0  0  0  0  0  0]
 [ 0 55  0  0  0  0  0  0  0  0]
 [ 0  4 47  2  0  0  0  0  0  0]
 [ 0  0  0 52  0  0  0  1  0  2]
 [ 0  0  0  0 52  0  0  0  0  2]
 [ 0  0  0  1  0 54  0  0  0  0]
 [ 0  1  0  0  0  0 53  0  0  0]
 [ 0  0  0  0  0  0  0 54  0  0]
 [ 0  3  0  0  0  0  1  1 47  0]
 [ 0  0  0  0  0  0  0  0  0 54]]
```

- Row 2, column 1: four 2s were taken for 1s.
- Row 8, column 1: three 8s were taken for 1s too.
- Column 1's total is bigger than its row: the network leans towards saying
  "1".

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="219.1705pt" height="222.808781pt" viewBox="0 0 219.1705 222.808781" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 222.808781 
L 219.1705 222.808781 
L 219.1705 0 
L 0 0 
L 0 222.808781 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 34.5625 184.608 
L 211.9705 184.608 
L 211.9705 7.2 
L 34.5625 7.2 
L 34.5625 184.608 
z
" style="fill: none"/>
   </g>
   <g clip-path="url(#pf2f4091bb6)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAPYAAAD2CAYAAADlEnrIAAADeklEQVR4nO3dsY0TURRA0TE2ES1sRExK5CacbgcUsGVQwHZA6iYckRITUYCTiVbWIDoAyd+juZxTwPtfI1297M9uma/LBKS8W/sCwP0JG4KEDUHChiBhQ5CwIUjYECRsCBI2BAkbgoQNQcKGIGFDkLAhSNgQJGwIEjYECRuChA1BwoYgYUOQsCFI2BAkbAg6POKQ7x8/DZ3/+eePofP5e7fLefOfa388TVtnY0OQsCFI2BAkbAgSNgQJG4KEDUHChiBhQ5CwIUjYECRsCBI2BAkbgoQNQcKGIGFDkLAhSNgQJGwIEjYECRuChA1Bu2W+LmtfArgvGxuChA1BwoYgYUOQsCFI2BAkbAgSNgQJG4KEDUHChiBhQ5CwIUjYECRsCBI2BAkbgoQNQcKGIGFDkLAhSNgQJGwIEjYEHR5xyO1yHjp/fzwNnQ9bY2NDkLAhSNgQJGwIEjYECRuChA1BwoYgYUOQsCFI2BAkbAgSNgQJG4KEDUHChiBhQ5CwIUjYECRsCBI2BAkbgoQNQcKGoN0yX5e1L7EFo3968IcfH3AvNjYECRuChA1BwoYgYUOQsCFI2BAkbAgSNgQJG4KEDUHChiBhQ5CwIUjYECRsCBI2BAkbgoQNQcKGIGFDkLAhSNgQ5F1xWMHby/PQ+TY2BAkbgoQNQcKGIGFDkLAhSNgQJGwIEjYECRuChA1BwoYgYUOQsCFI2BAkbAgSNgQJG4KEDUHChiBhQ5CwIUjYECRsCDqsfQH4F7fLefgH2x9P09bZ2BAkbAgSNgQJG4KEDUHChiBhQ5CwIUjYECRsCBI2BAkbgoQNQcKGIGFDkLAhSNgQJGwIEjYECRuChA1BwoYgYUOQsCFot8zXZfQhXz48DZ3/Ov+aRnt7eR5+xvuv34afwf/BxoYgYUOQsCFI2BAkbAgSNgQJG4KEDUHChiBhQ5CwIUjYECRsCBI2BAkbgoQNQcKGIGFDkLAhSNgQJGwIEjYECRuCHvKuOPBYNjYECRuChA1BwoYgYUOQsCFI2BAkbAgSNgQJG4KEDUHChiBhQ5CwIUjYECRsCBI2BAkbgoQNQcKGIGFDkLAhSNgQJGwIEjYECRuChA1BwoYgYUOQsCFI2BAkbAgSNgQJG4KEDUHChiBhQ5CwIUjYECRsCBI2BAkbgoQNQcKGIGFDkLAhSNgQJGyYen4DwvQwB5A2qLsAAAAASUVORK5CYII=" id="imaged3c1fdc36a" transform="scale(1 -1) translate(0 -177.12)" x="34.56" y="-7.528781" width="177.12" height="177.12"/>
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
       <use xlink:href="#m15aed4d867" x="43.4329" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="43.4329" y="199.205656" transform="rotate(-0 43.4329 199.205656)">0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="61.1737" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="61.1737" y="199.205656" transform="rotate(-0 61.1737 199.205656)">1</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="78.9145" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="78.9145" y="199.205656" transform="rotate(-0 78.9145 199.205656)">2</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="96.6553" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="96.6553" y="199.205656" transform="rotate(-0 96.6553 199.205656)">3</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="114.3961" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="114.3961" y="199.205656" transform="rotate(-0 114.3961 199.205656)">4</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="132.1369" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="132.1369" y="199.205656" transform="rotate(-0 132.1369 199.205656)">5</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="149.8777" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="149.8777" y="199.205656" transform="rotate(-0 149.8777 199.205656)">6</text>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m15aed4d867" x="167.6185" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="167.6185" y="199.205656" transform="rotate(-0 167.6185 199.205656)">7</text>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m15aed4d867" x="185.3593" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="185.3593" y="199.205656" transform="rotate(-0 185.3593 199.205656)">8</text>
     </g>
    </g>
    <g id="xtick_10">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m15aed4d867" x="203.1001" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="203.1001" y="199.205656" transform="rotate(-0 203.1001 199.205656)">9</text>
     </g>
    </g>
    <g id="text_11">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="123.2665" y="213.206437" transform="rotate(-0 123.2665 213.206437)">predicted</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_11">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="34.5625" y="16.0704" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="27.5625" y="19.869228" transform="rotate(-0 27.5625 19.869228)">0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="34.5625" y="33.8112" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="27.5625" y="37.610028" transform="rotate(-0 27.5625 37.610028)">1</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="34.5625" y="51.552" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="27.5625" y="55.350828" transform="rotate(-0 27.5625 55.350828)">2</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m5c8d5162d3" x="34.5625" y="69.2928" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="27.5625" y="73.091628" transform="rotate(-0 27.5625 73.091628)">3</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m5c8d5162d3" x="34.5625" y="87.0336" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_16">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="27.5625" y="90.832428" transform="rotate(-0 27.5625 90.832428)">4</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_16">
      <g>
       <use xlink:href="#m5c8d5162d3" x="34.5625" y="104.7744" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_17">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="27.5625" y="108.573228" transform="rotate(-0 27.5625 108.573228)">5</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_17">
      <g>
       <use xlink:href="#m5c8d5162d3" x="34.5625" y="122.5152" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_18">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="27.5625" y="126.314028" transform="rotate(-0 27.5625 126.314028)">6</text>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_18">
      <g>
       <use xlink:href="#m5c8d5162d3" x="34.5625" y="140.256" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_19">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="27.5625" y="144.054828" transform="rotate(-0 27.5625 144.054828)">7</text>
     </g>
    </g>
    <g id="ytick_9">
     <g id="line2d_19">
      <g>
       <use xlink:href="#m5c8d5162d3" x="34.5625" y="157.9968" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_20">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="27.5625" y="161.795628" transform="rotate(-0 27.5625 161.795628)">8</text>
     </g>
    </g>
    <g id="ytick_10">
     <g id="line2d_20">
      <g>
       <use xlink:href="#m5c8d5162d3" x="34.5625" y="175.7376" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_21">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="27.5625" y="179.536428" transform="rotate(-0 27.5625 179.536428)">9</text>
     </g>
    </g>
    <g id="text_22">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.797656" y="95.904" transform="rotate(-90 14.797656 95.904)">true</text>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 34.5625 184.608 
L 34.5625 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 211.9705 184.608 
L 211.9705 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 34.5625 184.608 
L 211.9705 184.608 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 34.5625 7.2 
L 211.9705 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_23">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle; fill: #808080" x="43.4329" y="17.628994" transform="rotate(-0 43.4329 17.628994)">54</text>
   </g>
   <g id="text_24">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle; fill: #808080" x="61.1737" y="35.369794" transform="rotate(-0 61.1737 35.369794)">55</text>
   </g>
   <g id="text_25">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle" x="61.1737" y="53.110594" transform="rotate(-0 61.1737 53.110594)">4</text>
   </g>
   <g id="text_26">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle; fill: #808080" x="78.9145" y="53.110594" transform="rotate(-0 78.9145 53.110594)">47</text>
   </g>
   <g id="text_27">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle" x="96.6553" y="53.110594" transform="rotate(-0 96.6553 53.110594)">2</text>
   </g>
   <g id="text_28">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle; fill: #808080" x="96.6553" y="70.851394" transform="rotate(-0 96.6553 70.851394)">52</text>
   </g>
   <g id="text_29">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle" x="167.6185" y="70.851394" transform="rotate(-0 167.6185 70.851394)">1</text>
   </g>
   <g id="text_30">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle" x="203.1001" y="70.851394" transform="rotate(-0 203.1001 70.851394)">2</text>
   </g>
   <g id="text_31">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle; fill: #808080" x="114.3961" y="88.592194" transform="rotate(-0 114.3961 88.592194)">52</text>
   </g>
   <g id="text_32">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle" x="203.1001" y="88.592194" transform="rotate(-0 203.1001 88.592194)">2</text>
   </g>
   <g id="text_33">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle" x="96.6553" y="106.332994" transform="rotate(-0 96.6553 106.332994)">1</text>
   </g>
   <g id="text_34">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle; fill: #808080" x="132.1369" y="106.332994" transform="rotate(-0 132.1369 106.332994)">54</text>
   </g>
   <g id="text_35">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle" x="61.1737" y="124.073794" transform="rotate(-0 61.1737 124.073794)">1</text>
   </g>
   <g id="text_36">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle; fill: #808080" x="149.8777" y="124.073794" transform="rotate(-0 149.8777 124.073794)">53</text>
   </g>
   <g id="text_37">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle; fill: #808080" x="167.6185" y="141.814594" transform="rotate(-0 167.6185 141.814594)">54</text>
   </g>
   <g id="text_38">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle" x="61.1737" y="159.555394" transform="rotate(-0 61.1737 159.555394)">3</text>
   </g>
   <g id="text_39">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle" x="149.8777" y="159.555394" transform="rotate(-0 149.8777 159.555394)">1</text>
   </g>
   <g id="text_40">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle" x="167.6185" y="159.555394" transform="rotate(-0 167.6185 159.555394)">1</text>
   </g>
   <g id="text_41">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle; fill: #808080" x="185.3593" y="159.555394" transform="rotate(-0 185.3593 159.555394)">47</text>
   </g>
   <g id="text_42">
    <text style="font-size: 6px; font-family:inherit; text-anchor: middle; fill: #808080" x="203.1001" y="177.296194" transform="rotate(-0 203.1001 177.296194)">54</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pf2f4091bb6">
   <rect x="34.5625" y="7.2" width="177.408" height="177.408"/>
  </clipPath>
 </defs>
</svg>
<figcaption>The confusion matrix; the colour shows only the mistakes off the diagonal.</figcaption>
</figure>

## Building the matrix with PyTorch

We can build the confusion matrix ourselves in one line: turn each (true,
predicted) pair into a single number (`true × 10 + predicted`) and count.
Two measures per class come out of the matrix:

- **Precision:** of the ones we called "1", how many really are 1? Diagonal ÷
  **column** sum.
- **Recall:** how many of the real 1s did we find? Diagonal ÷ **row** sum.

```python
counts = torch.bincount(y_test * 10 + predictions, minlength=100).reshape(10, 10)
print(torch.equal(counts, torch.tensor(cm)))

correct = counts.diag().float()
precision = correct / counts.sum(dim=0)
recall = correct / counts.sum(dim=1)
for digit in (1, 2, 8):
    print(digit, round(precision[digit].item(), 3), round(recall[digit].item(), 3))
```

```text
True
1 0.873 1.0
2 1.0 0.887
8 1.0 0.904
```

- Class 1 has a recall of 1: all 1s were found. But its precision is low:
  other digits are also taken for "1".
- 2 and 8 are the opposite: everything the network calls "2" or "8" is right
  (precision 1), but it misses some of these digits.

## A per-class report

scikit-learn gives the measures of every class in one table. The **F1** score
is the harmonic mean of precision and recall: if either is low, F1 is low
too.

```python
from sklearn.metrics import classification_report

print(classification_report(y_test, predictions, digits=3))
```

```text
              precision    recall  f1-score   support

           0      1.000     1.000     1.000        54
           1      0.873     1.000     0.932        55
           2      1.000     0.887     0.940        53
           3      0.945     0.945     0.945        55
           4      1.000     0.963     0.981        54
           5      1.000     0.982     0.991        55
           6      0.981     0.981     0.981        54
           7      0.964     1.000     0.982        54
           8      1.000     0.904     0.949        52
           9      0.931     1.000     0.964        54

    accuracy                          0.967       540
   macro avg      0.970     0.966     0.967       540
weighted avg      0.969     0.967     0.967       540
```

- `support`: how many test examples the class has.
- `macro avg`: the plain mean over classes; every class counts the same.
- `weighted avg`: the mean weighted by the number of examples. With balanced
  classes the two are close.

## The most confused pair

Zeroing the diagonal and finding the largest number left tells which two
classes the network confuses most:

```python
mistakes = counts.clone()
mistakes.fill_diagonal_(0)
index = mistakes.argmax().item()
print(index // 10, index % 10, mistakes.max().item())
```

```text
2 1 4
```

True 2, predicted 1, four times. The next step would be to look at these
pictures: perhaps some 2s are written very thin.

## The top two predictions: top-k accuracy

Sometimes the network's first prediction is wrong but its second is right.
**Top-k accuracy** checks whether the right class is among the k classes with
the highest scores. On large multi-class datasets (thousands of classes),
top-5 accuracy is often reported.

```python
top2 = logits.topk(2, dim=1).indices
hit = (top2 == y_test[:, None]).any(dim=1)
print(round(hit.float().mean().item(), 3))
```

```text
0.994
```

Looking at the first two predictions, almost all test pictures are right: even
where the network went wrong, it put the right answer second.

## Summary

- Confusion matrix: row is the truth, column the prediction; the diagonal is
  right.
- Precision = diagonal ÷ column sum, recall = diagonal ÷ row sum.
- `torch.bincount(true * K + predicted)` builds the matrix in one line.
- `classification_report` gives a per-class table; `topk` gives top-k
  accuracy.
