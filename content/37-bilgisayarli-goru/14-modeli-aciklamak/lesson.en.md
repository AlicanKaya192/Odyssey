# Explaining a Model

When a CNN says "this is a square", **where in the picture did it look** to
decide? Accuracy does not tell us. A famous example: a model separating wolves
from dogs gave very good results; explanation methods showed the model was
looking not at the animal but at the **snow** in the background (most wolf
pictures had been taken in snow). Such a **shortcut** does not show up on the
test set, because the test set carries the same flaw; in the real world it
breaks down.

In this section we will build two explanation methods: the **saliency map**
and **Grad-CAM**. For the second we will use PyTorch **hooks**: catching a
layer's output without touching the network's code.

## The model to explain

Let us train a small CNN on 24 × 24 single-shape pictures. After the last
convolution there is **global average pooling** (`AdaptiveAvgPool2d(1)`):
each channel's 6 × 6 map comes down to one number, and the classifier looks at
these 16 numbers.

```python
import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_shapes, SHAPES

images, labels = make_shapes(800, size=24, seed=1)
x, y = torch.tensor(images), torch.tensor(labels)
x_train, y_train, x_test, y_test = x[:600], y[:600], x[600:], y[600:]

torch.manual_seed(0)
model = nn.Sequential(
    nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(16, 16, 3, padding=1), nn.ReLU(),
    nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(16, 3),
)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
generator = torch.Generator().manual_seed(1)
for epoch in range(10):
    order = torch.randperm(600, generator=generator)
    for start in range(0, 600, 32):
        batch = order[start:start + 32]
        optimizer.zero_grad()
        F.cross_entropy(model(x_train[batch]), y_train[batch]).backward()
        optimizer.step()
model.eval()
with torch.no_grad():
    accuracy = (model(x_test).argmax(dim=1) == y_test).float().mean().item()
print(accuracy >= 0.95)
```

```text
True
```

Test accuracy is above 95%. But is the model looking at the shape?

## The saliency map: the gradient with respect to the input

The simplest question: "Which pixel, if changed a little, changes the class
score the most?" The answer is the **gradient of the score with respect to
the input**. So far we took gradients for the weights; the same `backward`
works for the input itself too, as long as `requires_grad` is on for the
input.

```python
def saliency(image):
    image = image[None].clone().requires_grad_(True)
    scores = model(image)
    scores[0, scores.argmax(dim=1).item()].backward()
    return image.grad.abs()[0, 0]


def inside_share(index, top=30):
    sal = saliency(x_test[index])
    shape = (x_test[index:index + 1] > 0.4).float()
    near_shape = F.max_pool2d(shape, 3, stride=1, padding=1)[0, 0] > 0
    strongest = sal.flatten().topk(top).indices
    return near_shape.flatten()[strongest].float().mean().item()


print(saliency(x_test[0]).shape)
shares = [inside_share(i) for i in range(len(x_test))]
print(round(sum(shares) / len(shares), 1))
```

```text
torch.Size([24, 24])
0.8
```

- The map has the same size as the picture: one sensitivity for each pixel.
- On average about 80% of the 30 strongest pixels are on the shape or within
  one pixel of it, while this region covers only about a quarter of the
  picture on average. The model really is looking at the shape.
- `x_test > 0.4` gives the shape's pixels (noise is around 0.1, the shape is
  at least 0.6); `max_pool2d(..., 3, stride=1, padding=1)` widens this mask by
  one pixel in every direction, so the area just outside the edge counts too.

Saliency maps are noisy and speak about single pixels. Often we want a
coarser but more readable map: at the level of **regions**.

## A hook: catching a layer's output

Grad-CAM needs the output of the last convolution layer. `nn.Sequential` does
not hand it out; instead of changing the network's code we attach a **forward
hook** to the layer: a small function called every time the layer runs.

```python
captured = {}


def save_output(layer, inputs, output):
    captured["maps"] = output


handle = model[7].register_forward_hook(save_output)
model(x_test[:1])
print(model[7], captured["maps"].shape)
```

```text
ReLU() torch.Size([1, 16, 6, 6])
```

- `model[7]` is the `ReLU` after the last convolution: its output is
  `(1, 16, 6, 6)`, each of the 16 channels a 6 × 6 map. Each cell corresponds
  to a 4 × 4 region of the picture.
