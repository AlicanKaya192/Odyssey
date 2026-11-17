# Convolution

At the end of the previous section, moving a shape by three pixels made the
flat lists look nothing alike. In this section we build the cornerstone of
image networks, **convolution**. The idea: a small **kernel** (also called a
filter) slides over the picture and at every position asks "is my pattern
here?". Because the same kernel is used everywhere, the pattern is found
wherever it moves.

## Convolution by hand

We place a 3 × 3 kernel over every 3 × 3 patch of the picture, multiply the
matching numbers, add them up and write the result at that position of the
output. Then we move one column to the right.

```python
import torch

image = torch.tensor([
    [0, 0, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 1],
], dtype=torch.float32)
kernel = torch.tensor([
    [-1, 0, 1],
    [-1, 0, 1],
    [-1, 0, 1],
], dtype=torch.float32)


def convolve(img, k):
    kh, kw = k.shape
    out_h, out_w = img.shape[0] - kh + 1, img.shape[1] - kw + 1
    out = torch.zeros(out_h, out_w)
    for r in range(out_h):
        for c in range(out_w):
            patch = img[r:r + kh, c:c + kw]
            out[r, c] = (patch * k).sum()
    return out


result = convolve(image, kernel)
print(result.shape)
print(result.tolist())
```

```text
torch.Size([2, 4])
[[0.0, 3.0, 3.0, 0.0], [0.0, 3.0, 3.0, 0.0]]
```

- The left of the picture is dark (0), the right bright (1); between them is a
  vertical **edge**.
- The kernel's left is negative, its right positive: where the left is dark
  and the right bright it gives a large number. In flat areas left and right
  cancel and the result is 0.
- The output is smaller than the picture: a 3 × 3 kernel fits into a 4 × 6
  picture in only 2 × 4 places.

This kernel is a **vertical edge detector**. In deep learning we will not
write the kernels' numbers ourselves; the network learns them during
training. But the first kernels it learns are very often exactly such edge
and corner detectors.

## In PyTorch: F.conv2d

PyTorch does the same computation in one call. The only difference is in the
shapes: `F.conv2d` expects the input as a batch `(N, C, H, W)` and the kernel
as `(output channels, input channels, kh, kw)`.

```python
import torch.nn.functional as F

x = image.reshape(1, 1, 4, 6)
w = kernel.reshape(1, 1, 3, 3)
out = F.conv2d(x, w)
print(out.shape)
print(torch.equal(out[0, 0], result))
```

```text
torch.Size([1, 1, 2, 4])
True
```

The result is exactly the same. Note: "convolution" in mathematics flips the
kernel first; what deep learning libraries do is really **cross-correlation**,
multiplying without flipping. Since the kernel is learned anyway, this does
not change the outcome; the name stays convolution.

## An edge detector on a shape

Let us apply the same idea to a picture of a square. We also build a
horizontal twin of the vertical kernel (its rows and columns swapped). We draw
the square by hand to keep it clean: 1 inside, 0 outside.

```python
square = torch.zeros(1, 1, 8, 8)
square[0, 0, 2:6, 2:6] = 1
vertical = kernel.reshape(1, 1, 3, 3)
horizontal = kernel.T.reshape(1, 1, 3, 3)
edge_x = F.conv2d(square, vertical)
edge_y = F.conv2d(square, horizontal)
print(edge_x.shape)
print(edge_x[0, 0, 2].tolist())
print(edge_y[0, 0, :, 2].tolist())
print((edge_x != 0).sum().item(), (edge_y != 0).sum().item())
```

```text
torch.Size([1, 1, 6, 6])
[3.0, 3.0, 0.0, 0.0, -3.0, -3.0]
[3.0, 3.0, 0.0, 0.0, -3.0, -3.0]
24 24
```

- The vertical kernel responds on the square's **left and right** edges:
  positive on the left (dark to bright), negative on the right (bright to
  dark).
- The horizontal kernel finds the **top and bottom** edges.
- There is no response inside or outside the square.

