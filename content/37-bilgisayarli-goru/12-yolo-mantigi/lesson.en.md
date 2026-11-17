# YOLO Logic

Early detectors classified thousands of candidate regions of an image one by
one: it was slow. The **YOLO** family (You Only Look Once) turned the question
around: the image passes through the network **once**, and the network gives
all boxes at once in a single output tensor. Real-time detection in video
spread with this idea. In this section we will not train a big YOLO model;
instead we will build its **logic**: the grid, the responsible cell, the target
tensor and decoding the output into boxes. Then we will see how to filter the
output of a ready-made YOLO library with our own code. In the capstone section
we will train our own small detector with this logic.

## The grid and the responsible cell

The image is split into an S × S **grid**. The cell that the **centre** of an
object falls into is **responsible** for finding that object. Let us split our
32 × 32 scenes into a 4 × 4 grid: each cell is 8 × 8 pixels.

```python
import torch
from dl_data import make_scenes, SHAPES

images, boxes, masks = make_scenes(100, size=32, seed=7)
S, size = 4, 32
cell = size / S
for x1, y1, x2, y2, label in boxes[0]:
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    print(SHAPES[label], (cx, cy), (int(cy // cell), int(cx // cell)))
```

```text
square (21.5, 11.5) (1, 2)
circle (24.0, 23.5) (2, 3)
triangle (11.5, 11.0) (1, 1)
```

