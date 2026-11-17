# Image Data

In this module we will teach a computer to "see": we will build networks that
say which shape is in a picture, mark where objects are with boxes and find
what each pixel belongs to. All of them start from the same question: **what
is a picture to a computer?** The answer is surprisingly plain: a table of
numbers. In this section we learn the shape of that table, the type and range
of its numbers and the order in which PyTorch expects images. Most mistakes in
the later sections come from a misunderstanding here.

## An image is a table of numbers

The `load_digits` dataset that ships with scikit-learn contains handwritten
digits (no internet needed). Each digit is an 8 × 8 pixel picture; each pixel
is a number between 0 (empty) and 16 (full).

```python
import torch
from sklearn.datasets import load_digits

digits = load_digits()
image = torch.tensor(digits.images[0])
print(image.shape, image.dtype)
print(image.min().item(), image.max().item())
print(image[3].tolist())
print(digits.target[0])
```

```text
torch.Size([8, 8]) torch.float64
0.0 15.0
[0.0, 4.0, 12.0, 0.0, 0.0, 8.0, 8.0, 0.0]
0
```

- `image.shape` gives the image's **dimensions**: 8 rows, 8 columns. We call
  the number of rows the **height** and the number of columns the **width**.
- `image[3]` is the fourth row: the brightness of eight pixels from left to
  right.
- The brightest pixel in this image is 15; its label is `0`: a zero.