The same two kernels on a noisy shape picture:

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="349.2pt" height="125.709182pt" viewBox="0 0 349.2 125.709182" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 125.709182 
L 349.2 125.709182 
L 349.2 0 
L 0 0 
L 0 125.709182 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g clip-path="url(#p96b72758cf)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAIkAAACJCAYAAAAYJBvJAAAEdElEQVR4nO3dyUozSwBA4Y4mEpVookaJccIJNyKCuBZ8Ex/One8guFZ0oyIqCGKc5zgPP3mBPg3VV5R7vm0VZSKHFovu6kwul/uOwPv7e+x4qVSiJaJ6vR47/vb2hmtkMpnY8e9v/CpRX19f7PjZ2VkUanh4GOdUKpUo9Pe+sbGBa2Sz2djx0dFRXKMJZ+h/z0iEjETISISMRMhIhIxEyEiEMj09PbgD1dLSEjt+cnIShcrn8zjn5eUl+Of09/fHjt/f3wf/jMfHx+DPkeT3OjAwgGscHx9HobySCBmJkJEIGYmQkQgZiZCRCGXy+Tzuk9DNPIVCAX/Q5eVlFIpuGKpWq7hGkht1SC6Xix0fHBzENQ4PD3HO+Ph47Pj+/n70E7ySCBmJkJEIGYmQkQgZiZCRCBmJUOOROH7s7QcsLy8HPxn38PCAa9Rqtdjxzs5OXKOnpyf4uywuLuKcpaWloKfz0rrJyiuJkJEIGYmQkQgZiZCRCBmJULapqSn4Zh/ae0giyQ1D9HBWV1dX8GlJ19fXuMbT01Ps+PT0NK6xt7cX/Flvbm6CP+vr6yuu4ZVEyEiEjETISISMRMhIhIxEyEiEsl9fXzjp9vY2+q8dHBzgnNnZ2djx7e1tXKNYLMaOz83N4RofHx/BJx11d3fjnDROXWpubo4db2trwzW8kggZiZCRCBmJkJEIGYmQkQhl6bTnBtpLaW1txTWen5+D/1+n/ZpyuYxr0E02KysruMYc7KWMjIwE77UkOVGJXr/W0NHRETt+enqKa3glETISISMRMhIhIxEyEiEjETISoezn5ydOSjInVJIn59J4/VqpVAp+zdsrbMgled1ckifnaLOMNsqSbJa1t7fjGl5JhIxEyEiEjETISISMRMhIlM4+Cd2Y9Pb2Fv0VdLLT0NAQrrGzsxP0WrSGo6OjKFQaD2/RzWANXkmEjETISISMRMhIhIxEyEiEjESI38/1Q5tldDR5kmO0p6amcA26UWd9fR3X6IRXsCXZoExy0tFPKBQKOMcriZCRCBmJkJEIGYmQkQgZidLZJxkbGws+zZn+H0/yQNP8/Hzs+NraWvAr5JPcDFSA7zIxMYFr3N3dRb9Bks/hlUTISISMRMhIhIxEyEiEjETISIQad/F806SZmZnY8a2trR95CjCbzQbf7EPfZXNzM/otuuHGJHoaseHi4iL4c3glETISISMRMhIhIxEyEiEjETISpbOZloaBgYHY8ePj4+g3SON9gkkkOfKbjrtKcuR3vV6PQnklETISISMRMhIhIxEyEiEjUTr7JLR3kMa+AZ0elORpszTWSEMGTmRKerITvRotDcViEed4JREyEiEjETISISMRMhIhI5GR6A/ddPRX9Pb24pzz8/PoNyiXy8FP8E1OTuIa/rkRMhIhIxEyEiEjETISISPR79knWVhYiB1fXV3FNej1abu7u8GnJX18fEShKpUKzqnVajinWq3Gjl9dXeEaLy8vUSivJEJGImQkQkYiZCRCRiJkJEJGooj8A60VHFBZ6ybzAAAAAElFTkSuQmCC" id="image65725cd22c" transform="scale(1 -1) translate(0 -98.64)" x="7.2" y="-19.869182" width="98.64" height="98.64"/>
   </g>
   <g id="text_1">
    <text style="font-size: 9px; font-family:inherit; text-anchor: middle; fill: currentColor" x="56.435294" y="14.038594" transform="rotate(-0 56.435294 14.038594)">image</text>
   </g>
  </g>
  <g id="axes_2">
   <g clip-path="url(#p7403986639)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAIkAAACJCAYAAAAYJBvJAAAEKElEQVR4nO3du44TZxiH8W/GXmNvxvZCJKJISJGSNkGIggI6riF97oSLgzodTQqqIA4rYKX1cX0Yo80N/B+UT2ny/OpXY2wezUqv5tCc+v5UgM22KbVM2hs2uNuxueEQjS0OEzTXgK/a7a/QscrhwOZmMzR2tb4TZ1Yr9pEPfjyiuZYdTv9nRqLISBQZiSIjUWQkioxEkZEoMhJFw2PPNqlHtpwr3V9/5qHLS3awJ0/Q2LKZorm+Zx87H23izNX+LjpWd8E+88MHNkd+ukeP2LH2/QDNeSZRZCSKjESRkSgyEkVGoshIFBmJIiNRNBwUuEotbDtXXr6st16Eq8MVvIx0u2Vz83vwgMDHj2SqlNev621cHz5kxzprvcZVlfjnRpGRKDISRUaiyEgUGYkiI1E0PLVwSUa9epVn3r9nx3rxgs0t2dhPD+Di8NM6jry9nNa8lx39bLc+f84zf/wO7xiH/zjPJIqMRJGRKDISRUaiyEgUGYkiI1FkJIqGTUFP6CzHI3xE52BQ5xmY3+D8nM0tN2y73IED/vYr+93+fsu+65s3aKy0bcU1rxtX1eKfG0VGoshIFBmJIiNRZCSKjESRkSgankpTdatZLi7qXKj5DSovGEtZg2d5fvmCDjWbfY/mrq/RWBmPKz6LFPJMoshIFBmJIiNRZCSKjESRkSgyEkVGoojuIDlyEeaU3ZFPN4eTMXtawNU1u8Z1PJ7nz/zELkqd/3wPzfXw5VRo44ouhC2FPlHCM4kiI1FkJIqMRJGRKDISRUaiyEhUb5kG9zOl7HZ5ZjSqd6xb6/xIzVvD8x/Q3Lt3eeaX+/fRsejloWhJ9s/lkKXa79sc9mjOM4kiI1FkJIqMRJGRKDISRUaiyEgUGYnqPaJzt2Obwwl5/CbdpNI7vOHd7A18JxL65y3Zm5iaA3tb+Xp9F80tFuU/55lEkZEoMhJFRqLISBQZiSIjUWQkioxE9a5xhQvGMnn8uN7akG5c4TWu+3aC5uCStKrnz+stl2/gdnw0OkNznkkUGYkiI1FkJIqMRJGRKDISRUaiyEhUb+M6YcvKUp49q7fSpG9igrfkX7QVr3Ft4U8Hv+vTp+xwA/ZUTWS1YnOeSRQZiSIjUWQkioxEkZEoMhJFRqKoOfU9umOcXhJ3p82PfVzesMvmuu/Yzez09dzHbl7tcLMZXH6tF1UXgsf2rNqukj521TOJIiNRZCSKjESRkSgyEkVGoshIFBmJ6m1c8WM1wRpvc2Ab18kYblwpuooEN6ovV2wD3Z3YxvXUTau9dH3Qwt8N/p96JpGR6N/zTKLISBQZiSIjUWQkioxEkZGo3g3j+Bmd9OLPihZLtv2cnrfVXh3f0etvt+wnpi+nGoCvsNnCF1gVsL71TCLCPzeKjESRkSgyEkVGoshIFBmJIiNRSb4Czj7NNYN7ZPEAAAAASUVORK5CYII=" id="image4ad6b49da5" transform="scale(1 -1) translate(0 -98.64)" x="125.28" y="-19.869182" width="98.64" height="98.64"/>
   </g>
   <g id="text_2">
    <text style="font-size: 9px; font-family:inherit; text-anchor: middle; fill: currentColor" x="174.6" y="14.038594" transform="rotate(-0 174.6 14.038594)">vertical</text>
   </g>
  </g>
  <g id="axes_3">
   <g clip-path="url(#p874bc868b0)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAIkAAACJCAYAAAAYJBvJAAAD6ElEQVR4nO3dPY8TZxRH8WfsWbM2znrtUKCFCiHyFRAlH5sCiQYpSpsqEhIVTdjF8oJZ/DZRPsH5o1xBkfOrr8b7cjSWrh57ut1uGFqg75Op1roWXa7tDx3O3Nxkr3l+ns1NJtncdPQNZ479veha482n7EV3u2zudOKZ1Sq71t1dNDbKrqb/MyMRMhIhIxEyEiEjETISISMRMhKhblivh8p15R9/TqO516955s2b6FLt/v1sbj5vZabZr9nuZYvZ9vx5NvfsGc88eVK75PVOImQkQkYiZCRCRiJkJEJGImQkQkYi1MdryFHW0+FQd1Qz3aSGP1rbbuuOfj582EpVbo0Xs310reP8LJrzTiJkJEJGImQkQkYiZCRCRiJkJELd4ZB9YDw1bsdobhiNcaY7ZEuhfcuWQp8/t7K59Tq71uVlNpfuNJeTL3Vbw2Sj6Z1ECd9uhIxEyEiEjETISISMRMhIhIxEqBtOp6FyOxfPJecc07OQ6XdvppvI4HpfR9l5w3fvspc8y5bG7cGDui1v+q/yTiJkJEJGImQkQkYiZCRCRiJkJEJGop+wcU1tNu2HSw+5JpvZPnxK1NVVNHacTMv+DemPlvJOImQkQkYiZCRCRiJkJEJGImQkQkYi1A273VD6PZjpk3aS86vhY9LTM6772SKaOxsd687Lvn+fzV1cZHPn53VfURCuZr2TCBmJkJEIGYmQkQgZiZCRCBmJCo8vhr7turJjeOnXYKY7t3TPlzzLZnEx1B7TnM3qlpDp+cVwQeqdRMhIhIxEyEiEjETISISMRMhIhIxEqNtus4cipdvK9ORc8tntdAmZLhi7j3+XHREc5r+Unl5Mf4fkb/LrqnSJ7p1EzLcbISMRMhIhIxEyEiEjETISISMR6tbrbOOafkPn8q/fs8G3b3nm1atWKv0lVqu61+zDVeqLF9ncy5c4cnv1W+l23DuJkJEIGYmQkQgZiZCRCBmJkJEIGYlQv+i//PhDmOkn2pfL2q8VePQomzsGX9F5e5td6/o6m/vwIZu7ucGR2dPsUj6GXmV8uxEyEiEjETISISMRMhIhIxHqhs2m9Anjx/mibJeW7simh3CxVfjMnuEyW/QVP7KnjU/7uhcNzy96JxEyEiEjETISISMRMhIhIxEyEiEjUeFDkdItXqXkadrfYX/IHthU6awFG9LvERwjPZ660uc1eSeRkei/804iZCRCRiJkJEJGImQkQkYi1KdnV6+309JjpMm27/Hj7FrpA5umk+CD4P+eXx2Ny16zTbIP2n+9y7akk+Dvu91Gl2rLi+zv4Z1EyEiEjETISISMRMhIhIxEyEiEjESN/AM44eCwjq28aAAAAABJRU5ErkJggg==" id="imagea1b0d02a74" transform="scale(1 -1) translate(0 -98.64)" x="243.36" y="-19.869182" width="98.64" height="98.64"/>
   </g>
   <g id="text_3">
    <text style="font-size: 9px; font-family:inherit; text-anchor: middle; fill: currentColor" x="292.764706" y="14.038594" transform="rotate(-0 292.764706 14.038594)">horizontal</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p96b72758cf">
   <rect x="7.2" y="20.038594" width="98.470588" height="98.470588"/>
  </clipPath>
  <clipPath id="p7403986639">
   <rect x="125.364706" y="20.038594" width="98.470588" height="98.470588"/>
  </clipPath>
  <clipPath id="p874bc868b0">
   <rect x="243.529412" y="20.038594" width="98.470588" height="98.470588"/>
  </clipPath>
 </defs>
