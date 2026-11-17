# Feature Extraction and Image Similarity

In transfer learning we saw that the network's body turns a picture into a
**feature vector** of 64 numbers. This vector has another use: **comparing**
pictures. If similar pictures get vectors that lie close together, jobs such
as "find the pictures most like this one" (image search) or "which group is
this picture close to" (nearest-neighbour classification) can be done without
a classification head. These vectors are also called **embeddings**; it is the
picture counterpart of the idea you saw for words in the Embeddings and
Language Models module.

## Extracting the embeddings

We train the body from the previous section on shape pictures and extract the
embeddings of 300 new pictures as a gallery. An embedding is the output of the
trained model's body (`model[0]`).

```python
import torch
import torch.nn.functional as F
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from dl_data import make_shapes

x_train, y_train = map(torch.from_numpy, make_shapes(600, seed=1))
gallery, labels = map(torch.from_numpy, make_shapes(300, seed=2))

torch.manual_seed(0)
model = nn.Sequential(
    nn.Sequential(
        nn.Conv2d(1, 16, 3, padding=1), nn.BatchNorm2d(16), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(16, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(),
        nn.AdaptiveAvgPool2d(1), nn.Flatten(),
    ),
    nn.Linear(64, 3),
)
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
loader = DataLoader(TensorDataset(x_train, y_train), batch_size=32, shuffle=True,
                    generator=torch.Generator().manual_seed(0))
for epoch in range(5):
    model.train()
    for xb, yb in loader:
        optimizer.zero_grad()
        F.cross_entropy(model(xb), yb).backward()
        optimizer.step()


def embed(images):
    model.eval()
    with torch.no_grad():
        return model[0](images)


vectors = embed(gallery)
print(vectors.shape)
```

```text
torch.Size([300, 64])
```

Each picture is a vector of 64 numbers. The numbers mean nothing one by one;
what is meaningful is the vectors' **direction** relative to each other.

## Cosine similarity

**Cosine similarity** measures how much two vectors point in the same
direction: 1 the same direction, 0 unrelated. If we first normalise the
vectors to length 1 (`F.normalize`), the cosine similarity of all pairs is a
single matrix product.

```python
unit = F.normalize(vectors, dim=1)
similarity = unit @ unit.T
print(similarity.shape)
print(torch.allclose(similarity.diag(), torch.ones(300), atol=1e-5))

query = 0
scores = similarity[query].clone()
scores[query] = -1
nearest = scores.topk(5).indices
print(labels[query].item(), labels[nearest].tolist())
```

```text
torch.Size([300, 300])
True
2 [2, 2, 2, 2, 2]
```