Drawn as a picture, the same table looks like a digit to our eyes:

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="349.2pt" height="77.345759pt" viewBox="0 0 349.2 77.345759" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 77.345759 
L 349.2 77.345759 
L 349.2 -0 
L 0 -0 
L 0 77.345759 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g clip-path="url(#p37b7a6b232)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEIAAABCCAYAAADjVADoAAABWElEQVR4nO3a0Y2CQBRA0XGzDVCCUgKWYAu0YAu2oC1YApYALWgHUIKWwGaz93tmkqcfm9zzOwbIzSS8jGzWdV1T0PV6za6fz+fs+n6/L95jGIb0SV8fvfo/YggYAoaAIWAIGAKb0hyxLEsq6bouNGfcbrfiPeZ5zq7f7/cU4Y6AIWAIGAKGgCFgCBgC36lgqRioSgcrfd9n1w+HQ/Eepd9cLpfs+ul0yq67I2AIGAKGgCFgCBiido54vV7hg5mSpmnCs0rNc+a4I2AIGAKGgCFgCBiido5oKt7x4ziGPhSpUfMcEe4IGAKGgCFgCBgChoAh3jlQPR6P0J9Eu92ueI/SFzHRwyF3BAwBQ8AQMAQMAUPUzhFdxft5u91m19u2DX1I8muapuz68XhMEe4IGAKGgCFgCBgChqidI2pEP/asOfN4Pp/ha+S4I2AIGAKGgCFgCBgi/fkBLxFDHMCpu68AAAAASUVORK5CYII=" id="image9b1e1cde74" transform="scale(1 -1) translate(0 -47.52)" x="7.2" y="-22.625759" width="47.52" height="47.52"/>
   </g>
   <g id="text_1">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="31.114286" y="16.317187" transform="rotate(-0 31.114286 16.317187)">0</text>
   </g>
  </g>
  <g id="axes_2">
   <g clip-path="url(#pc6b81ed724)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEIAAABCCAYAAADjVADoAAABFUlEQVR4nO3bQQ2DMBhA4bJMAE5AAhJwAFKQgAOwgBOkgAJ22Du3JF05LO+7/luavHRJM0p1XdcVCuv7Pjrfti06H4Yhuca6riHHK+vbf8QQMAQMAUPAEDAE3iHTcRzJz6TOCSld14XS3BEwBAwBQ8AQMAQMAUPAEDAEDAFDwBAwBAwBQ/zqj5kntG1bfA13BAwBQ8AQMAQMAUPcPUfM8xydT9MUSqvruvga7ggYAoaAIWAIGAKGgCFQ5d683fc9+8bLeZ7R+bIsyTXGcQw53BEwBAwBQ8AQMAQM8asHPO2Nhy+pc0TqZu6ds0oudwQMAUPAEDAEDAFDPHlR5Ei85dM0TXTuGzwP8qcBQ8AQMAQMAUOErw/dVysIVXgXkAAAAABJRU5ErkJggg==" id="imageef7f643da5" transform="scale(1 -1) translate(0 -47.52)" x="64.8" y="-22.625759" width="47.52" height="47.52"/>
   </g>
   <g id="text_2">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="88.508571" y="16.317187" transform="rotate(-0 88.508571 16.317187)">1</text>
   </g>
  </g>
  <g id="axes_3">
   <g clip-path="url(#p261d500796)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEMAAABCCAYAAAAMlmvWAAABV0lEQVR4nO3awY2CQBhA4XGzdy2BErQDOpAS7ABKwA4sgQ7ACmwBOrAEO2CP+04zkIGT77v+BpKXOfxxOMzzPIedjeOY/E3bttH58/mMzuu6Tr7j8XhE5z/JJ3wRY4AxwBhgDDAGGAN+wwZ7wu12i86naQq5rtdrdF6WZfY7PBlgDDAGGAOMAcYAY4Ax1i5dXdftvlT1fR+dV1UV9ubJAGOAMcAYYAwwBhgDDksukT6fT9blzDAMqVeE9/udNT+dTiGXJwOMAcYAY4AxwBhgjLV7Ru4esmTPaJom65JoyTtSPBlgDDAGGAOMAcYAY4Axtl662sTXvUsWotQl0f1+j863+NDZkwHGAGOAMcAYYAwwxtZ7xpj4gvhyuSSfcTwesy6JUpdMS3gywBhgDDAGGAOMAcZY+1Fsyvl8js5fr1f2/xlFUYS9eTLAGGAMMAYYA4wBxgj//gCy2FSPmbyptAAAAABJRU5ErkJggg==" id="imageebde2da010" transform="scale(1 -1) translate(0 -47.52)" x="121.68" y="-22.625759" width="48.24" height="47.52"/>
   </g>
   <g id="text_3">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="145.902857" y="16.317187" transform="rotate(-0 145.902857 16.317187)">2</text>
   </g>
  </g>
  <g id="axes_4">
   <g clip-path="url(#p1a94bda39a)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEMAAABCCAYAAAAMlmvWAAABR0lEQVR4nO3awY2DMBQAUWe1DVACSgm0kLQCLVACKQFKSA1pJbSQEljltHOyQd+5RPOuFkEaOdKXzWnbti0F3W637Po8z9FXpOv1+vF3/IR/4YsYA4wBxgBjgDHAGPCbKni9Xtn1ZVlCz7/1fZ8i9swh7gwwBhgDjAHGAGOAMcAYtYeuaZpCz+8ZukqHO03TpCh3BhgDjAHGAGOAMcAYcKpxiRSdIy6XS4p6PB7hOcSdAcYAY4AxwBhgDDBG7fOMdV2z6+fzOTxn3O/37LrnGZX5NwFjgDHAGGAMMAYY48jQtRYGqj0DT9u22fXn8xl+Rw3uDDAGGAOMAcYAY4AxjswZS+Hr3j0HL+M4ZteHYQhfEtW4iHJngDHAGGAMMAYYA4xxZM6YdnzwWjprKM0RpfOOt67r0qe5M8AYYAwwBhgDjAHGSP/+APvVPbJdGsaRAAAAAElFTkSuQmCC" id="image4c3b79e7c1" transform="scale(1 -1) translate(0 -47.52)" x="179.28" y="-22.625759" width="48.24" height="47.52"/>
   </g>
   <g id="text_4">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="203.297143" y="16.317187" transform="rotate(-0 203.297143 16.317187)">3</text>
   </g>
  </g>
  <g id="axes_5">
   <g clip-path="url(#pde12e8f268)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEIAAABCCAYAAADjVADoAAABWElEQVR4nO3bQY3CQBhA4elm71RCUVALlVAH1AFIwAEWkFAHYKEOcEBR0M1m33n+JgM9bN53/QOTvAzJZFqqZVmW9GGPxyM73+/32fntdgvX6Loulfgq+vQ/YggYAoaAIWAIGALfaQPzPGfnu90uO79er+EaniPexJ8GDAFDwBAwBAwBQ6CKLmbu93tunPq+T5HX65Wdt22bnU/TFK7xfD6z87qus3N3BAwBQ8AQMAQMAUOsvZiZg0uV6Izw63A4FF28VFUVrjGOY3Y+DEN27o6AIWAIGAKGgCFgiLXniD64b7hcLtFXpPP5nEocj8fil1Ei7ggYAoaAIWAIGAKGgCHWPuApvbhZ8zbL6XQq+vwaTdNk5+4IGAKGgCFgCBgChnjXm7d18ALGmocr0aVKdAZ4B3cEDAFDwBAwBAwBQ2z5D54hOEdE8y24I2AIGAKGgCFgCBgi/fkBsuZEildGL9MAAAAASUVORK5CYII=" id="image025059bbf6" transform="scale(1 -1) translate(0 -47.52)" x="236.88" y="-22.625759" width="47.52" height="47.52"/>
   </g>
   <g id="text_5">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="260.691429" y="16.317187" transform="rotate(-0 260.691429 16.317187)">4</text>
   </g>
  </g>
  <g id="axes_6">
   <g clip-path="url(#p96d46670e6)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEIAAABCCAYAAADjVADoAAABS0lEQVR4nO3b0YnCQBRA0XHZf1NCSjEd2IElaAnpwNhBSjAVRDuwBEuIFWRZ9n7PCG9AWO75fZCBy4BDnGzWdV1TwOl0ys4vl0uKOhwO2fk4juE1vsJP+CcMAUPAEDAEDAFDYBM9R1yv1+y8aZriM/q+z87v93t2Ps9zcY3dbpeduyNgCBgChoAhYAgYAoaodaCq4Xa7Zedd12Xnx+OxuMYwDNm5OwKGgCFgCBgChoAh8J0+fEb49Xg8UkTbtinKHQFDwBAwBAwBQ8AQtc4R+/0+O5+mKbpEOp/Pocsq73BHwBAwBAwBQ8AQMAQMUetA9Xw+o49I2+029OJmWZbiGqWbO+4IGAKGgCFgCBgChqh1jlje+A0veb1eoT+J3rndW+KOgCFgCBgChoAhYIha54i2cEmj9OVMrS95o9wRMAQMAUPAEDAEDJH+/AAPyz/g3vqs6wAAAABJRU5ErkJggg==" id="imagec4d7697f1b" transform="scale(1 -1) translate(0 -47.52)" x="294.48" y="-22.625759" width="47.52" height="47.52"/>
   </g>
   <g id="text_6">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="318.085714" y="16.317187" transform="rotate(-0 318.085714 16.317187)">5</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p37b7a6b232">
   <rect x="7.2" y="22.317187" width="47.828571" height="47.828571"/>
  </clipPath>
  <clipPath id="pc6b81ed724">
   <rect x="64.594286" y="22.317187" width="47.828571" height="47.828571"/>
  </clipPath>
  <clipPath id="p261d500796">
   <rect x="121.988571" y="22.317187" width="47.828571" height="47.828571"/>
  </clipPath>
  <clipPath id="p1a94bda39a">
   <rect x="179.382857" y="22.317187" width="47.828571" height="47.828571"/>
  </clipPath>
  <clipPath id="pde12e8f268">
   <rect x="236.777143" y="22.317187" width="47.828571" height="47.828571"/>
  </clipPath>
  <clipPath id="p96d46670e6">
   <rect x="294.171429" y="22.317187" width="47.828571" height="47.828571"/>
  </clipPath>
 </defs>