</svg>
<figcaption>A square and the output of the two edge kernels: red is a positive, blue a negative response.</figcaption>
</figure>

## Stride and padding

Two settings change the size of the output:

- **Stride**: how many pixels the kernel moves each time. A stride of 2 roughly
  halves the size of the output.
- **Padding**: a frame of zeros added around the picture. With a 3 × 3 kernel,
  1 pixel of padding keeps the output the same size as the input.

```python
x = torch.zeros(1, 1, 16, 16)
w = torch.zeros(1, 1, 3, 3)
for stride, padding in [(1, 0), (1, 1), (2, 0), (2, 1)]:
    out = F.conv2d(x, w, stride=stride, padding=padding)
    print(stride, padding, tuple(out.shape[2:]))
```

```text
1 0 (14, 14)
1 1 (16, 16)
2 0 (7, 7)
2 1 (8, 8)
```

The output size comes from a single formula (K kernel, P padding, S stride;
rounded down):

$$\text{output} = \left\lfloor \frac{H + 2P - K}{S} \right\rfloor + 1$$

16 pixels, kernel 3, padding 1, stride 2: `(16 + 2 − 3) // 2 + 1 = 8`.

## As a layer: nn.Conv2d

Inside a network we use convolution through the `nn.Conv2d` layer. The layer
keeps its own kernels (weights) and one **bias** per output channel; random
at the start, learned in training.