- The diagonal is 1: each picture is perfectly similar to itself.
- For the first picture, all five most similar pictures (excluding itself)
  are of the same class. The network gained this without any "search"
  training, just while learning to classify.

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="371.52pt" height="150.071268pt" viewBox="0 0 371.52 150.071268" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 150.071268 
L 371.52 150.071268 
L 371.52 0 
L 0 0 
L 0 150.071268 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g clip-path="url(#p23fb7d2a4d)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEcAAABHCAYAAABVsFofAAAD40lEQVR4nO2cuU4rQRBFZ8wIAzb7KhaDkAUJIEQGQiIlI+AL+AwSPoMPICIiI0SARA4IEbALI/Z9B7P4abJXy7s99iOjTnZH1fboqqfU3VUzfktLS877i4eHB4/T3t5O9O7uroh5e3vz/peOjg5x7enpieirqysR09PTQ/T29raIyWazRJeWlhL9+voqxsQi3POvxcwBmDmA4Pj4mFwoKipyPvdvSn4pLy8n+vHx0csXLd/d3Nw4x2UyGaK7urpEzN7eHtHf39/O37WZAzBzAGYOwMwB+PF4nCwC39/fZZDvEz03Nydiqqurib6/vxcxdXV1RDc2NhK9tLQkxgwNDRE9Pz8vYj4/P4menJz0XCQSCaKfn59FjM0cgJkDMHMAgZZjOK2trXDBF9LU1ER0WVmZiEmlUkS/vLzAHBRye3tL9NjYmIhZWVkhOp1Oi5iPjw+4EbWckyf2WAHMHICZA/BTqVQO7XBDYjHqYWVlpceZmZmBu2DtpK+zs5Poi4sLMSYejxN9cHAgYiYmJpz3x3f3/f39RK+trYkxNnMAZg7AzAEE2mk+p6SkBC6gNCoqKsS16+trog8PD4keHBwUY3p7e4leXV11/neUSsjm5qYzxmYOwMwBmDkAPxaLkXVOEAQiKBshx3DW19fFtfr6eqJPT0+dFYH9/X2ip6amnJtKPiYK2mbVZg7AzAGYOQAzBxBE2fxlWUKura11VihmZ2dFzMDAANxU7uzsiDENDQ1Eb21tiZhkMgl/N2R4eJjohYUForUTUZs5ADMHYOYA/EQikXOdwv8U09PT8FCKb3BDxsfHYW7TWk74BjeEb7BramqcrS42cwBmDsDMAZg5gKCQBFyrLAJ5EqyqqhIxvETMy8pRTvD6+vrEtZOTE6KjnG5G6TW0mQMwcwBmDiBcUZFF4OjoqPP5zChV0bOzM2fOubu7I3p5eZnokZERrxB47lLbSVjVlrfpXV5eyjEF3c0vwcwBmDkAMwcQ8JeyFhcXRdA7OyXjvX0h/ERRK4/wnmKtVcSFluh5SUcr8fBr2mkhx2YOwMwBmDkAP51O51wvtybZ6T5/OU3rIT4/P3e2vfFycJSeaA3+u0dHR86ck8vl4MlgiM0cgJkDMHPy2XjyDZr2vHZ3d3scvnHTDpN4Kxx/4VVbe/C1kFaRdf2P1mKysbEB21hCbOYAzByAmQMwc/JJyPylMm1xpi0CeULTkisv5fJqQ3NzsxjDv2ygfemAf0Xh6+tLxLS1tcGvnmgVC5s5ADMHYObkk3O0F1df2IuqhVJcXAyrBlqu4BWLn4JXbbW2FZs5ADMHYOYAzBzv3/wB2o9X7SdziGEAAAAASUVORK5CYII=" id="image16a3d20a7f" transform="scale(1 -1) translate(0 -51.12)" x="7.2" y="-19.031268" width="51.12" height="51.12"/>
   </g>
   <g id="text_1">
    <text style="font-size: 8px; font-family:inherit; text-anchor: middle; fill: currentColor" x="32.708571" y="13.278125" transform="rotate(-0 32.708571 13.278125)">query</text>
   </g>
  </g>
  <g id="axes_2">
   <g clip-path="url(#p4b451868a5)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEcAAABHCAYAAABVsFofAAADhUlEQVR4nO2cyUorURCGT2s7JCqJJnEkIiLY4M4BxJUbn8G9b+Oz+BwuXTkQN86ixBmHGKdIVpdTVfc/HfEuLvzfrg51mvRPpVLdVSeRc67hWmRgYECttbW1efbX15fyeX9/9+y+vj7PrtVqas/d3Z37F0xMTHj2ycmJ8vHviHhQHADFAcRyobOzUzl1dHQE88nt7a1rNVfJHDQ0NPQrOWdubk6tbW1tefbr62vwnhg5AIoDoDgAigOIxsbGvCKwXq8rp8fHRxfykVxfX6s1WeQdHBx49uzsrNoji7M0heLa2pryubm58eyXlxcXgpEDoDgAigOIz8/PvYX+/n7lVE+RYySHh4dqLZfLeXaxWPTso6Mjtefs7Axeo0lPT08wn8SxqneDMHIAFAdAcQAUBxD95E3gT9nb2/Psz89P+GbQSq7d3d3KZ3JyEtpWwZkGRg6A4gAoDiAOvfWziqz7+3sXYmlpSa3l83nPfnp68uxGQ6e/bDYLP4vFT4pWWZA2YeQAKA6A4gCiYrHYCH2nj4+PXYjx8XHPfn5+Dr5w2tjY8OyFhQW1R9Y+hUJB+fT29sI81aRarbpWYeQAKA6A4gAoDiDKZrNeQm5vb1dOBZEEkyRRPpubm7BjYbG9vQ1btE1mZmaCyTZNIStbzxLrh4iRA6A4AIoDiEqlkpdzrq6ulFMickylUgnmht3dXdfq6Nn6+rryWV1d9ezBwcFggWcVirIALZfLnv329qb2MHIAFAdAcQAUBxDLBDw8PBwcA8mLN3pWAh4ZGQl2EuST/Pz8vAthdRZkQpbJ1+panJ6eevbi4qLaw8gBUBwAxQFESZI0QvPEVfGdtuaFo6jZPP3D5eWl8lleXoYPnlauSIPMQ1Z3s6urC84dj46Oqj2MHADFAVAcAMVpZQQlk8kop5qY/bXm6z4+Pjx7enpa+ezv78NiMk2b2aJUKgV95IEX+SNjfV5GDoDiACgOIMrlcsGxt4eHh+DDn3yotNrBsiOxsrLi2Ts7O2rPxcWFaxX5htG6jsyRVseCkQOgOACK00qdY3UzK0a34X9DdiTkQ+7U1JTaw8gBUBwAxQFQHEAsD3fJ4sjCejiVIxzWAViJ7DbIsxFpD6qmwfqnhVDRysgBUBwAxQFE5XK5ERo9y4gcY+WT38gNVl6QoyHWeSs50ibPcVn3IK9r7WHkACgOgOIAKI77O99huS7CyDK8ygAAAABJRU5ErkJggg==" id="imageb6333fc845" transform="scale(1 -1) translate(0 -51.12)" x="68.4" y="-19.031268" width="51.12" height="51.12"/>
   </g>
  </g>
  <g id="axes_3">
   <g clip-path="url(#p1f9679403c)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEcAAABHCAYAAABVsFofAAADlklEQVR4nO2cSy8sURSFT+lu2rPRCEIMiESTIMRUhJ/BzE/yU5iZiRkSBgbilXjE+/1+9U1Nbuy9z111q/Qd3fXNVmWf6rZyavc+5+wSOOeK7htlZWVO8/X15UpBb2+v0AcHB0I/Pz+bMdXV1UI/Pj6amKamJqEvLi5cKbBOkN/QHADNAQSFQkHknM3NTVcKampqzLWHh4fY9xkcHBR6fX3dxKRSKaE/Pz9jf05PT4+5xpkDoDkAmgOgOYBAF4G+RPr6+ir02tqaidnf3xd6ZGTExKysrAhdUVEh9NDQkBmztbUVmdRnZ2eFPjo6MjG5XE7o29tbFwVnDoDmAGhOnJyTlIWFBaHf3t5MzP39vdCXl5dCd3R0mDGFQkHoTCZjYkZHR4UOgvDPkugF9fX1tYkxYyIj/mNoDoDmAGgOIN3d3S0u7OzsuCS0trbCojBkbGwM3mN3dzf2bmLSAi+fz7uoHVDOHADNAdAcQDppjtFMTU0JPTc3Z2Le39+FPjw8jFxU1tXVuSiS7PzpAtQHZw6A5gBoDiBdXl4euWhra2sT+unpycScnZ0JXVVVZWIWFxeFHh4eFrq9vd2M6e/vF7q5udnEnJ+fu5+ia6UQzhwAzQHQHADNAQT5fL4YtzjyoRewvp22+fl5oevr64U+PT01Y6anp2FLSsjx8XFkMVlbWwvvc3JyYsZw5gBoDoDmxCkCKysrTdCzakcbGBgwMTpfXF1dmRidC3S72sTEhCtFa0tDQ4OJ0TlQn4T44MwB0BwAzQHQnJ8eB6cS9NzpZOvrD15aWhJ6ZmYmMtGn02kTo4+edctMSGNjY+QPhoYzB0BzADQnTs7RRaHvmfbtFupxfX19JmZ7exu2vfneffDtOmr0DqLv3QdfS8x3WlpazDXOHADNAdAcAM35aRGYVoXXx8eHidErYd9O4OTkpNCrq6tC39zcuFKgj3NC9vb2YKJnC0pM+FgBaE6p+5BTaiHqe2Z1u4kP3V5yd3cXOUYXjiGdnZ2wtcWXN/Xuoa/45cwB0BwAzQEE2WxW5JyXl5d/8oJp0pZYTTabNdf0d/adPuh8pnOXb4HLmQOgOQCaA6A5gCCXyxWjCrFiMf77an9zJKsLM90m4jv+1f855W+L1CQ/Ipw5AJoDoDmAIJPJFOMuGHOent2uri6hNzY2XFx87znoHOj7bF1Mjo+Pm5jl5WW4YaffFwvhzAHQHADNAdAc92d+Ae77H6EDxQFYAAAAAElFTkSuQmCC" id="image8c4b4dad2f" transform="scale(1 -1) translate(0 -51.12)" x="129.6" y="-19.031268" width="51.12" height="51.12"/>
   </g>
  </g>
  <g id="axes_4">
   <g clip-path="url(#p204268f881)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEcAAABHCAYAAABVsFofAAADjklEQVR4nO2cyy5sQRSGa7PRodEhEeKadg0GZoyEGWMDD+CpeAdPYOIRCBEDpAmihXa/0056uNaq81fvzZmc/N9sVapq7/579eqqvVbtyDn37RTd3d3CLpVKwn55eXEhmpubTdvX15ewn5+f3b+goaHBtPX09Aj78PAwOE/Nr97VfwbFAVAcQJTNZk3MeXx8FHZLS0vwN93Y2Cjs09PTYMzxMTk5Kezd3d3gmPr6emG/v7+734CeA6A4AIoDoDiA+OPjwzQODAwIu1AouKS0traatru7u+A4veCsBh2As9msC/3J+Ojt7RU2PQdAcQAUBxDFcWwWgZ+fn2iMi+PYJR3jWzy+vb2ZPnV1dcIul8vBhWR7e7uwr6+vXRr0tek5AIoDoDgAigOI8vm8CchXV1dwQXd7e2smWllZEfb8/Lzpk8lkhJ3L5Uyf8/NzuMCbnZ01Y/L5PLxOhZubGxjEfYGcngOgOACKA4h82YeOjg6YbXh4eDAT7e3tCbtYLJo+TU1Nwq6trTV91tbWhL2wsBCMFb44FKKtrS246aXnACgOgOIkjTmaoaGh4Mbz/v5e2Jubm6bP+vp6cOOp1yiLi4vCXlpaMmMODg6EXVNjv3O9ga0Geg6A4gAoDoDiAOLR0VHTeHx8DAOeb2OnS07Ozs5Mn+np6WCqd3h4GPbR91Khq6sr+CRQZ1m+v+3/0MzMjLDpOQCKA6A4SUtQ9EOozs5OYW9vb5uJfJlTzerqanDjOTIyAjeVOkNQob+/PxiX0kDPAVAcAMUBUBxA7CvN0G0l9YSsmuA7MTFh2p6enoTd19dn+uzs7MB5fdc+OTlxSfE9UdQZCnoOgOIAKE7SEhR9TqCQouzNd/ZBZy02NjZMn+Xl5R+XwfkYGxsT9v7+fnAMPQdAcQAUB0BxADbH4py7vLxMfPBCp1erCaQXFxemLTRufHzctOn78e3KqwnAGnoOgOIAKA4gyuVyZhGoS07KKpU6ODgY/E2nPfvwG+j0tS8O+T6DPhRLzwFQHADF+WkJytzcXLC8RK+F9Oa1wtHRUehSwXl1JsT3sEsf2K0QRZWPmiz+0XMAFAdAcQAUBxBlMplgHXJZLQJ9bxsIvaEg7VtPdP1hNYfefOiA7CtB0Yfl6DkAigOgOID49fXVNOr64KI6x6AXZr5ykrRvVdKZSJ2FTIuOMVNTU6bP1taWsOk5AIoDoDgAiuP+zh9lvS8xAR9BAQAAAABJRU5ErkJggg==" id="image3b07a9dce9" transform="scale(1 -1) translate(0 -51.12)" x="190.8" y="-19.031268" width="51.12" height="51.12"/>
   </g>
  </g>
  <g id="axes_5">
   <g clip-path="url(#pd8c9d885a5)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEcAAABHCAYAAABVsFofAAADhElEQVR4nO2cuU4rQRBFe7AxoGGx2RGLEJhFBJCA+ATI+Q6+jIQIckRCyCqEMCCZAMQmVrHKTw6rurk1w/N7Cfdkd1Q9tq/a5erqaUfOuYpTdHV1CX11dSV0Q0ODHuLe3t6cRWtrq9APDw/mmEwmI/TX15c5Jp/Pe9eGhoaE3tnZMe9TZ0b8YmgOgOYAolDOsb7DdXW+pzoPXVxceDGVivlS/41isehdOz4+FpozB0BzADQHQHMA2dDFmZkZobe3t4VuaWnxxjQ1NQkdx7EXMzc3J/T9/b0Xs7u7K/To6KjQh4eHziKKqr8zkomJCaFLpZIXMzw8LDRnDoDmAGhO2pyjc4zm8fHRWTw9PXnXNjY2Ui8ic7lc6oLu9PTUi5menhb65ubGizk7OxOaMwdAcwA0B0Bz0iZkXUStra0Jvbi46I1ZWVkRur+/3+wWbm5umolzeXnZWejVtO4ehjp/ursZgjMHQHMANAcQxXHstef0wnJ9fR0WS1VmZ2edxefnp9BtbW1ezMfHh9A9PT3mfcfHx4U+OjpytYAzB0BzADQHEEVRVLF2CTKqblhdXfVuNDY2JnQ265dQl5eXZsz8/Lz7F3R2dsLGVqjRxpkDoDkAmgOgOYBski3agYEB+ChJlf39fXPLuLm5WejJyUkvRo/Ti+BQ91An29CuxvX1tdCvr6/mwpgzB0BzADQHEC0sLHhJ5/z8HO4yhr73W1tbZsNJLyIHBwe9GF2chRa5FqGcqK/pzxiCMwdAcwA0B0BzAFEul6tYHbuKKhRDhePd3Z3QJycn5tbu0tKSF1OrLp5GF5zlctmL0YUhZw6A5gBoDiD7/v7uavEMb6FQMBd/3d3dqc9LTE1NCX1wcPCj96cLWf1+qzw/PwvNmQOgOQCaA6A5aR9B0Z2/vDoYsre3ZxZ4ocNeSRKwJkkC7u3thY+khAh1Kr0YM+IXQ3MANCftYTR9sKygCqbQQbPGxkazu58E3bHTZypub2+9MfX19UK/vLyYr6PfbxUuPFPArxWA5gCyukYInW2I1dmpvr4+b0xooWkRegRFH8TXj+CF6hOdY/QB+9CO58jIiBej6zfOHADNAdAcAM1JWwS2t7ebhddP6OjoMA+E6UWufi5Zd+uSon9UktyHMwdAcwA052//BSUJoX9jsnYfQgWdXtTqBpnOW9/lrlrAmQOgOQCaA6A57nv+AKI9D/+Tmk+jAAAAAElFTkSuQmCC" id="image72edd727ad" transform="scale(1 -1) translate(0 -51.12)" x="252" y="-19.031268" width="51.12" height="51.12"/>
   </g>
  </g>
  <g id="axes_6">
   <g clip-path="url(#p769867c588)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEcAAABHCAYAAABVsFofAAADyUlEQVR4nO2cuUpsQRCGe+S44D7u476CYKCBjAZiIKIPoZngw/gcRiYK4guIkRq44hgIbriPKy64MHJucC9V1VafHm7m/2V/U308/LR1eqmemDEmYxzk5eUR/f7+7upihoeHRdvy8jLRBQUFIubt7Y3oyspKoktKSkSfp6cnotPptIgZGhoiemVlxbjIcUb8YmCOAsxRiNlyTnd3N9GpVMq4aG9vJ/ry8tKZu+7u7pzPbW1tJfr6+tr53NHRURGztLRE9MfHh4hpamoiGiNHAeYowBwFmOObkHNyqGe1tbVEn5+fG99EGnJ1dUX0y8uL8YW/iy358w9K1I8KByNHAeYowByFWDKZFDlndXWV6IaGBqKLi4vFg46Pj4l+fX0VMfn5+Wpu+/NCsTAN/iM3N5foTEauk5ubm4k+ODgQMV9fX87Fs3g/EQH+AnMUYI4CzPGdBPLdt7RlZ43DV9hbW1sihrclk0kRs7+/T/TNzQ3RdXV1og//QDQ2NoqYsbEx9bkhPT09RGPkKMAcBZijENgaXTkmxiZqITs7O+quWsjz8zPRc3NzImZ6elqdkFZXV4s+a2trzl0+PpG15Zzd3V2iMXIUYI4CzPGd5yQSCe/NLc7MzIxoq6mpcS4iBwYGiD47OyO6rKxM9Hl4eHCePnCCQKbbz89PojFyFGCOAsxRgDm+k8BsEnBVVRXRvb29Iobv/Nl2Are3t4mOx+NE7+3tOReMUbDtZt7f39P3837qLwLmKMAchaC0tFQ0Pj4+an2s5WqFhYVEj4+Pi5iFhQXn3ykvL1c3v/gENWRkZMT4YiufGxwcJBojRwHmKMAcBZijENjKQFpaWog+OjpSa4Vtx8G2hMf72U4S+AlFW1sb0V1dXc5VuY3+/n6i19fXRczp6SnRGDkKMEcB5ijE4vF4xlValopQMsYnhra8xJmfn3eWk2xsbBA9NTVlsoGXl9hKUPjOJEaOAsxRgDkKMEchsF3OiHLZjMMTcF9fn4jhydW2uudHsnyXj9cI2kpmLi4unMdCJycnxgVGjgLMUYA5vsfBLhKW3Tg+yTo8PDTZsLi4SPTExIRz95CXu0TJJ52dnaKtqKiIaIwcBZijAHMUgvr6etHIyz6ibC7xuwXZwuc+rpMQ26X7KNjKXzY3N4nGyFGAOQowRwHm+E4CKyoqiL69vVWPbG3lG1Hg5SUhfCHMY6L8isHk5KRom52ddfbjF2cxchRgjgLM+d8LTxsdHR3qCehPdxJ8F7k8/9l+BYXfsQjhpTa2HImFpwf4t1KAOQowx/zMN/7VLdi+NB2dAAAAAElFTkSuQmCC" id="imagebb9fb87cd4" transform="scale(1 -1) translate(0 -51.12)" x="313.2" y="-19.031268" width="51.12" height="51.12"/>
   </g>
  </g>
  <g id="axes_7">
   <g clip-path="url(#pad021ee2a2)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEcAAABHCAYAAABVsFofAAADk0lEQVR4nO2cyy5sURCG126t3W8dESHul7QgBiZmjIxEDDDxPl7BK5hJSBh5AIkpIUHcIiGIS1w6Ln3Ss7Oqlr/2Psc5E/83q5Vae7c/pVStVS1yzhXcb5SVlTlJRUWFZ9/d3TmLKIrUWqHgvcqVlJR4dmVlpdrz+PjokjI0NKTWrq6uoB0ilfjNPwiKA6A4gGJi8BNBDNLptFp7f38399XV1Xn2/f29Z2ezWbWntrbWs4+Pj833lJaWqrWGhgaYc2T+K8LIAVAcAMUBUBxAlMlkClaylTw/P6u1kZERz97d3VU+AwMDnt3a2urZGxsbzqKpqUmtxSnoJIODg569s7OjfBg5AIoDoDhJisBQzhkfH/fszc1N9y/I5XJq7fDw0LPf3t7M54Qa2Dh5U8LIAVAcAMUBUJy/7co7OjrMrvfg4AB200UeHh5cUnp7e+F74ib2vb09z66vrzdPFRg5AIoDoDiAKJfLeTnn4uLCzBXd3d3KR+ah/f195SMLzMXFRfO58t2h08KZmRmXlOrqas/O5/PKh5EDoDgAigOgOEmKwNAVxcfHh9n1xulyl5eX4XNPTk7Unra2NjMht7e3e/bw8LD5WWSRKq+qizByABQHQHEA6fLycjOfRGKc5Obmxlmsr6+btwRy3CV0ytfY2OjZ5+fnZqG4tramfObm5mDByduHhPDXCkBxAGn59/3p6Uk55UVTJmuPUJ0TamCrqqocqqnGxsbUntfXV3PkbmJiwrNPT0+VT3NzM3xOKN8xcgAUB0BxABQHkJZJMpVKmQn59vZW+chELmeXQzOAo6Oj5ryfvBWoqalRPrKQlT/TV8+2YOQAKA6A4iQpAq+vr51FaeDGU7KwsKDWVlZWYOG4vb2t9nR1dZk3FFtbW4m/L9HT0wNHXYowcgAUB0BxABQHkI4zd5zJZBIn5BDylPHl5cWzp6amzGvbYPcsCtfZ2Vnzs4QSsHqu6fGDoTgAigOIstlswWoqrS+VhU7sQiMdshldWlry7L6+PrPxvLy8VD7z8/Oe3d/fr3zkuJzMb6urq2oPIwdAcQAUB0Bxvvvbwf+TP5lD/i4YOQCKA6A4SXKOPMkPFXjT09NOIouoOONzks7OTvPWIHQSKJvRs7Mz5dPS0gKvqycnJ9UeRg6A4gAoTpKcE/qeVCTG3uTNZejA6fPz0yUllE+Ojo7gwVvoXXH+I0scGDkAigOgOACK477mF0zoINwKcmOMAAAAAElFTkSuQmCC" id="image7e0d4e00cc" transform="scale(1 -1) translate(0 -51.12)" x="7.2" y="-91.751268" width="51.12" height="51.12"/>
   </g>
   <g id="text_2">
    <text style="font-size: 8px; font-family:inherit; text-anchor: middle; fill: currentColor" x="32.708571" y="85.854125" transform="rotate(-0 32.708571 85.854125)">query</text>
   </g>
  </g>
  <g id="axes_8">
   <g clip-path="url(#p483b4173b0)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEcAAABHCAYAAABVsFofAAADrElEQVR4nO2cSy9zYRDHzzlK41KXoi6tsCARFWkqYecD8AmsfAA+i4WvYiF2EomVYFEJYuNWRdQ1RV365ixn5nn/Q8UreTO/3ZzM0zb/TKczZ+bU9zyv4ik0NTURe3h4WPgcHx8T++bmRvi8vr4Su7u7m9iFQsH7KVpaWojt+z6xb29vxZngxz7Nf4CJAzBxAD7POe3t7cLp+vqa2HV1dcKnXC57XyUejxO7WCwKn4GBATUvNTc3E/vu7k74vLy8ELuxsRHmpBCLHICJAzBxACbOVxJytYlzYmKC2LlcTviUSiX4Pr29veJaPp/XPp7X2tqqFnRtbW1qkcqxyAGYOAATB+D39PRUtO/i8/MzsQcHB4XP4eEhsScnJ4XP5uYmsd/f32GDG/L4+Kj6cMbGxsS1jY0NmN9cedQiB2DiAEwcgIkD8IMgIAm5pqZGvYNXLclkkthnZ2fEjkaj4sz4+DhMrJ+FJ2D+w/P09CTOWOQATByAifPdxvNfsbq6Kq7V19fDqUHI/Pw8LEhdTe/o6KjaKFvkAEwcgIkDMHF+IyEnWcEXsri4SOxKhb61qwDlnfvIyIjw2d3dJfbc3JzwaWhoIHZtbS2xr66uxBmLHICJAzBxABFt/Ooa/x4cHHgavKl0jW15o/nx8SHO8LuOrrzER9g8B7mKPtfrcCxyACYOwMQBRLLZLLmwtbXlaQRBoN5MWl5eFj58Erm9vU3sqakpceb8/ByeCZmdnSX2+vq6uoLS19cH12xCLHIAJg7AxAGYOL/ReK6trYlrfO8uEqE16N7enjiTSCRgs+oqHl0F6MLCgro3yLHIAZg4ABMH4KdSqYq2ilFS1tU+y9LSErEzmYy64sabXr4O45pQuCanMzMzMHd1dnaKMxY5ABMHYOIATBxA5PT0VJ0aJFghdn9/L3x4Iu/v71fXSXin7CrMeNLmXboruU5PTwsf/uAbnz6cnJyIMxY5ABMHYOIA/EwmQ76wOzs7aiFWdjx4xicArjtr/BkF/kzFysqKOqnkd/A+SzqdhrmLN8EhFjkAEwdg4gBMHIAfjUZJQh4aGhJOObYv5yrwjo6OPA3ePfOE7LqDx8+49oW1My54An54eBA+FjkAEwdg4nx3+tDV1UXsi4sLdRzsegj17e3ty/9iwJvey8tL4cN3k10TimqwyAGYOAATB+DHYrGK9ntfDalUSp1M8n80cdVY+/v7xO7o6FBvtLnW53jjGYvF1NUWixyAiQMwcQAmjvd3/gAfLyy+YOw+4wAAAABJRU5ErkJggg==" id="imagefb96f297fd" transform="scale(1 -1) translate(0 -51.12)" x="68.4" y="-91.751268" width="51.12" height="51.12"/>
   </g>
  </g>
  <g id="axes_9">
   <g clip-path="url(#pbb9fded6ce)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEcAAABHCAYAAABVsFofAAADlUlEQVR4nO2cyUprQRCG+5g4xTFG44CIqGBABFEfQBDcCD6DT6hbXbh0pYi6MYqIihMOOM9DLtlZVX3/PolyN/f/dhWqz4k/ZVHVXZ3IOVdw34iiyGkKBeFSNjU1NcKurKwU9v39vVlTUVEh7K+vL+OTzWaFfX5+HvwumUxG2NfX1/bdwaf8x1AcAMUBJLu6usQHJycnLkTkyUs6f7y9vRmf5uZmYZ+dnZWcp56enozP+/t78Dk9PT3CPjw8FHZ7e7tZw8gBUBwAxQFQHECUzWYLoQIqowqmq6srVw4tLS3CTqfTwj49PTVrfAlYU1VVJezq6upgIfvw8BB8LiMHQHEAFAdQrObEP+PAwIBx2t3dFXZdXZ3xeXx8dD9tYHWT+bdGsxx0kaoLR9+7GTkAigOgOACKU0pCTiaTxunj40PYqVTK+LS1tQn74ODAhZicnBT20tJSsCt/eXlx5RB6ju7aizByABQHQHEAJsH4iqGmpiZh397eGh/dyOmiy/fZ9va2sBcWFsyavr4+Yb++vhqf4eFhYXd0dBgfves4Pj4u7NXVVbOGkQOgOACKA6A4gGSco9TPz08XQidt327h3NycsAcHB4O7c5eXl8JeWVkxPhcXF7Ag9e1m6h3G/v5+s4aRA6A4AIpTSuNZLolEQtiNjY3BQkw3mr5Tg6GhIWHPz88bn4mJCWFvbW0Zn9nZWWHf3d25EIwcAMUBUByA3dny0KeaPz224hsbOzo6Cp5Mtra2ClvXXL7n+Hyen59hDoqbYzSMHADFAVAcAMX5aULe29sLNog62fpmAtfW1mBR6DtZGBsbg7N8voTc0NBgfLq7u+EM4MbGhlnDyAFQHADFAUS5XE40nvl8/lfG3hKqEfWdnG5ubgY31Y6Pj4ObUnrjylfwzczMwDW+URdGDoDiACgOgOKUshOoZ4OL1NbWuu/c3Nw4jU6mvgSn5/AWFxdh8i0yPT0dnFXW7xodHXWl4vu7GTkAigOgOKXknFwuZ5zynsJQMzIyEryzsLOzA08blpeXzRo9hqffUy5xxmoYOQCKA6A4AIoDiFKplEjIU1NTxml9fV3Y+/v77l+hC1C96/dbF0N8MHIAFAdAcX46gpJWTZnvF0M0cS6sxSHO3Qc9dxznlw7iwMgBUBwAxfntsbf6+nrzWZxL7KFTjM7OTrNGb275TjV0E6lPOXyNcG9vL7zkW4SRA6A4AIoDoDju7/wBH/Azup6Sz+MAAAAASUVORK5CYII=" id="image92cd3b0331" transform="scale(1 -1) translate(0 -51.12)" x="129.6" y="-91.751268" width="51.12" height="51.12"/>
   </g>
  </g>
  <g id="axes_10">
   <g clip-path="url(#pdd89c196ae)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEcAAABHCAYAAABVsFofAAADxklEQVR4nO2byUozURCFb5uOQ6IYlRjROAfRrQg+gBtBdOMDuBJfwwfxIQQRBEVcuBIFFwoKDjgFRcV5ipKW3v1Vda1rh7j5Od/uNPd2OodKUXW74o2OjgaGsbS0RPTg4CDRJycnfIu5vb01Lvr7+4ne29sz5aCzs9P5fMPDw0Tv7u6KNc/Pz0RXlOXp/lNgjgLMUfCy2azIOefn5+YvaGtrI/rq6kqs+fr6ItrzPFWHFItF8xcgchRgjgLMUYA5CmF2Ewm5srKS6EKhQHQulxM3Ojg4MOUglUoR/fT0RHRjY6PYc319TXR7e7tYc3Z25vzs6upqohE5CjBHAeYo+LFYTFzkOSaRSBB9fHws9tTW1hL99vYmP8z3iW5qahJr8vk80ZlMxlk4cmx5id/X9tmfn59EI3IUYI4CzFGAOQpeKpUSReD9/b2JSkUF9TkIxG3N/Pw80R8fH2INT+RTU1NEJ5NJsefl5SXy88bjcXGtu7ubaESOAsxRgDkKXiaTCVyNXJL9znlzaDvBW1hYcBZnq6urYs3AwADRy8vLRM/OzppS8gkvZB8eHpz3QeQowBwFmKMAc6KeBLqIWTr59fV1tUu3FZcXFxdizdraGtEzMzNE7+zsiD18zevrqymFjo4OohE5CjBHAeYo+LaCiZ+IJVgBxX+bITc3N0Tv7+87G0Q+8hEyOTmp5jJ+mhgyMjLiLED5d3h/fxdrTk9PiUbkKMAcBZij4Pf19YmLfCTMY2MfthE33njaaiFbruLU1dWpuYGPzoWsrKwQ3dra6nw+Wy3EG2xEjgLMUYA5CjAnauPJk3SevUrlSdM29jE+Pi7WTExMED03N+cs6Pip5PT0tCkHLS0t4trl5SXRiBwFmKMAcxS8XC4XuBqwAhtJSafT4kZ8je10f2tryzlO0tzcTPTQ0JBxwcdJbM00zye/AZGjAHMUYI4CzFHwfN8PXB1smiVgXpiF1NTUqH8CCTk8PFTnfn+aJfyX3t5e531/w29mqRE5CjBHAeZEbTy7urqIrq+vdxZZm5ubzjEV/saT/yk1ZGNjwzk+58KWy2xvG1z7EDkKMEcB5ijAnKgJmc8UF0v49+3Y2Ji4tri46NzHC86GhgaiHx8fS+q4q6qqnDPQPT09RCNyFGCOAsyJmnP469+AFWK2Ao8Xjtvb284xENsrWZ5z+JuOo6MjsYc/TzabFWv4qePd3Z1xNdyIHAWYowBzyj1qG7c0nhzbYRc/yOKjcrZ8x/OADT5yYqth+NiMbUyFv9lF5CjAHAWYowBzzM98A0djNCNwJu5CAAAAAElFTkSuQmCC" id="imagef5a5a39a71" transform="scale(1 -1) translate(0 -51.12)" x="190.8" y="-91.751268" width="51.12" height="51.12"/>
   </g>
  </g>
  <g id="axes_11">
   <g clip-path="url(#p3c973c6dac)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEcAAABHCAYAAABVsFofAAADiUlEQVR4nO2bS0srQRCFe3RiFKPxEXyBUYmIBBc+0IUg+btu/QXu4kKjG/GFC4mK+DZRfJtcZtlVfU/fMZF7L5xvV01NMhxqiuqu6iCTydSN4ObmxsRlenrasj8/P5XP8fGx+Zdpb2+37Ja/9ib/ARQHQHEAgTFG5Zzv0Nra6vWp1+2/qtVqyqe3t9ey7+/vY79Lf3+/Wnt/f7fsMAyVj/wvRg6A4gAoDoDiAMIgiHIyTpx/QldXl2U/PDwon/n5ecve3t5WPrlczrIvLi4s+/z8XD3T09Nj2ZVKRfkkEglvQpYwcgAUB0BxGi0CQ/F9ujaVkmQyqdbe3t68xdrz87Nlv7y8eIvNr68v0wz6+vosm5EDoDgAigOgOAB/JWR0AnYVULIITKfTyufk5CR2sXZ6emrZq6ur6pmlpSV4KhkxODgI/yeipcWOFUYOgOIAKA4gWFhYUEVgqVRCz5ihoSG1JvPHyMiI8rm6urLsx8dH5bO1tQU3misrK+qZVCpl2Ts7O8pHvs/o6KjxwcgBUBwAxQFQHECQSqVUQpY734pItrJtGvH6+mqagSz6ZNJ2FZfyv127dLn29PSkfBYXFy2bkQOgOACK0+hJYEJs0j4+Pkwz2NjYML7xl3w+7z2FlK3egYEB5XN0dATzSwRHUGLAzwpAceJ2PKempiz78PDQsru7u715qVqtKh+Zq2ZmZpTP7e0t7Jy63ld2Olw5R46X7O/vGx+MHADFAVAcAMUBhK5xE5mAJa6Te7lZdSVOydzcnFqTp3hy4+kqAjc3N+FISsTu7q5lLy8vKx+2g2PAzwpAceJ2PGW+qIu85JoNds0U+3DdhVhfX7fsjo4O2FmNKBQK3jEVeUg2MTGhfORvM3IAFAdAcQAUp9kXQ7LZrForl8vmJ5DJ33VR7uzszDuCIk8apO1qgzNyABQHQHHi5py2tjZ4uu8a35Cdyu8iN39yk3t5eameyWQyDV/gjZidnbVsRg6A4gAoDoDiAMLh4WG1KC+A5UVLdm9v78eSomzpTE5OemeX5YmA6yRQ7tzX1taUj2wDMXIAFAdAcQChPGlzUXW0dn1tXNfvym5DsVhUPrK7IIs+13jd+Pi4ZR8cHCgfmWPGxsa8m2dGDoDiACgOIEgmk3XfRVVJZ2end9Mmx8wirq+vTVzkKJrML647FXd3d94xFdfoHsfeYsDPCkBxABTH/J5fv8koDsRTCH4AAAAASUVORK5CYII=" id="imagebf77d34761" transform="scale(1 -1) translate(0 -51.12)" x="252" y="-91.751268" width="51.12" height="51.12"/>
   </g>
  </g>
  <g id="axes_12">
   <g clip-path="url(#pc73473bd4c)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEcAAABHCAYAAABVsFofAAADw0lEQVR4nO2byUorQRSGu000xtk4i2hEURFRHBa6EJ/HFxBXuvQBXLkWRN9BN1ll4YAbUdCNEyLBOWoc4qWXZ7h/defi6p5v9xen0+Sn+lBV55SfSCR+PEZ5eTnRLy8vnovJyUmi9/b2nM/4vi/GmpqaiM7lcl5UWltbxdjt7S3R7e3tIubm5obosshv/o8wcwBmDiD46EXOKSujnhWLRe83mJ6eFmMHBwdEFwoF5+8MDg4SfXJyImIqKyuJfn9/FzGdnZ1E28wBmDkAMwdg5kRNyKUk6K6uLqJrampEzPHxMVxsBnx+fhKdSqWIvru7836L/v5+om3mAMwcgJkDiHshaGhoIPrx8VHE5PN5oi8vL0VMY2Mj3GQGnJ6eEp1MJr2o1NXVibGnpyfnc/zdNnMAZg7AzAGYOQA/nU6LRSBPpim2EGtubhY/xHfCfX196L3qewJeX1/hbvr7+9u5cNROGKurq4mur68XMVdXV0TbzAGYOQAzJ+rGk+eUXAkVgIqKCjH28fHhfG5jY4Pora0topeWlpyVjzCVhTDYzAGYOQAzB2DmAHytHMxP/t7e3ryoJVi+A9cWiqurq87f5Ys+bYH380P/wsLCgoiZmJggOpvNihh+MmkzB2DmAMwcQFxbmMXj+IBweHhYjB0dHTlP3paXl50LxZ6eHqK3t7eJHh8fdy4C+cllwPr6OtEtLS0ihm9ybeYAzByAmQOIa5VJ12FSQWkL4RVP7SCLr4W6u7uduWt2dhYeSAVsbm4SPTMzI2J2dnaIHhsbEzGHh4dE28wBmDkAMwdg5gDiz8/PXtTevayyaQsD77nTkjbv7+MJeG5uTjyTyWSIPjs7EzFTU1NE7+7uOisUNnMAZg7AzAGoO8zR0dHIOWZkZITo6+tr5zetbXB5Dvz6+iJ6f39fPNPb2+tsjdNyjKuNxmYOwMwBmDkAMwfgx2IxUX1Ip9NEn5+fe1F37ryCETAwMED0/Py8iOEnffwEIEwf4eLiooi5v7+HWquY2MwBmDkAMydqCwr/9orsroPWh1zK3QItl62trcFqpnbvYmVlxbnxHBoagvcwtNYbmzkAMwdg5gDMnH+9jJZklzO0lhRe2g3T/5dIJMQYX/TxJMlLtlrPonbzl7eX8EWrhs0cgJkDMHMAflVVlcg5vLUsz07IwuQK7RIZz1WlXBrr6Ohwtq2UWh3h2MwBmDkAMyfqOofnFJ/lIG2t8fDw4EUlFouJsba2NnhnQdt41tbWOtt8Ly4uYIUlwFpQImCfFcDMAZg53t/5A97FLo/zDw/rAAAAAElFTkSuQmCC" id="imageb9d4f4fb9b" transform="scale(1 -1) translate(0 -51.12)" x="313.2" y="-91.751268" width="51.12" height="51.12"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p23fb7d2a4d">
   <rect x="7.2" y="19.278125" width="51.017143" height="51.017143"/>
  </clipPath>
  <clipPath id="p4b451868a5">
   <rect x="68.420571" y="19.278125" width="51.017143" height="51.017143"/>
  </clipPath>
  <clipPath id="p1f9679403c">
   <rect x="129.641143" y="19.278125" width="51.017143" height="51.017143"/>
  </clipPath>
  <clipPath id="p204268f881">
   <rect x="190.861714" y="19.278125" width="51.017143" height="51.017143"/>
  </clipPath>
  <clipPath id="pd8c9d885a5">
   <rect x="252.082286" y="19.278125" width="51.017143" height="51.017143"/>
  </clipPath>
  <clipPath id="p769867c588">
   <rect x="313.302857" y="19.278125" width="51.017143" height="51.017143"/>
  </clipPath>
  <clipPath id="pad021ee2a2">
   <rect x="7.2" y="91.854125" width="51.017143" height="51.017143"/>
  </clipPath>
  <clipPath id="p483b4173b0">
   <rect x="68.420571" y="91.854125" width="51.017143" height="51.017143"/>
  </clipPath>
  <clipPath id="pbb9fded6ce">
   <rect x="129.641143" y="91.854125" width="51.017143" height="51.017143"/>
  </clipPath>
  <clipPath id="pdd89c196ae">
   <rect x="190.861714" y="91.854125" width="51.017143" height="51.017143"/>
  </clipPath>
  <clipPath id="p3c973c6dac">
   <rect x="252.082286" y="91.854125" width="51.017143" height="51.017143"/>
  </clipPath>
  <clipPath id="pc73473bd4c">
   <rect x="313.302857" y="91.854125" width="51.017143" height="51.017143"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Two query pictures (left) and the five most similar pictures by embedding.</figcaption>