</svg>
<figcaption>The first six digits of <code>load_digits</code>: each is 8 × 8 numbers.</figcaption>
</figure>

## Channels: a colour image

In a grey picture each pixel is one number. In a colour picture each pixel is
**three** numbers: the amount of red (R), green (G) and blue (B) light. Each of
these three layers is called a **channel**. Image files and NumPy usually keep
pixels in `(height, width, channel)` order; PyTorch puts the **channel
first**: `(channel, height, width)`.

```python
import numpy as np
import torch
from PIL import Image

rgb = np.zeros((4, 6, 3), dtype=np.uint8)
rgb[:, :3, 0] = 255
rgb[:, 3:, 2] = 255
picture = Image.fromarray(rgb)
print(picture.size, picture.mode)

x = torch.from_numpy(np.array(picture)).permute(2, 0, 1)
print(x.shape, x.dtype)
print(x[0, 0].tolist())
print(x[2, 0].tolist())
```

```text
(6, 4) RGB
torch.Size([3, 4, 6]) torch.uint8
[255, 255, 255, 0, 0, 0]
[0, 0, 0, 255, 255, 255]
```

- We built a picture with 4 rows and 6 columns: the left half red, the right
  half blue.
- **Careful:** Pillow's `size` is in `(width, height)` order: `(6, 4)`. NumPy's
  `shape` is `(4, 6, 3)`. The two libraries describe the same picture in a
  different order.
- `permute(2, 0, 1)` reorders the dimensions: the third one (channel) moves to
  the front. The result is `(3, 4, 6)`.
- `x[0]` is the red channel: the left of the first row is 255, the right 0.
  `x[2]` is the blue channel: the opposite.

## The type of the numbers: uint8 and float

Pixels in image files are stored as `uint8`: whole numbers from 0 to 255, one
byte per pixel. The type saves space but sets a trap in arithmetic.

```python
import torch
from torchvision.transforms import v2

a = torch.tensor([200, 100], dtype=torch.uint8)
print((a + a).tolist())
print((a.float() + a.float()).tolist())

to_float = v2.ToDtype(torch.float32, scale=True)
b = to_float(a)
print(b.dtype, [round(v, 3) for v in b.tolist()])
```

```text
[144, 200]
[400.0, 200.0]
torch.float32 [0.784, 0.392]
```

- `200 + 200` should be 400; `uint8` cannot hold anything above 255, so the
  number wraps around and gives `144` (400 − 256). **There is no error**; the
  result is silently wrong.
- Networks work with `float32`. When converting, pixels are usually divided
  by 255 and brought into **[0, 1]**: 200 → 0.784. torchvision's
  `v2.ToDtype(..., scale=True)` transform does this in one step.

## A batch of images: NCHW

We do not give pictures to a network one by one but as a **batch**. In PyTorch
a batch of images has the shape `(N, C, H, W)`: number of images, channels,
height, width. Throughout this module we use our own fixed-seed shape
pictures: each contains a circle, a square or a triangle.