Each line: the shape, its centre and the responsible cell (row, column). The
square's centre (21.5, 11.5) falls into the cell in row 1, column 2.

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="169.632pt" height="169.632pt" viewBox="0 0 169.632 169.632" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 169.632 
L 169.632 169.632 
L 169.632 0 
L 0 0 
L 0 169.632 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g clip-path="url(#p296035f20b)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAANgAAADYCAYAAACJIC3tAAALdklEQVR4nO3dS2tTbRTF8aQX2yZpjTa9QlGcOnCoIOhQivh5LSg40rkfQK22NNKb1Xq/5SXz7hWe/Z6VHOH/G/ZwcjnJ5pT17Oyn2el0Bo3A58+fG6VmZ2fDY79+/WrU2czMTHjs9+/flT7X9PR0eOzPnz+NOuj1ehf+/fj4ODxnfn4+PPb9+/fi65G9FnNzc+Gxy5cvF7+vwWCQOjYVHgHwv1FggBEFBhhRYIARBQYYUWCAUXOYMkYHO51OZfH9uGNw5dKlS8XR7vn5eXhscXExdV5EvY7otWefS2k2h1+Pslg6ey1mg+UdtbSjvk/Ra1ePubGxEZ5zdHQUHrt69Wp4jDsYYESBAUYUGGBEgQFGFBhgFMcwI5ozM8aZFCpRQ6pKR9vtdnhsamqqOBFcXV0Nz9nb20s1CUfW1tbCY3///k0lZxGV+rVarfBYlEyqx1NJobpO0WOqz199dz99+hQe4w4GGFFggBEFBhhRYIARBQYYUWDApJp9oybGs7OzVOyrotOoifXbt2/F5wz9/PmzUUpF8Wo2xI8fP4rj56obhJVoBsXQx48fi89T5yjdbjc8pr5TGeqzjJqE1ftSs2ZU0zF3MMCIAgOMKDDAiAIDjCgwwIgCA4yaCwsLg9KoW0XxKysr4bHDw8PS15eOR1W8nxnTrDq31YyKqiPmL1++FD9edpx19CsB9fkvLS2llgt+B93q/X4/PGdhYaHSX4Ko2RonJyfhMbXkwh0MMKLAACMKDDCiwAAjCgwwosAAo2ar1Qoz5ii2Vt3jjrg4Q0WuUed2NCp81GATdV5mzPi1a9dSSx1qaSKz1BEtF2S76Z8/f178Ou7cuZOK/dV1j36F8fXr19TSiXod3MEAIwoMMKLAACMKDDCiwIBJzeTo9XrFjY9VN75mZZpz1cZ32eQ0Shijazu0u7vbqJIaWa2Ss4ynT5+mPpNLQbKnxnerZt/t7e3i1+H47nIHA4woMMCIAgOMKDDAiAIDjCgwYFI7XEYNrnWJ4lWjqnqNV65cufDvx8fHjapFTaeqGVXNIVE7PkbUDI3M9X3x4kV4Tnap43LQMKuabJWqr6GidjjlDgYYUWCAEQUGGFFggBEFBhhRYMCkYvrMLpHjHDEdjVse2traCo/t7e0VP5faTVPt3JmZk6GeS0Xu0TEVdatZKNFMFnWOmoXy5s2b4q5+FYGrHTPVedEyzYcPH1Kd++oz5g4GGFFggBEFBhhRYIARBQYYUWDApGL6jGwUH3VTq65zFT+rCD8js2SRXc5Qu1hmfkEQjQofJXo8tYxwcHBQHI+rX26srq42MiOr1XJBFKtno3j1XNzBACMKDDCiwAAjCgwwosAAo+bS0tIgs+lc1aLN+aremG/o+vXrxTM5VJqp0qcoOVNpm6KSsyjpUo2v6vqur68XNQEPPXnyJDw2JV7Hq1evLvz7jRs3UmO/7927V9ycnf2uqWSXOxhgRIEBRhQYYESBAUYUGGBEgQGT2uEyis7V6GEV4Waohl7VFJuJuhcXF1Pvq9/vF0fTqvFV7SCaaSBWMXLVY6Sj78zQ48ePG6Xn3b17NzUeW43pjpqVq27oHuIOBhhRYIARBQYYUWCAEQUGGFFggFFzenp6ULpboepizkbuS0tLxRG4ojq3o5hejU5WcxdOT08bVWq1Wqkx3efn58XPpSL8zFwTtdTxQ0TnERWdq+dS1yL6rmV/PcIOl8CE8C8iYESBAUYUGGBEgQFGFBhg1Ox0OoPMoJfMABi1O2PU4awGkahO8Krj52jJYlT8HMXqVf/qwCFaVlHvNzuyfCH43mR2CB013juK1bNLDGrZijsYYESBAUYUGGBEgQFGFBhgNKNSmiiJU0mRejw1ryFKC7Npm2rAjJo9VcqZbXCO0rFMQutIR5Vo5oWahaKakZeXl8Nj0bXPpoiZ+RrZ75o6jzsYYESBAUYUGGBEgQFGFBhgRIEBk5rJUYeGVBW3q1i97qIx16MMBuHHVfv3NRCvPYr31WecvRZR47Zq6FVjutVr5A4GGFFggBEFBhhRYIARBQYYUWCA0UzUWa5GSat5B1WPOnZE8dHuktm5C3WJ26MdJNVIaPX5R9TunOoXEwcHB8W/plAzXra3txsZmRHearlIzYbhDgYYUWCAEQUGGFFggBEFBhhRYIDRjNrVMRPFqpg+swNjdgDMzs5Occe3ip/VdYp2zFS7X6pfKqj4eW1trXjojdqdUw3KiTrcz87OwnPW19fDY1/EsJyqhx6peD/6/NVSTCbaH+IOBhhRYIARBQYYUWCAEQUGGMUxnKCaR8dJbYqnRi73er3idEylWar5OTq2ubnZyDg5OSluSFXprUpOo2vYarXCc/r9fqrBuRd8JqrJttPphMeyo8mrHPs+xB0MMKLAACMKDDCiwAAjCgwwosCAusX0KjpVOxyq2QXRvA7VIKqOPXr0KDz28uXL4rj97du34TF1XjTz4vbt240M1ZwbRdO3bt0Kz3n9+nV4bHV19cK/7+/vh+eoCP+7iLOj5txut5uK4tX8l2j5QV1b9doV7mCAEQUGGFFggBEFBhhRYIARBQbULaZXncWqY1rF9FXP61CvMZpRoUY7q7kbu7u7xTF9ZhZKdmfMaC7IqPcVzVdRyzRqTkov6JhXv1ZQv3BQ1PcpWkpQMb16z2ppgjsYYESBAUYUGGBEgQFGFBhQtxRRNbeq1Ec1YEaPqR5PJVaqSXRra+vCvz979izV7Kkm5z58+LDSeRIqpY2S0+zE2ugzUamZasCeEZ9XNF8lOwtFzRrJJJNqI0hmcgATwr+IgBEFBhhRYIARBQYYUWBA3WJ6FXOqhk41cjvT7Ksi3Pfv34fH2u128TyRqGl3VJNo1NSr4vasaLng6OgoFWdHSwnq2qrPZE6MOo9i8OyShWrOzW6ml8EdDDCiwAAjCgwwosAAIwoMMKLAgLrF9NFI5VGRdTTjQY1OVnM81HOpyD3q+L5//354zs7OTnjswYMHjVJqFobqSFfvOeqmV9dCxeDv3r278O83b95M7SyqRPG+mkGilgTUTpsZy8vLqWvIHQwwosAAIwoMMKLAACMKDDCiwIC6xfSHh4fFcfso0eAQ1TGtOtxV535EPZeKYjNUt7eK4pVoF87Nzc3U+1pbWyvuzlexeksMy4muvbpOahCNGogTLRep79PJyUkjgzsYYESBAUYUGGBEgQFGFBhgNIx8iodDqDRIjWnOPGb28VSDq2oS/ZdFyZlqsp6dnQ2PqUbrqk0FaaFKCtUobmVlZaW4QTia4zKqOZs7GGBEgQFGFBhgRIEBRhQYYESBAXWL6dW45WhU9Lij82g+xagdCTPUfI1oTLNq6M02+6pdMzPNvlHsn43Hm6IROIq61SwM1YCrYvVo+UEtWajdWdVyBncwwIgCA4woMMCIAgOMKDDAiAID6hbTZ3W73eJdM1X0XPWcjH9B1Ak+alZGREXu0YyK09PTxrgsiBkv2THd4/xlAXcwwIgCA4woMMCIAgOMKDDAiAIDjJrz8/NhTB8NHFFDVKqW7cBX8X40SEeNzlbHqqaic9VpnxkclInB1TnqlwoDcQ2jXySoz3+cywXZMe3cwQAjCgwwosAAIwoMMKLAgEk1+0bzELKbkWXTsTokRSo5VclZNBtEnaPmP5yfn4fH5ubmiuaC1OkzmQpGZ6vNA/f39yt9LnUtssk5dzDAiAIDjCgwwIgCA4woMMCIAgOMmu12e1BlU+zGxkbx3I3sfIUolh4VTWeiczWKW+34GTWkRlHxqF0d1fjpqhuSo/HTqgFXNb4qmc+k6tkw6rmyr4M7GGBEgQFGFBhgRIEBRhQYYESBAZPqph9ndDpOUcysYm4VnVdtnFG8EnX1q45+pS12nYx2uKzLdcru6sodDDCiwAAjCgwwosAAIwoMMKLAgIbPfzVYdfHz3jXrAAAAAElFTkSuQmCC" id="imagefa9bce5281" transform="scale(1 -1) translate(0 -155.52)" x="7.2" y="-6.912" width="155.52" height="155.52"/>
   </g>
   <g id="patch_2">
    <path d="M 84.816 46.008 