</figure>

## Embeddings or raw pixels?

What if we did the same search with raw pixels? The measure that checks how
many of each picture's 5 nearest neighbours are of the same class is called
**precision@5**; let us take the mean over all pictures.

```python
def precision_at_k(features, labels, k=5):
    unit = F.normalize(features, dim=1)
    scores = unit @ unit.T
    scores.fill_diagonal_(-1)
    nearest = scores.topk(k, dim=1).indices
    return (labels[nearest] == labels[:, None]).float().mean().item()


pixels = gallery.flatten(start_dim=1)
print(round(precision_at_k(pixels, labels), 2))
print(round(precision_at_k(vectors, labels), 2))
```

```text
0.66
1.0
```

With raw pixels a third of the neighbours are of another class: a different
shape in the same place can look "more similar" than the same shape somewhere
else. With embeddings almost all neighbours are of the right class. The
features the network learned keep **what** the shape is, not **where** it is.

## Nearest-neighbour classification

With embeddings you do not even need a classification head: looking at the k
training pictures nearest to a new picture's embedding and taking the
majority class is enough (**k-nearest neighbours**, kNN). Adding a new class
needs no retraining; adding the embeddings of a few pictures of that class to
the memory is enough.

```python
memory = F.normalize(embed(x_train), dim=1)
votes = (F.normalize(vectors, dim=1) @ memory.T).topk(5, dim=1).indices
knn_pred = y_train[votes].mode(dim=1).values
with torch.no_grad():
    head_pred = model(gallery).argmax(dim=1)
print(round((knn_pred == labels).float().mean().item(), 2))
print(round((head_pred == labels).float().mean().item(), 2))
```