```python
import torch
from dl_data import make_shapes, SHAPES

images, labels = make_shapes(300)
x = torch.from_numpy(images)
y = torch.from_numpy(labels)
print(x.shape, x.dtype, y.shape)
print(SHAPES)
print(torch.bincount(y).tolist())
print(round(x.min().item(), 2), round(x.max().item(), 2))
```

```text
torch.Size([300, 1, 16, 16]) torch.float32 torch.Size([300])
('circle', 'square', 'triangle')
[86, 109, 105]
0.0 1.0
```

- 300 pictures, 1 channel (grey), 16 × 16 pixels. The pixels are already
  `float32` and in [0, 1].
- `torch.bincount` counts how many pictures each class has: the three classes
  are roughly equal.
- The pictures carry a little noise: the shapes are not perfectly flat. Like
  real photographs.

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="349.2pt" height="75.067165pt" viewBox="0 0 349.2 75.067165" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 75.067165 
L 349.2 75.067165 
L 349.2 -0 
L 0 -0 
L 0 75.067165 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g clip-path="url(#p3bab56da4e)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEIAAABCCAYAAADjVADoAAADN0lEQVR4nO2by04qQRCGe8igeBliRMdLCIkaxAAJCxO3vIBvymO4ccPWKDHoAgMKGFS8K2NOTiXH+qetxnBcWd/uNzPY+VNTU11d4xljIvOJpaWlz9L0ej2mk8kk07Z72u22kfB9n+mpqSmmHx4eYvesr68z3e12mX59fRX/J67x8fGR6YR49y9CjSDUCMLDHPE/SCS4v6PRiOlsNst0FLmXcHFxwXQQBEzf3d2ZSdCIINQIQo0g/EqlYj5zfn7O9O3trfN5npmZEd/RyPPzM9Pv7+9MX19fGxeunLCwsMD0zs4O0/V6nWmNCEKNINSIr+oIz/vzp39sbW0xPRwODdLpdMx3uLq6Ep/3ubk5Z21yc3PD9PT0tLh/WV1dZXp+fp7//lgr/wWoEYQaQagRhL+7u2ukQuP09NS4SKVSTD89PYnX7+3tMV2r1Zje2NiI3YNJHAs7XEO1WhXXgElfI4JQIwg1YtzGTMLRZBmHMAzFggqLo3Q6HfsNzFWYh7A5u7a2Jq4JizaNCEKNINSIcXOEB+/vfD7v3HRhM8cFNk0ODw9j1+DGDJs/29vbE+UpjQhCjSDUCIKfxlrAmt62j3h5eTEShUKB6ZOTE6aPj4+ZPjg4iP3G/v4+029vb0yvrKyIa3IdZmtEEGoEoUYQXhAEkfS+xgPbVqtlJqVcLot5x9YDweGRTCYj1hXYvMWcgXsojQhCjSDUCMJ3Haa2ICdsbm7Grjk7O/vW4MdgMBD3Kri/sQ2PYU7AfgTmBFwTDp9pRBBqBKFGEGoE4ePBSKlUEg98bKfh40zFSQkYi6N+vx+7x3boI03t4CbLhUYEoUYQasRPTt4iOJ2CeWZ2dtY5nf9dsPGCBRTmFI0IQo0g1AjCC8Mwkp5PfH7xSxrbPY1Gw0i4vhKysby8LG7CEGzMYI7A2kcjglAjCDXiqzoil8sZqZlrO+BxTePj1CuCjRn8Osc2WYvNG2zGXl5eiofEmMc0Igg1glAjCM/zvEh6v+LQ1f39vZkUbAA3m00xH9i++nGBX/BgwxjRiCDUCEKN+Ml+RLFYZPro6Ei8HvumePA87nC8xOLiovgloUYEoUYQaoT5ywdsDzAF6fd92gAAAABJRU5ErkJggg==" id="imagef818759302" transform="scale(1 -1) translate(0 -47.52)" x="7.2" y="-20.347165" width="47.52" height="47.52"/>
   </g>
   <g id="text_1">
    <text style="font-size: 9px; font-family:inherit; text-anchor: middle; fill: currentColor" x="31.114286" y="14.038594" transform="rotate(-0 31.114286 14.038594)">triangle</text>
   </g>
  </g>
  <g id="axes_2">
   <g clip-path="url(#p7211bb95a9)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEIAAABCCAYAAADjVADoAAADRklEQVR4nO2cTUt6URDGj3aVa2GmWWHZC6nRJiKI1kHfpA/Xru8QuE5qUxEVCJJaavb+riH/WTjjcW5X2/2f3+6h6z2Xh3HumTljgVAo1DZdfH5+dksTj8eZfn5+Zvrj44PpQCBgJO02W8LMzMwwXa1Wjcbi4iLTqVSq5xr53IVCgWnHcZheXl5mOqg+wX8EjCBgBBFIJpPsCxwOh7ulub6+Nhqu6zL99vZmvJidnWX64eFBvf7p6Un9vO050+k006VSSV0DEUHACAJGEAHXddvaOz8ajTJdq9WMhtwjdJibm1Pf8ZJQKMT0/Pw801dXVz2fyWazTF9cXBg/ICIIGEHACKJTGLTNEOzt7al1QYfHx0emy+Uy07FYjOlkMqmusbOz07PG7u6uWlt47V0QEQSMIGAEASMIJxjkXsgNkUxsXpslW9GVSCTU5k2j0WD65eWF6bW1NabPz8971pD3vLu7U+/5/v7ONCKCgBEEjCCcVqtlumk2m8YPl5eXTG9sbPRcc3JywvTExATTm5ubTH99famNmcnJyZ41vJo7IyMjTI+OjjKNiCBgBAEjCEc2a1siZ0QiEaZfX1/V75otx0xNTanv8P39fTVnLC0tqTnE1syRBz7j4+NMVyoVphERBIwgYAThfH9/m26k9kLWCTZk/SEPluUhkcwh8vBG/n2QnDA2NsY0IoKAEQSM6JcjwmJfIQdB/gLZA1lYWGD69PRUPbwpFouea3jVHnI/hIggYAQBIwh+CmL85wTZ47QNk62urqrv+MPDQ/XAR+YxWz/CL/JwGxFBwAgCRhAwol+yzGQyanNWJhlZEG1tbclbmnw+r552yw2SXCOXyzF9f39vhkXeAxFBwAgCRvSbmFlfX++W5vj42FdRJidVbBsiucbR0ZEZFrnJkoXd7e2t+nlEBAEjCBgx6FRd2ufU+2/wOkSSyKLN1oiRzVn5yyMJIoKAEQSM6JcjIj6/r7KJYqsDfnONhmz22H4BIA9wvJDDKogIAkYQMOKvpvP/gunpaaZvbm6GvqccTpG1xsrKCtOICAJGEDBi0Byxvb3N9MHBgXqY0+Hs7EztWdiGw7T/DmAblJfD8fV63dcvlBERBIwgYIT5xw/BkBvCZi/UCgAAAABJRU5ErkJggg==" id="image92f69ad436" transform="scale(1 -1) translate(0 -47.52)" x="64.8" y="-20.347165" width="47.52" height="47.52"/>
   </g>
   <g id="text_2">
    <text style="font-size: 9px; font-family:inherit; text-anchor: middle; fill: currentColor" x="88.508571" y="14.038594" transform="rotate(-0 88.508571 14.038594)">square</text>
   </g>
  </g>
  <g id="axes_3">
   <g clip-path="url(#p8660b138fc)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEMAAABCCAYAAAAMlmvWAAADSklEQVR4nO2cWUsjURCFb7dRo0YxrohGQYNREMm7L4I/3D+gD6LgmpjFjRCN+4qJzLxM1emm7jSZp+F8bydJd4dD3fJW3YqBc67jgP7+fqWHhoaUvru7UzqTySj9/PzsLKanpyOvfX5+Kv34+Kh0u91WemZmRumrqyuXlPn5eaXDxHf4j6EZApohSLkYvr+/zRyRy+XMtff+/q707u6u0l9fX5FnYo7odHQqW15eVvr4+Fjp2dlZpS8vLyPPyOfzSlcqFaUZGQKaIaAZgmBtbS2yzzg4OHAWuO9Ip9NK397emvuWj4+PyD17enrMvOVjampK6Uaj4b0mm80qzcgQ0AwBzRAE6XS641t/tVrNdUMYhua+5Bc3NzdmvdNsNs3viPc8Pz+PPOPp6cnMS4wMAc0Q0AwBzRCksKiKK5pKpZLSDw8PSg8ODipdKBTMxDU8POyQarWq9MLCgtLlclnppaUlpVdXV50PbCAhjAwBzRDQDEEQ1xD2sb+/b76POeHw8FDp0dHRyDXYnBkZGfFeYzExMZG46czIENAMAc3oNmc0oHFyf3+v9OTkpNnsiSvUsDmLjZf19XWlV1ZWlN7e3nZJwbzCyBDQDAHN8OWMgYEBs4GLewCsXcbGxpTG+gcPiH5/kSAwv4OP3t5e70EV5pmTkxOlGRkCmiGgGd3uM5DX11ez0YrNXWz+xvUrNjY2XBLwYOvl5cV7DQ+RDLhMBDTDlzNCOPTB4TIcHMG/16enp0qnUilvbYJ7E6wbcC8zPj5u1j9/02fB3iwjQ0AzBDRDQDMEQRiGkQTahoSZFCzE8AQ9rojCgycsvHDi0Dd13Gq1Ip/BzSBO/zEyBDRDQDP+daHmA3PG1taWd9oPcwQe+OD7uP7Pzs5cUhgZApohoBm+XxUgODhyfX1tTt6hxmbv3t6e6xYsJjFH4NRyXGMaJ5cZGQKaIaAZvn1GsVg0a4l6vW7uEbAuwEETPKiOa+j29fWZ90Tw0Ont7c0lhZEhoBkCmpG0NsnC4Ihv/SKbm5tKHx0dRT6DB0vYIF5cXFR6Z2cn0d4ormmMPRNGhoBmCGhGt/2MbMIcgmsTB+/jhvOT/ucFZG5uLvLaxcWFeQ0jQ0AzBDTD/eEHrsQio/u88uwAAAAASUVORK5CYII=" id="image5897a7fbbd" transform="scale(1 -1) translate(0 -47.52)" x="121.68" y="-20.347165" width="48.24" height="47.52"/>
   </g>
   <g id="text_3">
    <text style="font-size: 9px; font-family:inherit; text-anchor: middle; fill: currentColor" x="145.902857" y="14.038594" transform="rotate(-0 145.902857 14.038594)">triangle</text>
   </g>
  </g>
  <g id="axes_4">
   <g clip-path="url(#p3fd12c0457)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEMAAABCCAYAAAAMlmvWAAADaklEQVR4nO2b3UpqURDHl2ZaaVm56QsTMS+CAi8MugiCHiGInqJeoSfqKqLLriIIgiBUDASlSDP7tE+1Mva5OTOzF7PaGZw4zO/uT9vt6s/scdas2R6lVFu5ZHp6Gul8Ps9e393djXSr1VK/Ee+/XsBvQswAiBkAz3dyRjAYRDocDiNdLpdVp/T39yP9+PiIdLvtbtmhUIi9n41EBkDMAIgZAN/s7CzUqlAoIP36+qoog4ODSE9NTSHt9/uRPjs7Y/9Otc39/b3i8HjsdPf1HPL8/Iz0wsKC4xqJDICYARAzOq0zKD6fD+m3tzekDw8PkT46OkL65OTEuP8pFotIp9NppKPRKNJPT09ILy0tKRMSGQAxAyBmAMSMn06gJg4ODpC+vb1lE7AuCdPijzaI6PVra2tIX19fI51IJBzfKZEBEDMAYgbA8bBalmVsgtDnd25uDulAIID0/Pw80js7O2wBZZPJZNgc0Wg0kG42m2yO+MpGUCIDIGYAxAyuzkgmk2yz5zvQOmJrawvph4cHx2dow2hzc5PNQ8vLy0h3dXUh7fV6jQdZEhkAMQMgZnB1RuEHckQkEmF/81dXV5E+Pj523IPuX8bHx5EeGRlBenJykm1Cv7+/G9ctkQEQMwBiBsBHn73Ly0vVKXd3d0gvLi6yzd3t7W3HPejB0vDwMNIrKytIVyoVdk30/9QhkQEQMwBiBrc3CZBeBO0b6BgYGEA6FouxA3D0kFhXA+zu7rK5bH19HelarYY0PVCn/REdEhkAMQMgZgDEDG6j1vhCwuzt7UW6Xq+7Sla0oNIl0L29PaQ3NjaUG+ihkmn6yEYiAyBmAMQMrugKkulfOgGjyxl08o5O1tFDolwuxzZ/ba6urpC+uLhwXMOtm66BopsOlMgAiBkAMcPNsEqITOPrNmb0LYKJiQn276b76d4qOD8/V26gh0YfHx/sGv98xtU3/OeIGQAxA+CxLKvNPVs3NzfK9JtO306kDWFTDtHtE+g9xsbGXNUdtBZ6eXlRJiQyAGIGQMxwU2dEybS+TbVaRXpoaAjpnp4edphsZmYG6f39fWUatKN7lVQqxfYvstms457cmm0kMgBiBkDMAHji8TjKGaVSSblldHRUcQdRp6enSPf19bE5RlfffKducPu2o0QGQMwAiBnqL5+GtyVkCyrH+AAAAABJRU5ErkJggg==" id="image6119a46262" transform="scale(1 -1) translate(0 -47.52)" x="179.28" y="-20.347165" width="48.24" height="47.52"/>
   </g>
   <g id="text_4">
    <text style="font-size: 9px; font-family:inherit; text-anchor: middle; fill: currentColor" x="203.297143" y="14.038594" transform="rotate(-0 203.297143 14.038594)">triangle</text>
   </g>
  </g>
  <g id="axes_5">
   <g clip-path="url(#pc4722374b4)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEIAAABCCAYAAADjVADoAAADaUlEQVR4nO2bSU/jQBCF28SQYEQgbAEEIhKJCBzghPgBSIgT/xeO3JEQm1gFCkJhXxL2zSM0dXA9e9oxg+Ywet/tRW0neaouV1e3nXQ67ZsAmUwmKM3d3Z351zQ1NSnd2toaGvPw8JDont3d3Ur39/fr70x0t/8YGiHQCMExxqgckUqlgtKUSiWlt7e3lW5ubjbI29ubSUKxWLTO39XV1dA19/f3Snd1dSl9fX2tdE9Pj9L1el1pRoRAIwQa8acckfQZ//n5GXvNzc2N0p2dndbxWLt0dHSExhweHird1tamdF9fn9Lr6+tKT05OKs2IEGiEQCMEd2RkxAR5fX1V+vz8XOmPj4/Y+X57e6v08vKy0gsLC8YG5oS9vb3QGKxv4sD/iTAiBBoh0AiBRghONptVBVWtVrMmLt/X9ReOj+L9/V3parVqXchNTU0p3dvbG/sdS0tLSs/NzSm9tbWl9OzsrNKMCIFGCDRCcDzPU5N+fHw8KM3Kyoqxkc/nQ5+dnZ1ZNS6IsGiLK+K+mJiYsOauzc1NpT3PU3p6elppRoRAIwQaIbiPj48myMbGhnU+Y9O0kToC6wacr/gbMCc4zlf/SHNxcaH0wcGB0u3t7daF4NPTk9KMCIFGCDRCcHAT2IfnMTZqcDMG5/sXa2trSl9eXiq9v7+v9MzMjPlpdnZ2lB4bG7PmHUaEQCMEGiG4Ly8vJkhLS4uxcXR0pHQulzNJD2ngMx85Pj5Wenh4ODQG64DFxUVrT+P5+dmaMxgRAo0QaMR3N4HL5bK13xi1mYJ5JQ5cF0T1I9LptLEdcLm6ulI6m81aaxdGhEAjBBoh0AjBGR0d9ZMUO3h6zXXd0BhciO3u7ip9enpqXQANDQ2ZpGBCxeSJ4GlARoRAIwQaIbhxJ9wQbN5G5QjcoBkcHLQ2ahC8Z9SpOiyY8K0CXGTNz89bN6YZEQKNEGhEo4uuIjRrcW5izmik1sB74Hz+DlgXDAwMKF2pVKzXMyIEGiHQCMEpFAr+3zRRsEES9VYeNkVwbYGbSphT8G2cqOYNEldX4AEXRoRAIwQaIbhJc4IXc8gjan5ijsDDKD9BoVBQ+uTkxDoeN7YYEQKNEGiE4OTzed9WF+AzHjeJ43qcUYfK8SAYrhOSvkncCHgoDnuajAiBRgg0wvzmF5WmIzbdZmFqAAAAAElFTkSuQmCC" id="image202b242d3b" transform="scale(1 -1) translate(0 -47.52)" x="236.88" y="-20.347165" width="47.52" height="47.52"/>
   </g>
   <g id="text_5">
    <text style="font-size: 9px; font-family:inherit; text-anchor: middle; fill: currentColor" x="260.691429" y="14.038594" transform="rotate(-0 260.691429 14.038594)">square</text>
   </g>
  </g>
  <g id="axes_6">
   <g clip-path="url(#p9fcacd81b7)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEIAAABCCAYAAADjVADoAAADe0lEQVR4nO2cu0srURDGz2o0Mb7iYwOKaBAJmiaCSMBCEFvBLr3/gIX4z9ha2djZ2dmJD1AiSAqjwRcY3++gRsKdwm92nXVvrrfQ+XUf2T27+2XO5Jw5Z2MZY0rGB83NzaBLJTz95ubG+KW+vh70/f096J6eHtAHBweebYZCIdCtra2gLy4uQFd9+W5/OGoEoUYQlm3b0MnPzs4+StPe3g66UCiY76aqCr+ft7c30A0NDaDv7u4qv2bFLfwQ1AhCjSAsv+MITjgcBv3w8GC8CAaDoF9eXkC/vr6aSunu7gadz+dBx+Nx0BoRhBpBqBFfzRGLi4ugbdsWf8MHBwdBb21tOdrkcwfef+vq6kCvra2Bnp2dNZUSjUZBa0QQagShRhBqBGGFQiFIlk9PT0Zibm5OTHyRSAR0JpNxtMGP6e3tBb2zswN6ampKHIB9hVQqBXp1dRW0RgShRhBqBBHgOaGmpkYceOzt7YlFlFwuJxZVylxeXoLe2NgQJ0w8J1RXV4uTOLfJ3/r6OuhEIoHP4Wjhl6JGEGrEvyrMLCwsiAsrvD+X2d/fB51MJkGPjo6K1+TjDp633Ojq6gJ9eHgIWiOCUCMINYIIGIbNCi98wYcXTQYGBkBfX1+Dvrq64pcw6XQadDabNRJtbW2gT09PjReWVU5/n+cEjkYEoUYQagRhxWIxsR7B+yPve3yjyPz8POixsTHD2dzcBD05OWn85Ai+AOSWh/yiEUGoEYQaQQT4uL+lpcVI8JzAub29Bb2ysuI4Znh42PiB3xOvefT39zvO4c/lVYvViCDUCEKNINQIwpqYmIDst7S09FGazs5OsfD6+PgIuq+vD/T09LThzMzMiIUWr0kYL/a47bDhCXR3dxe0roZ/gnYNQo0gAjwncI6Pj42f/npycgK6WCw6zuHFWl784ZOs8/NzMSc0NTU5rsF34XB4GxoRhBpBqBGElUgkSlLfisViYqGGvxnDxwD88zJDQ0Ogl5eXxUXgxsZGcdLFC8pu5/BJGN8xrBFBqBGEGkFYwWAQcsTz87M41+ALOtvb2+KY4H/Axx1uYw8vNCIINYJQIz7bKFJbW+s5V/CzaYP/nrsVeL8jR/hdBNKIINQIQo0gAvxtt6xHvXB8fBz00dGReDyvaf7Nm79e/y7g9g8FHR0d4jEjIyN4D553+UtQIwg1wvzhHbKTJPif3l5lAAAAAElFTkSuQmCC" id="image0a78947179" transform="scale(1 -1) translate(0 -47.52)" x="294.48" y="-20.347165" width="47.52" height="47.52"/>
   </g>
   <g id="text_6">
    <text style="font-size: 9px; font-family:inherit; text-anchor: middle; fill: currentColor" x="318.085714" y="14.038594" transform="rotate(-0 318.085714 14.038594)">triangle</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p3bab56da4e">
   <rect x="7.2" y="20.038594" width="47.828571" height="47.828571"/>
  </clipPath>
  <clipPath id="p7211bb95a9">
   <rect x="64.594286" y="20.038594" width="47.828571" height="47.828571"/>
  </clipPath>
  <clipPath id="p8660b138fc">
   <rect x="121.988571" y="20.038594" width="47.828571" height="47.828571"/>
  </clipPath>
  <clipPath id="p3fd12c0457">
   <rect x="179.382857" y="20.038594" width="47.828571" height="47.828571"/>
  </clipPath>
  <clipPath id="pc4722374b4">
   <rect x="236.777143" y="20.038594" width="47.828571" height="47.828571"/>
  </clipPath>
  <clipPath id="p9fcacd81b7">
   <rect x="294.171429" y="20.038594" width="47.828571" height="47.828571"/>
  </clipPath>
 </defs>