- `register_forward_hook` returns a **handle**; when the work is done the hook
  must be removed with `handle.remove()` (below).

## Grad-CAM

**Grad-CAM** (Gradient-weighted Class Activation Mapping) in three steps:

1. Take the last convolution maps (`A`) and the gradient of the class score
   with respect to these maps.
2. The mean of each channel's gradient is that channel's **weight**: "how
   important is this channel for this class".
3. The weighted sum of the maps with negative values set to zero (`ReLU`):
   the regions that speak for the class.

```python
def grad_cam(image, target=None):
    scores = model(image[None])
    if target is None:
        target = scores.argmax(dim=1).item()
    maps = captured["maps"]
    grads = torch.autograd.grad(scores[0, target], maps)[0]
    weights = grads.mean(dim=(2, 3), keepdim=True)
    cam = F.relu((weights * maps).sum(dim=1))[0]
    return cam.detach(), target


for index in range(3):
    cam, target = grad_cam(x_test[index])
    row, col = divmod(cam.argmax().item(), 6)
    ys, xs = torch.nonzero(x_test[index, 0] > 0.4, as_tuple=True)
    box = [xs.min().item(), ys.min().item(), xs.max().item(), ys.max().item()]
    print(SHAPES[target], (row, col), box)
```

```text
triangle (2, 2) [2, 6, 15, 20]
circle (4, 4) [8, 8, 22, 22]
square (1, 3) [9, 2, 17, 11]
```

- `torch.autograd.grad` gives the gradient only for the tensor we ask for; it
  does not touch the weights' `.grad`.
- The first picture is a triangle: the map peaks in cell (2, 2), that is rows
  and columns 8–11 of the picture; the shape's box spans x 2–15, y 6–20. The
  peak is on the shape.