L 123.624 46.008 
L 123.624 84.816 
L 84.816 84.816 
z
" clip-path="url(#p296035f20b)" style="fill: #ff7f0e; opacity: 0.35; stroke: #ff7f0e; stroke-linejoin: miter"/>
   </g>
   <g id="patch_3">
    <path d="M 89.667 41.157 
L 133.326 41.157 
L 133.326 84.816 
L 89.667 84.816 
L 89.667 41.157 
z
" clip-path="url(#p296035f20b)" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
   <g id="patch_4">
    <path d="M 123.624 84.816 
L 162.432 84.816 
L 162.432 123.624 
L 123.624 123.624 
z
" clip-path="url(#p296035f20b)" style="fill: #9467bd; opacity: 0.35; stroke: #9467bd; stroke-linejoin: miter"/>
   </g>
   <g id="patch_5">
    <path d="M 109.071 104.22 
L 138.177 104.22 
L 138.177 138.177 
L 109.071 138.177 
L 109.071 104.22 
z
" clip-path="url(#p296035f20b)" style="fill: none; stroke: #9467bd; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
   <g id="patch_6">
    <path d="M 46.008 46.008 
L 84.816 46.008 
L 84.816 84.816 
L 46.008 84.816 
z
" clip-path="url(#p296035f20b)" style="fill: #2ca02c; opacity: 0.35; stroke: #2ca02c; stroke-linejoin: miter"/>
   </g>
   <g id="patch_7">
    <path d="M 46.008 41.157 
L 79.965 41.157 
L 79.965 79.965 
L 46.008 79.965 
L 46.008 41.157 
z
" clip-path="url(#p296035f20b)" style="fill: none; stroke: #2ca02c; stroke-width: 1.5; stroke-linejoin: miter"/>
   </g>
   <g id="line2d_1">
    <path d="M 7.2 46.008 
L 162.432 46.008 
" clip-path="url(#p296035f20b)" style="fill: none; stroke: #1f77b4; stroke-width: 0.8; stroke-linecap: square"/>
   </g>
   <g id="line2d_2">
    <path d="M 46.008 162.432 
L 46.008 7.2 
" clip-path="url(#p296035f20b)" style="fill: none; stroke: #1f77b4; stroke-width: 0.8; stroke-linecap: square"/>
   </g>
   <g id="line2d_3">
    <path d="M 7.2 84.816 
L 162.432 84.816 
" clip-path="url(#p296035f20b)" style="fill: none; stroke: #1f77b4; stroke-width: 0.8; stroke-linecap: square"/>
   </g>
   <g id="line2d_4">
    <path d="M 84.816 162.432 
L 84.816 7.2 
" clip-path="url(#p296035f20b)" style="fill: none; stroke: #1f77b4; stroke-width: 0.8; stroke-linecap: square"/>
   </g>
   <g id="line2d_5">
    <path d="M 7.2 123.624 
L 162.432 123.624 
" clip-path="url(#p296035f20b)" style="fill: none; stroke: #1f77b4; stroke-width: 0.8; stroke-linecap: square"/>
   </g>
   <g id="line2d_6">
    <path d="M 123.624 162.432 
L 123.624 7.2 
" clip-path="url(#p296035f20b)" style="fill: none; stroke: #1f77b4; stroke-width: 0.8; stroke-linecap: square"/>
   </g>
   <g id="line2d_7">
    <defs>
     <path id="m6954b8bf7d" d="M 0 2 
C 0.530406 2 1.03916 1.789267 1.414214 1.414214 
C 1.789267 1.03916 2 0.530406 2 0 
C 2 -0.530406 1.789267 -1.03916 1.414214 -1.414214 
C 1.03916 -1.789267 0.530406 -2 0 -2 
C -0.530406 -2 -1.03916 -1.789267 -1.414214 -1.414214 
C -1.789267 -1.03916 -2 -0.530406 -2 0 
C -2 0.530406 -1.789267 1.03916 -1.414214 1.414214 
C -1.03916 1.789267 -0.530406 2 0 2 
z
" style="stroke: #ff7f0e"/>
    </defs>
    <g clip-path="url(#p296035f20b)">
     <use xlink:href="#m6954b8bf7d" x="111.4965" y="62.9865" style="fill: #ff7f0e; stroke: #ff7f0e"/>
    </g>
   </g>
   <g id="line2d_8">
    <defs>
     <path id="m4c371b7b4d" d="M 0 2 
C 0.530406 2 1.03916 1.789267 1.414214 1.414214 
C 1.789267 1.03916 2 0.530406 2 0 
C 2 -0.530406 1.789267 -1.03916 1.414214 -1.414214 
C 1.03916 -1.789267 0.530406 -2 0 -2 
C -0.530406 -2 -1.03916 -1.789267 -1.414214 -1.414214 
C -1.789267 -1.03916 -2 -0.530406 -2 0 
C -2 0.530406 -1.789267 1.03916 -1.414214 1.414214 
C -1.03916 1.789267 -0.530406 2 0 2 
z
" style="stroke: #9467bd"/>
    </defs>
    <g clip-path="url(#p296035f20b)">
     <use xlink:href="#m4c371b7b4d" x="123.624" y="121.1985" style="fill: #9467bd; stroke: #9467bd"/>
    </g>
   </g>
   <g id="line2d_9">
    <defs>
     <path id="m8e5df6f143" d="M 0 2 
C 0.530406 2 1.03916 1.789267 1.414214 1.414214 
C 1.789267 1.03916 2 0.530406 2 0 
C 2 -0.530406 1.789267 -1.03916 1.414214 -1.414214 
C 1.03916 -1.789267 0.530406 -2 0 -2 
C -0.530406 -2 -1.03916 -1.789267 -1.414214 -1.414214 
C -1.789267 -1.03916 -2 -0.530406 -2 0 
C -2 0.530406 -1.789267 1.03916 -1.414214 1.414214 
C -1.03916 1.789267 -0.530406 2 0 2 
z
" style="stroke: #2ca02c"/>
    </defs>
    <g clip-path="url(#p296035f20b)">
     <use xlink:href="#m8e5df6f143" x="62.9865" y="60.561" style="fill: #2ca02c; stroke: #2ca02c"/>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p296035f20b">
   <rect x="7.2" y="7.2" width="155.232" height="155.232"/>
  </clipPath>
 </defs>
</svg>
<figcaption>A 4 × 4 grid: each object's centre (dot) and the cell responsible for it (shaded); purple circle, orange square, green triangle.</figcaption>
</figure>

## The target tensor

We write the answer the network should learn into a tensor. For every cell,
`5 + C` numbers:

1. **Objectness**: is there an object centre in this cell (1 / 0)?
2. Where the centre is **inside the cell**, between 0 and 1: `cx_cell`,
   `cy_cell`.
3. The width and height of the box, divided by the **image size**: `w`, `h`.
4. The one-hot encoding of the class: C numbers.

```python
C = 3


def encode(scene_boxes):
    target = torch.zeros(S, S, 5 + C)
    for x1, y1, x2, y2, label in scene_boxes:
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        row, col = int(cy // cell), int(cx // cell)
        target[row, col, 0] = 1
        target[row, col, 1] = cx / cell - col
        target[row, col, 2] = cy / cell - row
        target[row, col, 3] = (x2 - x1) / size
        target[row, col, 4] = (y2 - y1) / size
        target[row, col, 5 + label] = 1
    return target


target = encode(boxes[0])
print(target.shape)
print(target[..., 0].int().tolist())
print([round(v, 3) for v in target[1, 2].tolist()])
```

```text
torch.Size([4, 4, 8])
[[0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]]
[1.0, 0.688, 0.438, 0.281, 0.281, 0.0, 1.0, 0.0]
```

- The tensor is `(4, 4, 8)`: 16 cells, 8 numbers in each.
- Three cells in the objectness map are 1: three objects.
- The square's cell: the centre is in the right half of the cell (0.6875) and
  near its middle (0.4375), the width and height are 28% of the image, class 1
  (square).
- Writing the centre relative to the cell lets the network learn small,
  bounded numbers in each cell. If the centres of two objects fall into the
  same cell, one is lost in this simple form; anchors (below) are for that.

## Decoding the output into boxes

The network's output is a tensor of the same shape. Turning it back into a
list of boxes is called **decoding**. Let us assume the network predicted
perfectly and decode the target tensor:

```python
def decode(output, threshold=0.5):
    found = []
    for row in range(S):
        for col in range(S):
            objectness = output[row, col, 0].item()
            class_probs = output[row, col, 5:]
            score = objectness * class_probs.max().item()
            if score < threshold:
                continue
            cx = (col + output[row, col, 1].item()) * cell
            cy = (row + output[row, col, 2].item()) * cell
            w = output[row, col, 3].item() * size
            h = output[row, col, 4].item() * size
            label = class_probs.argmax().item()
            corners = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
            found.append(corners + [label, score])
    return found


for box in decode(target):
    print([round(v, 2) for v in box])
print(sorted(boxes[0]))
```

```text
[8.0, 7.0, 15.0, 15.0, 2, 1.0]
[17.0, 7.0, 26.0, 16.0, 1, 1.0]
[21.0, 20.0, 27.0, 27.0, 0, 1.0]
[[8, 7, 15, 15, 2], [17, 7, 26, 16, 1], [21, 20, 27, 27, 0]]
```

- The decoded boxes are the same as the true boxes (ordered by cell).
- In a real network objectness and class probabilities are between 0 and 1;
  the **confidence score** of a box is their product: "there is an object
  here" × "this object is of this class".
- What comes after decoding is familiar from the previous section: a
  confidence threshold and per-class NMS.

## Anchors and anchor-free detection

A cell may hold more than one object, and objects have very different shapes
(a standing person is tall and narrow, a car is wide and low). Classic YOLO
versions use several **anchor** boxes in each cell: width–height pairs chosen
in advance. The network predicts the size of the box not from scratch but as a
**scale** relative to the anchor:

```python
import math

anchor_w, anchor_h = 8.0, 16.0
tw, th = math.log(1.5), math.log(0.5)
w = anchor_w * math.exp(tw)
h = anchor_h * math.exp(th)
print(round(w, 3), round(h, 3))
```

```text
12.0 8.0
```

The predicted `tw = log 1.5` turns the anchor's width into 1.5 times itself
(12), `th = log 0.5` turns its height into half (8). Thanks to `exp` the size
is never negative. Most newer versions are **anchor-free**: each location
predicts the distances to the box edges or the size directly; there is no
need to tune anchors to the data set.

## A ready-made YOLO library

In real projects we often use YOLO through a ready-made library with
pretrained weights. With Ultralytics, one of the common libraries, code that
finds people in a video looks roughly like this (we do not run it in this
module: the library is AGPL-licensed and downloads its weights from the
internet):

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
for result in model("street.mp4", stream=True):
    boxes = result.boxes
    print(boxes.xyxy.shape, boxes.conf[:3], boxes.cls[:3], model.names[0])
```

Sample output format (not a measurement; the values depend on the image and
the model):

```text
torch.Size([5, 4]) tensor([0.91, 0.87, 0.42]) tensor([0., 0., 2.]) person
```

In each frame `boxes.xyxy` holds `(N, 4)` pixel coordinates, `boxes.conf` N
confidence scores, `boxes.cls` N class numbers; `model.names` is a dictionary
from number to class name. The library applies NMS and a confidence threshold
internally (changeable with the `conf=` and `iou=` settings).

## Filtering the output with our own code

Whatever the library outputs, what follows is our job: keeping only the class
we want and boxes that are confident enough, doing our own NMS if needed,
counting how many people are in a frame. Let us build the same structure
(xyxy, conf, cls) by hand for two frames:

```python
from torchvision.ops import nms

names = {0: "person", 2: "car"}
frames = [
    {"xyxy": torch.tensor([[10.0, 10, 30, 60], [12, 11, 31, 62],
                           [50, 20, 90, 45], [100, 5, 120, 55]]),
     "conf": torch.tensor([0.91, 0.62, 0.88, 0.35]),
     "cls": torch.tensor([0, 0, 2, 0])},
    {"xyxy": torch.tensor([[14.0, 12, 34, 62], [70, 8, 92, 60]]),
     "conf": torch.tensor([0.9, 0.77]),
     "cls": torch.tensor([0, 0])},
]


def people(frame, min_conf=0.5, iou=0.5):
    keep = (frame["cls"] == 0) & (frame["conf"] >= min_conf)
    xyxy, conf = frame["xyxy"][keep], frame["conf"][keep]
    return xyxy[nms(xyxy, conf, iou)]


for index, frame in enumerate(frames):
    print(index, len(people(frame)), people(frame).tolist())
```

```text
0 1 [[10.0, 10.0, 30.0, 60.0]]
1 2 [[14.0, 12.0, 34.0, 62.0], [70.0, 8.0, 92.0, 60.0]]
```

- The first frame has four boxes: one is a car (class 2), one is below the
  confidence threshold (0.35); the two remaining person boxes were drawn on
  the same person and NMS dropped one. Result: 1 person.
- Two people in the second frame.
- The same filtering works unchanged with the tensors coming from the real
  library's `result.boxes`.

## Summary

- YOLO: the image passes through the network once; the output is a tensor
  like S × S × (5 + C).
- The cell the object's centre falls into is responsible; the target:
  objectness, centre inside the cell, size relative to the image, class.
- Decoding: cell + offset → pixels; confidence = objectness × class
  probability; then threshold and NMS.
- Anchors make the network predict size as a scale; newer versions are mostly
  anchor-free.
- The output of a ready-made library (xyxy, conf, cls) is filtered with our
  own code.