```python
from torch import nn

conv = nn.Conv2d(in_channels=1, out_channels=8, kernel_size=3, padding=1)
print(conv.weight.shape, conv.bias.shape)
count = sum(p.numel() for p in conv.parameters())
print(count, 8 * 1 * 3 * 3 + 8)
print(conv(torch.zeros(5, 1, 16, 16)).shape)

dense = nn.Linear(16 * 16, 16 * 16)
print(sum(p.numel() for p in dense.parameters()))
```

```text
torch.Size([8, 1, 3, 3]) torch.Size([8])
80 80
torch.Size([5, 8, 16, 16])
65792
```

- 8 output channels = 8 separate kernels. Each looks for a different pattern;
  the output has a **feature map** for each pattern: `(5, 8, 16, 16)`.
- The layer has 80 parameters in all. A fully connected (`Linear`) layer
  giving an output of the same size needs 65,792.
- There are two reasons for the gap: each output pixel looks only at a small
  neighbourhood (**local connectivity**) and the same kernel is used at every
  position (**weight sharing**).

## Several input channels

In a colour picture each kernel looks at all three channels at once: the
kernel's shape becomes `(3, 3, 3)` and the results of the three channels are
added.

```python
rgb = torch.ones(1, 3, 5, 5)
rgb[0, 1] = 2
rgb[0, 2] = 3
conv3 = nn.Conv2d(3, 1, kernel_size=3, bias=False)
with torch.no_grad():
    conv3.weight.fill_(1.0)
print(conv3.weight.shape)
print(conv3(rgb)[0, 0].tolist())
```

```text
torch.Size([1, 3, 3, 3])
[[54.0, 54.0, 54.0], [54.0, 54.0, 54.0], [54.0, 54.0, 54.0]]
```

At each position, 9 pixels of each of the three channels are added:
`9 × 1 + 9 × 2 + 9 × 3 = 54`. We changed the weight by hand inside
`torch.no_grad()`; this block tells PyTorch "do not record this operation for
learning".

## Summary

- Convolution: a small kernel slides over the picture, multiplying and adding
  at each position.
- `F.conv2d(x, w)`: `x` is `(N, C, H, W)`, `w` is `(out, in, kh, kw)`.
- The output size is `(H + 2P − K) // S + 1`; with 3 × 3, `padding=1` keeps
  the size.
- `nn.Conv2d` works with few parameters thanks to local connectivity and weight
  sharing; each output channel is a feature map.