- The map is 6 × 6; to lay it over the picture it is enlarged to 24 × 24
  (`F.interpolate`).

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="371.52pt" height="206.929533pt" viewBox="0 0 371.52 206.929533" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 206.929533 
L 371.52 206.929533 
L 371.52 0 
L 0 0 
L 0 206.929533 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g clip-path="url(#pa7a2dd9409)">
    <image xlink:href="data:image/png;base64,
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" id="imagefbb5e88d24" transform="scale(1 -1) translate(0 -77.76)" x="7.2" y="-19.009533" width="77.76" height="77.76"/>
   </g>
   <g id="text_1">
    <text style="font-size: 8px; font-family:inherit; text-anchor: middle; fill: currentColor" x="46.017391" y="13.27875" transform="rotate(-0 46.017391 13.27875)">triangle</text>
   </g>
  </g>
  <g id="axes_2">
   <g clip-path="url(#p2761fe6e3c)">
    <image xlink:href="data:image/png;base64,
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" id="image6f1b9a702e" transform="scale(1 -1) translate(0 -77.76)" x="100.08" y="-19.009533" width="77.76" height="77.76"/>
   </g>
   <g id="text_2">
    <text style="font-size: 8px; font-family:inherit; text-anchor: middle; fill: currentColor" x="139.17913" y="13.27875" transform="rotate(-0 139.17913 13.27875)">circle</text>
   </g>
  </g>
  <g id="axes_3">
   <g clip-path="url(#pecd8079cd8)">
    <image xlink:href="data:image/png;base64,
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" id="imagebd2bee6c97" transform="scale(1 -1) translate(0 -77.76)" x="193.68" y="-19.009533" width="77.76" height="77.76"/>
   </g>
   <g id="text_3">
    <text style="font-size: 8px; font-family:inherit; text-anchor: middle; fill: currentColor" x="232.34087" y="13.27875" transform="rotate(-0 232.34087 13.27875)">square</text>
   </g>
  </g>
  <g id="axes_4">
   <g clip-path="url(#pb767801eed)">
    <image xlink:href="data:image/png;base64,
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" id="image0b6d3dbedb" transform="scale(1 -1) translate(0 -77.76)" x="286.56" y="-19.009533" width="77.76" height="77.76"/>
   </g>
   <g id="text_4">
    <text style="font-size: 8px; font-family:inherit; text-anchor: middle; fill: currentColor" x="325.502609" y="13.27875" transform="rotate(-0 325.502609 13.27875)">square</text>
   </g>
  </g>
  <g id="axes_5">
   <g clip-path="url(#p979fae1e29)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAGwAAABsCAYAAACPZlfNAAAJ8UlEQVR4nO1dS28jWRWusqvKldiOE8edxO7pTs9kBhoJNqzYILFixZ5ZDBItkJgRQvMLmAHNr0AgIY26kQaN2LDhT7BggVrDo99JOokTO3Zcdr1H1Su+8126GmkW3Nb5drd0UnXLJ7e+ex73HLfX2yqd/8Dl5aUj4bo4Lkv4kxdoNpswLoqCZEx/V4dr167RtbOzsXi2b3gWzqfheiQTNNdhHDpdktnfuQHj2fiMZG7cRJl/PHzM81nDcVTMSCZa4rWg1SKZBl1R/F9DFWYZVGGWwXWcBhCL5/G3PsvSr+Rht27dgvGjR49IJgxDGMdxTDKdDnLN1dWSZHobW7Uyw52bKDNekcyagzzSDvj3KQrk5mWW13JY5vGzOhso9OzpU5LRFWYZVGGWQRVmGVRhlsF1HL/Wmm230cBcLK5IptFA3fd6GySzWiHR7uzsksx0isZjK2DjcTy+EM9mw7kpDOWGG5DMbn8E4+UFb0zCBhrg7YCfleUZjKOMnQZxA2Wu8infp+CNiISuMMugCrMMqjDL4DUbyBG+z9/o3/329zAuHf5GO8KxWzp57f+H5BkTHyUx3ydeoiG/02cujGbIB1tdNKQrBC7OJ4kikvnw5+/j3zjIRRXCFvJjWiQ859zl7UPNPsDkQNcVZhlUYZZBFWYZVGGWwW15A9gtjEZoTFY4OnoG40/vfkoyaYpEO5mck0yng8Z0smJS3e7t4H1OOAJ+Y/c6jEOfjeKLMUalh7t43wqnx0cw/uTjj0imSHHz0m7xpmyZ4Cao2eENzpNTnM+8we8VZ+iQCAJ+L11hlkEVZhlUYZbB8xsyFIrOzgrXhJO0NMhIY3Z7mzkjFUbwcMAZUWGJjub+sEcy68IB6zXYCN0coTG9ithh/fV9fC8vZ+fvoI+8+9YtzJCq8Ne//R3G08sJyQx392AcFMyFRyc4x5ZmTdkP/SRaBlWYZVCFWQa3778DhvPm5iYJTaZIogdvv0UyH/8ajc7C4UC2VyLRTo8xcvzi3jeEUdzkDcXl+Snet2n4vxNR4IbL8/nVR7+EcZpwSt2gj7/HuSFVO87x+W53m2QePEfDeVLyxiQp5k4ddIVZBlWYZVCFWQbPdzDqu5iygRk66ISMxguSmT6d1GZNdTvIYaNbb5BMFoljOAXzysFw86WR2gqxyNCaX/F7BcL+bxoyouYLjEKnBXNqLK61DJF0x8OH5Qa+LIqs9r10hVkGVZhlUIVZBlWYZXC/+7UflHVntqTtavKOe0L1n927RzJBE43XdTGusNZEj/5yfkIyrZZIn26zR78ocY4/+enPSGZ2hRuTdUMq3HiKxqwhC9uJRArbPOPfJwvxBzpfYRS/wnIl0tTVW28/9JNoGVRhlsE7fII1JfxX4KfbB2+SzPQMuabnF7X8tOZz2rMfiDRnj1O1t/qinkbG98mFXZqn7FgNfUxTN7y6zEB3EoPhvDnAaPL4GWZjVZgt0LGwyjgt/Pbtd2B8//59ktEVZhlUYZZBFWYZVGGWwfNfQWVy09EouNDKm9cxZe2DOz8kmT/c/Q2M1zrs1V4USMaDN4Yk8+DBA3z2iFPPfvHhBzBeb/Oz5nN8j60tNpyPznGzUjb4Pk1xDjs1nI3LS3xWt9smmeUyqo146AqzDKowy6AKswyeISmJEIpI7NkRF63K1tEhGxqM4k4Pv/8rl+tSbOyJjKP1kO+zM4BxlPOZ4ktRLLIo2ZAfiHRyk+N7XTiWp4aI/NnDhzButbm2SLuLHP/42Rc850vMrDJBV5hlUIVZBlWYZVCFWQb3m51vgT/alSW0K5IX53pbJW8WusLL3u1xNLlcw2v3/vRHkolc4dHf5rTnhUhZe/+9H5GMt0JDNZnynIMSvf6nFzznrIXG9NML9vpHogDK3JByHaXorU/EeeYKwyFuTJKEN1O6wiyDKswyqMIsgxeIKtq5OKZTocjwWxr47NyU10q2HZ1wG52ZqcyVrjhrEznjeML1LIZ7eH55dx+rY1c4+Rc6iN2AuXk1xZTzTofPZf/7VESKE+a5K1GYMnGYL4tS/mZ8n8UC5zObcfcIXWGWQRVmGVRhlkEVZhm8Voi7g8WCNx1Mj6/g4jdAtuW4c+fHJHP3889ri3q99+67MN5b5+itJ1K1k5TfIk1R5uKSST4tRNVSQ5XQVEQdipIN3lJsOkxp2KZNhoSuMMugCrMMqjDL4M0W+P3Ni3qtZobCi0mC3OdFnFnleXitTNkAf/7FP2G8t88ZUe4EuyrMz/nbn1ygEeomzBlRghyWeWuGtlZ4nnoVs2P3QqSp78ioedVa6vAJjD2Pf0ND5y2CrjDLoAqzDKowy6AKswzuwRpGnLcMxcFcUfCjaSDeQRs97wf7nPa8iLHStheytz7sIPEnhrTwyRg96IMOk/zhI0wZWyVcNGWW4rWFwyl1p6J3pqmoV5zL/svN2jRsx5DO3RItQUyp47rCLIMqzDKowiyD+3b328BhScyOy5Y4b9Tx2JG6v4Pc5+XMc/KccbvNnBEn+K13sc30CxTinHES8xGgVYo8EnT6JPOd730fxp/9+S8kc3iJvDsruG6IJ85zr1ZcnXtXOLEzw7ns83Pk3U6nQzK6wiyDKswyqMIsgyrMMri7/jdq+zgHrijG5RvSuQXvt5vs9j8QrTOODvmc2WCARvDS0DM6XMMI8+EZp8KFHdwEnU5mtUW9YkMl0bMEK3inLt+nLOPaFGvZW/T6dawe/t/Op0noCrMMqjDLoAqzDO6WfwActr+/T0JHj7HY1aiPZ4wrNHLRVlBW56pkRObQ3i73Xz47RcM0FFldFTa30Ah+cow8UyEW0ezEEElf5UjfV4b+y1mAhvws4s4QfdGyShrAFYZDrDdyfHxMMrvi99CWiq8B9JNoGVRhlkEVZhncdjCqNZz7PTx7G095Q9FbF55lQ6uKll9/Fm00ROP6WPRarhC00MsfGlK1L68WNfFdx5kuMHqQeDznKJ3Wnk2+eRPnPJ9zpEIa0/IsWIXBADdzej7sNYB+Ei2DKswyuL63WcthDdGyKvSYMxo5OjcDh7OUgiZey3MTsyA80capQiFKXWd0frg6JoT86ItaIxX2bmAU+PmYuzVsX8PiYCenLJMky//52FC/zxHwiwtsMamdIV4D6CfRMqjCLIMqzDK4zUYHGHxjgys5L0QfyIZhQ9EO8e/yFe9lmiKi2+122eCdcfRYwg/wPq6hrKoIkjtXwkiuUDi4MUlzTk9zGrihSVOWCcR8TBFnmXb9KhsTU09tXWGWQRVmGVRhlsFrNvFjX8r+S9W1Aq+1DJWuZQ0OT/R+Nt3b9B0fjURm1dFRffT2hKO3eVZvlJvele+T1fJuHC9f6sStMJlMXppFVWElek9HEbes0hVmGVRhlkEVZhlUYY5d+BIMljmnpTJTDAAAAABJRU5ErkJggg==" id="imagee3f9408252" transform="scale(1 -1) translate(0 -77.76)" x="7" y="-122.169533" width="77.76" height="77.76"/>
   </g>
  </g>
  <g id="axes_6">
   <g clip-path="url(#pa63a7f88b6)">
    <image xlink:href="data:image/png;base64,
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" id="image7ee746e1f8" transform="scale(1 -1) translate(0 -77.76)" x="100" y="-122.169533" width="77.76" height="77.76"/>
   </g>
  </g>
  <g id="axes_7">
   <g clip-path="url(#p3fafde44be)">
    <image xlink:href="data:image/png;base64,
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" id="image09b180416b" transform="scale(1 -1) translate(0 -77.76)" x="194" y="-122.169533" width="77.76" height="77.76"/>
   </g>
  </g>
  <g id="axes_8">
   <g clip-path="url(#p1f1611b25c)">
    <image xlink:href="data:image/png;base64,
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" id="image8be10616f2" transform="scale(1 -1) translate(0 -77.76)" x="287" y="-122.169533" width="77.76" height="77.76"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pa7a2dd9409">
   <rect x="7.2" y="19.27875" width="77.634783" height="77.634783"/>
  </clipPath>
  <clipPath id="p2761fe6e3c">
   <rect x="100.361739" y="19.27875" width="77.634783" height="77.634783"/>
  </clipPath>
  <clipPath id="pecd8079cd8">
   <rect x="193.523478" y="19.27875" width="77.634783" height="77.634783"/>
  </clipPath>
  <clipPath id="pb767801eed">
   <rect x="286.685217" y="19.27875" width="77.634783" height="77.634783"/>
  </clipPath>
  <clipPath id="p979fae1e29">
   <rect x="7.2" y="122.09475" width="77.634783" height="77.634783"/>
  </clipPath>
  <clipPath id="pa63a7f88b6">
   <rect x="100.361739" y="122.09475" width="77.634783" height="77.634783"/>
  </clipPath>
  <clipPath id="p3fafde44be">
   <rect x="193.523478" y="122.09475" width="77.634783" height="77.634783"/>
  </clipPath>
  <clipPath id="p1f1611b25c">
   <rect x="286.685217" y="122.09475" width="77.634783" height="77.634783"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Four test pictures and the model's decision on top, the Grad-CAM map below (enlarged to 24 × 24): the bright region is where speaks for the decision.</figcaption>