</svg>
<figcaption>The first six pictures of <code>make_shapes</code>: 16 × 16 pixels, a little noisy.</figcaption>
</figure>

## Normalising

Networks learn more easily when the input has a mean around 0 and a standard
deviation around 1. For this, the training data's mean is subtracted from each
channel and the result divided by its standard deviation:
`(x − mean) / std`. This is called **normalisation**.

```python
from torchvision.transforms import v2

mean = x.mean().item()
std = x.std().item()
normalize = v2.Normalize([mean], [std])
z = normalize(x)
print(abs(z.mean().item()) < 1e-5, round(z.std().item(), 3))
print(x.mean(dim=(0, 2, 3)).shape)
```

```text
True 1.0
torch.Size([1])
```

- After normalisation the mean dropped to zero and the standard deviation
  became one.
- `x.mean(dim=(0, 2, 3))` averages over the image, row and column dimensions;
  one number per channel is left. A colour picture would give three.
- The mean and standard deviation are computed **from the training data
  only**, and the same numbers are applied to validation and test data. Numbers
  like `[0.485, 0.456, 0.406]`, often seen with pretrained models, are the
  channel means of the dataset that model was trained on.

## Why not treat a picture as a flat list?

In the machine learning modules each example was a list of numbers. We could
turn a picture into a list of 256 numbers with `flatten` and give it to the
same models. But then the **neighbourhood** between pixels is lost. Let us move
a shape just three pixels to the right:

```python
import torch.nn.functional as F

img = x[0, 0]
moved = torch.roll(img, shifts=3, dims=1)
same = F.cosine_similarity(img.flatten(), img.flatten(), dim=0)
shifted = F.cosine_similarity(img.flatten(), moved.flatten(), dim=0)
print(round(same.item(), 2), round(shifted.item(), 2))
```

```text
1.0 0.38
```

`cosine_similarity` measures how much two lists point in the same direction:
1 means the same, 0 unrelated. To the eye it is the same shape; seen as a flat
list the similarity drops sharply, because the numbers at the same positions
now belong to different pixels. In the next section we meet the operation that
solves this, **convolution**: an operation that looks for the same small
pattern everywhere in the picture.

## Summary

- A grey image is `(H, W)`, a colour image `(C, H, W)`, a batch `(N, C, H, W)`.
- Pillow says `(width, height)`, NumPy `(H, W, C)`, PyTorch `(C, H, W)`.
- Pixels in files are `uint8` (0–255); before the network, `float32` in [0, 1].
- The normalisation mean and standard deviation come from the training data.