```text
1.0
1.0
```

kNN is as good as the network's own classification head. `mode` gives the
most frequent value in each row (the majority vote).

## Features from an inner layer: hooks

Sometimes we want the embedding from the middle of the network rather than
the last layer; or we work with a model that is not an `nn.Sequential` and
cannot be split into parts. PyTorch's **hooks** let us catch a layer's output
while the model runs normally:

```python
captured = []


def save_output(module, inputs, output):
    captured.append(output.detach())


layer = model[0][10]
handle = layer.register_forward_hook(save_output)
with torch.no_grad():
    model(gallery[:4])
print(type(layer).__name__, captured[0].shape)
handle.remove()
with torch.no_grad():
    model(gallery[:4])
print(len(captured))
```

```text
ReLU torch.Size([4, 64, 4, 4])
1
```

- `register_forward_hook` calls the given function after each forward pass of
  the layer: `(layer, inputs, output)`.
- What we caught is the `(4, 64, 4, 4)` map of the ReLU after the third
  convolution: before pooling, the position information is still there.
- `handle.remove()` removes the hook; nothing new was added on the second run.
  A hook that is not removed piles up memory on every call.
- We will use hooks again in the section on explaining a model (Grad-CAM).

## Summary

- A trained network's body turns pictures into meaningful embeddings.
- Similarity: `F.normalize`, then a matrix product = cosine similarity.
- precision@k measures search quality; embeddings are far better than raw
  pixels.
- kNN: the majority vote of the nearest embeddings; no retraining for a new
  class.
- An inner layer's output: `register_forward_hook`, then `handle.remove()`
  when done.