</figure>

Does the map's peak fall on the shape's box (with a one-cell margin) for all
test pictures?

```python
def peak_on_shape(index):
    cam, target = grad_cam(x_test[index])
    row, col = divmod(cam.argmax().item(), 6)
    ys, xs = torch.nonzero(x_test[index, 0] > 0.4, as_tuple=True)
    cy, cx = row * 4 + 1.5, col * 4 + 1.5
    in_y = ys.min().item() - 4 <= cy <= ys.max().item() + 4
    in_x = xs.min().item() - 4 <= cx <= xs.max().item() + 4
    return in_y and in_x


hits = sum(peak_on_shape(i) for i in range(len(x_test)))
print(hits / len(x_test) >= 0.95)
handle.remove()
print(len(model[7]._forward_hooks))
```

```text
True
0
```

- More than 95% of the peaks are on the shape: no sign of a shortcut for this
  model.
- After `handle.remove()` no hook is left on the layer (0). A hook that is not
  removed keeps being called on every run; running the same cell twice
  attaches two hooks (note: Hooks).

## How far should we trust an explanation?

- An explanation describes the **model**, not the world: the map says "the
  model looked here", not "this is the right place".
- Grad-CAM has the resolution of the last convolution (6 × 6 here): it cannot
  see fine detail. A saliency map is fine-grained but noisy.
- A way to test that a method really depends on the model: if the same map
  comes out of a network with random weights, the method describes the
  picture (its edges), not the model.
- If you suspect a shortcut, the strongest test is to build a test set
  **without** the shortcut (wolf pictures without snow).

## Summary

- Accuracy does not say what the model looks at; shortcuts do not show up on
  the test set.
- Saliency map: the gradient of the class score with respect to the input
  (`requires_grad`).
- A forward hook catches a layer's output; the handle is removed with
  `remove()`.
- Grad-CAM: channel weight = mean gradient; map = weighted sum + ReLU;
  enlarged to the picture size.
- An explanation describes the model; it has limits and ways to check it.
