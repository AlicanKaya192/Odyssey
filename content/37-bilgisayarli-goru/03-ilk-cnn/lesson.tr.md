# İlk CNN'i Eğitmek

Önceki bölümde CNN'in iskeletini kurduk ama hiç eğitmedik; ağırlıkları
rastgeleydi. Bu bölümde aynı ağı şekil resimleri üzerinde eğitip daire, kare
ve üçgeni ayırt etmeyi öğreteceğiz. Eğitim döngüsü Derin Öğrenmenin Temelleri
modülündekiyle aynı: ileri hesap, kayıp, geri yayılım, adım. Yeni olan,
girdinin bir resim yığını olması. Sonunda aynı işi tam bağlı bir ağa (MLP)
yaptırıp ikisini karşılaştıracağız.

## Veri: eğitim ve test

Eğitim ve test resimlerini farklı tohumlarla üretiyoruz: test resimlerini ağ
eğitimde hiç görmeyecek. `DataLoader` resimleri 32'lik yığınlar hâlinde,
her turda karıştırarak veriyor; karıştırmanın her çalıştırmada aynı olması
için kendi tohumlu üretecini (`generator`) veriyoruz.

```python
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from dl_data import make_shapes, SHAPES

x_train, y_train = make_shapes(600, seed=1)
x_test, y_test = make_shapes(300, seed=2)
train_set = TensorDataset(torch.from_numpy(x_train), torch.from_numpy(y_train))
x_test, y_test = torch.from_numpy(x_test), torch.from_numpy(y_test)
loader = DataLoader(train_set, batch_size=32, shuffle=True,
                    generator=torch.Generator().manual_seed(0))
images, labels = next(iter(loader))
print(len(train_set), len(loader))
print(images.shape, labels.shape)
```

```text
600 19
torch.Size([32, 1, 16, 16]) torch.Size([32])
```

600 resim, 32'lik yığınlarla 19 yığın (sonuncusu 24 resim). Her yığın
`(32, 1, 16, 16)` şeklinde: CNN'in tam beklediği biçim.

## Ağ ve eğitimden önceki durum

Ağ önceki bölümdekinin aynısı. Eğitimden önce bir yığında kaybına ve test
doğruluğuna bakalım:

```python
def make_cnn():
    return nn.Sequential(
        nn.Conv2d(1, 8, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(8, 16, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Flatten(),
        nn.Linear(16 * 4 * 4, 3),
    )


def accuracy(model, x, y):
    model.eval()
    with torch.no_grad():
        return (model(x).argmax(dim=1) == y).float().mean().item()


torch.manual_seed(0)
model = make_cnn()
loss_fn = nn.CrossEntropyLoss()
print(round(loss_fn(model(images), labels).item(), 1))
print(accuracy(model, x_test, y_test) < 0.5)
```

```text
1.1
True
```

- Ağın çıktısı her sınıf için bir puan (logit). `CrossEntropyLoss` bu
  puanları olasılığa çevirip doğru sınıfın olasılığının eksi logaritmasını
  alıyor. Üç sınıfta hiçbir şey bilmeyen bir ağın kaybı `log 3 ≈ 1,1`.
- Tahmin, en büyük puanın sırası: `argmax(dim=1)`. Eğitimden önce doğruluk
  şans düzeyinde (üçte bire yakın).
- `accuracy` ölçerken `model.eval()` ve `torch.no_grad()` kullanıyor: ağı
  değerlendirme kipine alıyor ve türev kaydını kapatıyor (notlarda
  ayrıntısı var).

## Eğitim döngüsü

```python
def train_epoch(model, loader, optimizer):
    model.train()
    total = 0.0
    for images, labels in loader:
        optimizer.zero_grad()
        loss = loss_fn(model(images), labels)
        loss.backward()
        optimizer.step()
        total += loss.item() * len(labels)
    return total / len(loader.dataset)


torch.manual_seed(0)
model = make_cnn()
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
for epoch in range(1, 9):
    loss = train_epoch(model, loader, optimizer)
    if epoch % 2 == 0:
        print(epoch, round(loss, 2), round(accuracy(model, x_test, y_test), 2))
```

```text
2 0.87 0.58
4 0.62 0.8
6 0.28 0.9
8 0.14 0.95
```

- Her tur (epoch) eğitim verisinin tamamından bir kez geçiyor.
- Yığın başına dört adım: türevleri sıfırla (`zero_grad`), kaybı hesapla,
  geri yay (`backward`), ağırlıkları güncelle (`step`).
- Kayıp düşüyor, test doğruluğu yükseliyor. Sekiz turda ağ test
  resimlerinin büyük çoğunluğunu doğru biliyor. Bu bilgisayarda eğitim bir
  iki saniye sürdü.

## Tahminlere bakmak

Doğruluk tek bir sayı. Ağın neyi bildiğini görmek için tahminlerin
kendisine bakalım:

```python
model.eval()
with torch.no_grad():
    predictions = model(x_test).argmax(dim=1)
for i in range(5):
    print(SHAPES[y_test[i]], SHAPES[predictions[i]])
wrong = (predictions != y_test).sum().item()
print(wrong < 25)
```

```text
triangle triangle
circle circle
circle circle
circle circle
square square
True
```

İlk beş test resminin hepsi doğru. 300 test resminden yanlış bilinenler
25'ten az. Hangi resimlerde yanıldığına bakmak, bir sonraki iyileştirmenin
nerede olacağını söyler:

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="371.52pt" height="87.898237pt" viewBox="0 0 371.52 87.898237" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 87.898237 
L 371.52 87.898237 
L 371.52 0 
L 0 0 
L 0 87.898237 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g clip-path="url(#p6a5fa3b46d)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEcAAABHCAYAAABVsFofAAADg0lEQVR4nO2cPU9qQRCGz8EjCH6gUaHRBI3RBhqjjYmVnQk/gZ/Ar7OhoTAmRhMTGxujEiORBI3gR/wGj6G7O7P33YOXe5v7Pt1sZo/4Zs6wOzuL73le6P3C3NycJ2k2m4YdBIHyeX199f6UTCajxoaHhw377u5O+by9vTmfHY/HDfvj48M5J+b0+I+hOACKA1DJ4/7+Xjl9fn5C28bQ0JAaGxkZge99uVxWc5aXl5257evry7BnZmaUT6fTgZ9le3tbzWHkACgOgOIAKA7Al4tAG/Pz84Zdr9eVTyqVMuyXlxflMz4+DhdmFxcXas7x8bFhn52dKZ/p6WnDfnx89FxfNGtra4a9ubmp5jByABQHQHEAegdpoW7JMRJbjpHIBdzT05NhVyoVNUf6FItF5dNqtQz78PBQ+WxtbRl2tVqF+bAHIwdAcQAUB0BxAIGs6snda1SiVNrkQlEu1hYWFtScRqNh2Lu7u8pncXHRsNfX15XP3t6eYYdhCBN/D0YOgOIAKA4gyGazxsD19bXnYmpqSo0lEgnDbrfbykfmGPm3u92umnN7ews3mbbKpG3jKfPZycmJ87mMHADFAVAcAMUBBLGYqc/KyopyOj09dSbbKLh2xvKz2BKl3IH3mJiYMOyDgwPlMzk5adi5XM55zMzIAVAcAMUBBLLKt7q66v0tqo7q29XVlbP9pVAoKJ9arWbYpVJJ+ezs7MAcNDY2puYwcgAUB0BxAH4ymQxdLR5ZsUGUhaIeNzc3Xr/Izer7+7s3COQapsfl5SVcP9nWbowcAMUBUBwAxQH4vu+HrhOAmlhkRWFjY0ON7e/vwzlyYWb7grB9GUTpKf4JjBwAxQFQnH7a3paWlpRTSxSYbL3Kshf4XyLvR9j6pOX/dX5+7nwuIwdAcQAUB0BxAH48Hg9dlyq64pjW1j8nE5xsN7H1Dc7OzsKj3x7pdNpZsZNH2LbLcq6LIbYLbYwcAMUBUByAH4vFwn4Xc8lkUo3Jd9a2QXQR5bT1p8hq5sPDg7MKycgBUBwAxQFQnH525bZ+v3aElpPR0VFndU4+WyZtW3uJTP62RC8riFH6GqPAyAFQHADFAQSDquglxNHu8/Nz30fGtkWg3OQeHR0pn3w+78w5/BWUAcPXCkBxAH4qlQpdF1lzoqVDtnNELR65iFKkGhTyV1ps9y4YOQCKA6A4AIrj/Z5vqz87OpMdm4wAAAAASUVORK5CYII=" id="imagef7ca50cf69" transform="scale(1 -1) translate(0 -51.12)" x="7.2" y="-29.578237" width="51.12" height="51.12"/>
   </g>
   <g id="text_1">
    <text style="font-size: 8px; font-family:inherit; fill: currentColor" transform="translate(19.081696 14.078906)">square</text>
    <text style="font-size: 8px; font-family:inherit; fill: currentColor" transform="translate(17.446696 23.681094)">&gt; circle</text>
   </g>
  </g>
  <g id="axes_2">
   <g clip-path="url(#p2572505704)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEcAAABHCAYAAABVsFofAAADiUlEQVR4nO2cuU5rMRRFnXAJUyBCzJNAEFEARQooaZH4FL6Eim/ge6hASFCBmFGAMCdMCeTpdnjbbOfmofeavbpjnYR7tw5bto+dlDGmbr4xODhokOvrayvu6elxcp6enkxShoeHrfjl5cXJ6ejosOKrqysnJ5/PW/HBwYGT09bWZsX1uvXa5uPjw/lM+scnFxKHocohROgf6C8xo6Oj5jvpdDroOZlMJvg9x8fHVry4uOh85uzszIoLhYKT09nZacWPj49Ozs3NjUmKKocgcQgShyBxCCmcBPqIosiKa7WaaYaBgQE68fIZ6f9ElUOQOASJQ4hwUlWtVp2kYrFoxRsbGybE/f29M3Z6emrFa2trVjw7Oxv83lwu54yhV+FC1LcY7erqor4ao8ohSByCxCFIHEK0s7NjDczNzTlJVTDpo6MjJ2dmZsaKs9msk7OysmLF6+vrJimpVDxv5fh2ApGFhQUr3tracnJUOQSJQ5A4hGhkZMQaeHh4CHpO1uMn7+/vVlwul50cHFteXrbizc1NE+Lt7S3oH3t7e04Odhsa8SVVDkHiECQOQeIQos/Pz+Cq/PX11Yr7+vqCbduvry8nZ39/34qXlpZMUnyGfHd3R3ccfSv329tb+vwxqhyCxCFIHEKErVRs0cZ0d3eb7/T29hoEPWZ8fNzJwUXt+fm5SQo+r2/XET0yZn5+3ooPDw+DXqbKIUgcgsRJ0vH07cLXoMM5NTUV7FDgMTPf4hT/z32fwTnV5eWl+VeocggShyBxCBKHkCoUCvWQ4ZVhB893XrgRcDI5NDSU+PwwmrrvjKJvoojvgOetfbubqhyCxCFInCSTQOxc+hZp7e3tJuQNv3WEbXJy0opPTk6a+p7V1VUr3t7eDr6TKocgcQgShyBxkhhya2tr0GzLnlYv0t/f74xhpwPxXQirVComKRMTE8ELJvievq6LKocgcQgShxBhp8930azcgMcgpVLJGcMFYUtLC42bJeRtMWNjY8GLtaocgsQhSByCxCFEOMHz3eqtwEQMd/B8huZb5eIO4vT09K+s5NFcfTeB8fwytr1955tVOQSJQ5A4hAjPHftu/JdgQuc7goJ+8vz8bEJgO9h3XA39ZHd318m5uLgI/i18ZnxvPKcco8ohSByCxPnbS/cZmPv4NqWwm9mI5zQC/nJKs0dQsKOJi2n0thhVDkHiECQOQeKYn/kDpjswHpFanwMAAAAASUVORK5CYII=" id="image9653fd870c" transform="scale(1 -1) translate(0 -51.12)" x="68.4" y="-29.578237" width="51.12" height="51.12"/>
   </g>
   <g id="text_2">
    <text style="font-size: 8px; font-family:inherit; fill: currentColor" transform="translate(80.302268 14.078906)">square</text>
    <text style="font-size: 8px; font-family:inherit; fill: currentColor" transform="translate(73.884143 23.681094)">&gt; triangle</text>
   </g>
  </g>
  <g id="axes_3">
   <g clip-path="url(#p421f1b70d7)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEcAAABHCAYAAABVsFofAAAD7klEQVR4nO2cyUprQRCG+yRHY5yioqI4D+CMAYMIbgQ37nwTn0Afwp1v4DO4U9wIDig4ISIijohzVMQhl7Ozhvt3And369v9oTqJP30qXV3dBs65nPtFOp12nK+vL6J3d3edj4aGBvHa9fU10Y2NjURfXV2JMePj40Svra2JmPLycqKrqqpEzOPjI9FPT0/OR8wb8R9j5gDMHECQTqdJztne3hZBLS0tRNfX14uY/f19ot/f352P9vZ275iPjw+YO/KlsrKS6OfnZ6ITiYQYYzMHYOYAzByAmQMI+CIwnwVdEETDHExwQ0NDImZnZwcm4DAMvQs8LSF3d3cTfXZ2JmIqKiqIvru7I7q/v1+MsZkDMHMAZg4giMViJOe0traKoJ+fH2/RlsvlYA6KGBkZIXpzc9P5iMfjRH9/f3tzDi9wI7LZrCsUmzkAMwdg5gDMHECQyWRIJr25uRFBr6+vRN/f33sXa1oCTCaTcBHId/0ijo6OiL69vXU+tAqbV/c1NTVEx2JyntjMAZg5ADMHEO7t7cFOQ8Tw8LD7zcvLi+PwHLOwsCBieLchlUoRfXl5KcaMjY15uw/V1dVEn5+fi5iZmRm4aLWcUyD2WAHMHICZAwj5Qqy5uVkEbWxswEpZa7MUFRV5q2eO1hbiu3raLl9XV5fzLWR5wuU/IJ+fn3IM/Lb/OWYOwMwBiO1+bZevqamJ6IuLCxFTXFxMdF1dnfNxcnLi3eUrKysjuq+vz7sI7OzsFDH8WIr2N3Bs5gDMHICZU0jHkxeZEfkUpxxt3bC4uEh0T0+P9zgdLxC1ondwcJDot7c3ETM9Pe0KxWYOwMwBmDkAMwcQxOPxnG8hlmI7dvmc4Z2fnxevtbW1wbOFWkHLi0ieoDV4ZyFidnaW6JWVFef7IbKZAzBzAGYOIMxkMt6FWCPrGpSWlooY3onkY7Qcw+86aO/b0dEBj8NoR9hKSkpEjHZU7zcPDw/iNZs5ADMHYOYAzBxAuLW1BRd8WoI7PDx0vuMlWgeA7yjy880HBwdizPLyMtETExMiZn19neje3l4Rs7q6Cj9bw2YOwMwBmDmAIJFI5HyF3Sfb1eMdgYja2lqi5+bmRAwfx+868J1BrauhdUX5+2jfb2pqyhWKzRyAmQMwcwBmDiDkN3+Pj4+dj6xyxpgf8ZicnPRW7rwlu7S0JMaMjo7Cz9FaxLxK19rTfMdTq9pt5gDMHICZU0j3geegiNPTU/cv4MdAeP7g9ye0GK2gHRgYgMf0tJzCF7vaLqTNHICZAzBzACF/prX8kvTck9Lgl9zz+Q8m2j0uXtBqn53P5VZfp9SO2haIPVYAMwdg5ri/8wer3E3NkBQbwQAAAABJRU5ErkJggg==" id="image3657c4b4ea" transform="scale(1 -1) translate(0 -51.12)" x="129.6" y="-29.578237" width="51.12" height="51.12"/>
   </g>
   <g id="text_3">
    <text style="font-size: 8px; font-family:inherit; fill: currentColor" transform="translate(141.522839 14.078906)">square</text>
    <text style="font-size: 8px; font-family:inherit; fill: currentColor" transform="translate(139.887839 23.681094)">&gt; circle</text>
   </g>
  </g>
  <g id="axes_4">
   <g clip-path="url(#p04f9c73880)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEcAAABHCAYAAABVsFofAAADdUlEQVR4nO2cOU8jQRCFe4wxiNMgboQgAoQlApAgcOofjURKAkLgEBLEfYMNmMtgWJFtVde+np7dbN+XPatnDE89RVV1DYlz7tspRkZGhG61WkInSaIvce3t7UJfXFy4EJ2dnd5nHx8fQk9OTgp9fHwcvO/4+Lj3WUdHh9CHh4femqmpKaFzwW/6j6E5AJoDSKyY09XVJfTg4KDQp6enLoSOQVY8sdZMTEwI3Wg0hL67u/OuGRgYELpWq7l/AXcOgOYAaA6A5sQG5Hw+L3R3d7fQDw8P3o3a2tpg8mYlcPp7fvj8/BS6v78/eI0VpLOg/0Bw5wBoDoDmAPwH2Dk3PDws9NXVVbDw/Pr6Erperwfve3t760L09vZGJ6AW8/PzQu/t7XlrGHMi4GMFoDkAmgNICoVCsCqfmZkRulqtBrt6b29vLgu6Kr+5uYn+Y6C7fj88Pz9H/yzcOQCaA6A5gGRubs6LOfv7+0Kvr68LXalUXIiDgwPvs6GhIaEvLy+9NcvLy0JPT08L/fj46F2jk0ldvFpdyDRw5wBoDoDmAGhObCdQ8/0tlxwdHXlrrq+vhX5/f/fW6MRwYWHBW2N1EH9ndXXV++z8/NyFODk5CR4L6Q4Adw6A5gBoTmwncGlpCV3jHQ9bhefo6Ki3ZmNjQ+i+vr7gc68Lzc3NTe+aXC4HtUWapJA7B0BzADQnNubs7OzAETZrrGx7exs2zKyTU+uE4unpCcYlXYhaeZdufqVFj65w5wBoDoDmAGhObEDWtNQcsj4RsBLDtbU1b025XIbFqsXi4iJMJK0TC6vDqGeMrdMI3VHkzgHQHADNAeStIk0nUbu7u/AUwSoYrWf69fU1GBtKpVIwxmRpdukET4/TWXDnAGgOgOYAaE7s6UNPTw88SbCOW3XFbVXPerYwy0ygrtotxsbGgnPSZ2dnwftw5wBoDoDmxMacYrEotE4U7+/vvRsVCgWhm82my4IuYPV36STRGpmxYmLod7RiLXcOgOYAaA6A5vztCErobdy0b+SurKwIvbW15WJJ00Ww0MfKs7OzwcDOnQOgOQCaExtz9DhJUyV0uhi0Tij0qJzVHbRGUKw541is/66S5V0M7hwAzQHQnNgTT51LJCpHsF66T4NuOKXJT/Qoy8vLi7dGv1+V9V0vnftw5wBoDoDmAGiO+zO/AAxxHGh4t/KnAAAAAElFTkSuQmCC" id="image7f0bcc70d8" transform="scale(1 -1) translate(0 -51.12)" x="190.8" y="-29.578237" width="51.12" height="51.12"/>
   </g>
   <g id="text_4">
    <text style="font-size: 8px; font-family:inherit; fill: currentColor" transform="translate(202.743411 14.078906)">square</text>
    <text style="font-size: 8px; font-family:inherit; fill: currentColor" transform="translate(201.108411 23.681094)">&gt; circle</text>
   </g>
  </g>
  <g id="axes_5">
   <g clip-path="url(#p9243638a59)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEcAAABHCAYAAABVsFofAAADqklEQVR4nO2byUszQRDFe8wY92hMghsuSIjLRRG8iHjxP/cmqIjghopbDInGPYm7kRxr8TXzKd/F+t3eUJNMHp2ipqo7cM7VXURGRkbEtXK5THStVhMxvb29RN/c3Hi/q6Ojg+hqtSpiZmdnid7c3BQxY2NjRJ+cnIiYgYEBopu8T/eHMXMAZg4gyGQyIudcXV0RPTk5SfTe3p74oOXlZaIPDg5EzNnZmYtKa2sr0alUSsRcXFy432BwcJBoWzkAMwdg5gDMHEDwL0WgRnNzM9GLi4siZnd3l+hiseh+g2QySfTb25uIqdfr3mKSF6m2cgBmDsDMAQRhGIqc8/7+7n5KT0+PuHZ3d+ct6FpaWoguFAre7wrDkOhMJuPNJ9vb2yKmqYmuFVs5ADMHYOYAzBxAmM1mxcXn52fYNWtraxP3PD09OR88AV9fX7uoLCwsiGvr6+uwIG1wdHQEO4Pa77SVAzBzAGYOIIjFYqIIjMVicNpweHjofGj/e/5C2NXVJWIeHx8jdeu0a2tra+43sJUDMHMAZg7AzAGEnZ2d4uL9/T3RiUQCvjk3eHl5ITqXy4mY4+Njoh8eHkTM6+sr0fF4nOiNjQ1xz9zcHNFB0GhwOvgbtHH15+cn0bZyAGYOwMwBBMlkUhSBt7e36B7X3t7ufN1DnjsaXF5eejt2PBfw79I+lz8vn0ZoL8s8v2jYygGYOQAzBxBqNQtvBJXZlrZKpeJ88LriuxzDOT8/J3piYgJOMLSpAc9t2vY5PgHVfpetHICZAzBzAGZO1C0oPMHNz88Tvbq6Kj6IF17aHuOVlRWil5aWnA/ePdQ6jBytUOR7jLXn40nbVg7AzAGYOVFzDi/WKqw40l48+cSCN6m0Ai+fz3u3rmjNOF9zrru7W8TwBpi2Rebj44NoWzkAMwdg5gDMnJ/uQx4aGvIexOBJXOvub21tET0+Pu77are/vw/f0jW0Tubo6GiksXMDWzkAMwdg5kTNOdPT00Tv7Ox4cwUvqrTJJEfrxvn2HfPDaVqBxw/PaWcd0um0iDk9PSXaVg7AzAGYOQAzJ2pC5ttHEmzMwkc12h5e3lX77gBYVLREyp9HGwfzwyPDw8Mihm+JsZUDMHMAZg4g6OvrEzmnVCqhe9Qun9bx99Hf3+/dysLzCZ8iaGc1uNa6g1qHkXczbeUAzByAmfM/Dt3HWR7SchCfpGpTAt+WO42ZmRnvyymf0mp12NTUFH3eyE/yhzBzAGYOwMxx3/MF9CAhDFoSqaEAAAAASUVORK5CYII=" id="image04133dc9eb" transform="scale(1 -1) translate(0 -51.12)" x="252" y="-29.578237" width="51.12" height="51.12"/>
   </g>
   <g id="text_5">
    <text style="font-size: 8px; font-family:inherit; fill: currentColor" transform="translate(266.952107 14.079531)">circle</text>
    <text style="font-size: 8px; font-family:inherit; fill: currentColor" transform="translate(259.340857 23.681094)">&gt; square</text>
   </g>
  </g>
  <g id="axes_6">
   <g clip-path="url(#p5f38ac7118)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAEcAAABHCAYAAABVsFofAAADZUlEQVR4nO2czUtyURDG7y1TyorErMSiSEFBoU0r8Z8PolWLIouCCoK+Kcu+6EO70e49M9Nz7k3eVs9vN4dzj/EwTjNn5hoGQRAFCWk2m2ptY2Mj6TFBqVRSa09PT9CenZ1Vz5yfnzt2uVxWe+bn5x17bW1N7QnD0LGHfvzLCcVB0HMAYaFQUDHn5eXFsRcXFx17b28v+CsymYxjv729qT2Tk5OOXSgU1J6joyPHHhrSfiHX6DkAigOgOACKA/jOelRAnpiYcOx8Pu/Y7+/v6qDX11fH7nQ6/g8XSdc3URQlfkYGYGvP1dVVkBR6DoDiAChO0pgjC8KzszPHbjQa6qB2ux34yOVyjn13d6f2zMzMOPbw8HDiWGYVtDc3N4798PDgLU7pOQCKA6A4AIoDSFmLt7e3MKmSVXvcoCjPrdVqas/+/j48N51OqzWZlF5fX6s98kbR4vT01LHpOQCKA6A4gLBWq0W+hKnX60E77nda3uqNjY2pPTIxlDFmdHRUPdPtdmGyad3yyfhnJZz0HADFAVAcAMVJWpXLqrsdo+L+K2TV/lPSJ8lms95kst/vOzY9B0BxABQHEFarVRVzDg4OHHtlZcWxd3d31UFWYigZGRlx7I+PD+8z8rN3dnbUns/Pz+B/QM8BUBwAxQGElUol8uUE29vb3q7k+vq6Yy8tLXlzFFmIWsh8xCoqZTfTKmjlBZ01pnJ/f+/Y9BwAxQFQHADFSdp9kHO9kQjAW1tb6plWqwVn8KzgenFxofYsLCzAzkKcUZI43RGrHSyTUnoOgOIAKA4g9fz8rBZ9BWHZeLdAxgJrz/HxsXc8TY7YyY6AjIe/xZpnltBzABQHQHEAFCdp9yHpbLCFvE20KmqrkyBvC+PcMEqWl5e9/wzijLLQcwAUB0BxAGEul4t8nb+uGPGIg7xVs27orO+9lRj+y/j4+K/GX2QX1xpBkYUwPQdAcQAUB0BxACnr5QwZKEMRJB8fH72B0hpbqdfriVsz09PT3l8kkDOM1m2hrO6tW0gJPQdAcQAUB5BaXV1Vi5ubm44t98gXZH/L1NSUN3mU8U3Gl7jIc/iLBAPCrxWA4gx62SUpFotqTRancbqOc3Nzau3y8jIYlEqlotYODw/hL7t8c3Jy4tj0HADFAVAcAMUJfuYLLQog6F7+v7kAAAAASUVORK5CYII=" id="imagec75aa77869" transform="scale(1 -1) translate(0 -51.12)" x="313.2" y="-29.578237" width="51.12" height="51.12"/>
   </g>
   <g id="text_6">
    <text style="font-size: 8px; font-family:inherit; fill: currentColor" transform="translate(328.172679 14.079531)">circle</text>
    <text style="font-size: 8px; font-family:inherit; fill: currentColor" transform="translate(320.561429 23.681094)">&gt; square</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p6a5fa3b46d">
   <rect x="7.2" y="29.681094" width="51.017143" height="51.017143"/>
  </clipPath>
  <clipPath id="p2572505704">
   <rect x="68.420571" y="29.681094" width="51.017143" height="51.017143"/>
  </clipPath>
  <clipPath id="p421f1b70d7">
   <rect x="129.641143" y="29.681094" width="51.017143" height="51.017143"/>
  </clipPath>
  <clipPath id="p04f9c73880">
   <rect x="190.861714" y="29.681094" width="51.017143" height="51.017143"/>
  </clipPath>
  <clipPath id="p9243638a59">
   <rect x="252.082286" y="29.681094" width="51.017143" height="51.017143"/>
  </clipPath>
  <clipPath id="p5f38ac7118">
   <rect x="313.302857" y="29.681094" width="51.017143" height="51.017143"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Yanlış bilinen ilk altı test resmi: üstte doğrusu, altta ağın tahmini.</figcaption>
</figure>

## CNN ile tam bağlı ağ

Aynı veriyle, aynı döngüyle, resmi düz bir listeye çeviren tam bağlı bir ağ
eğitelim:

```python
def make_mlp():
    return nn.Sequential(nn.Flatten(), nn.Linear(256, 64), nn.ReLU(), nn.Linear(64, 3))


torch.manual_seed(0)
mlp = make_mlp()
optimizer = torch.optim.Adam(mlp.parameters(), lr=0.005)
for epoch in range(8):
    loss = train_epoch(mlp, loader, optimizer)
mlp_acc = accuracy(mlp, x_test, y_test)
cnn_acc = accuracy(model, x_test, y_test)
print(round(mlp_acc, 2), round(cnn_acc, 2))
print(sum(p.numel() for p in mlp.parameters()), sum(p.numel() for p in model.parameters()))
```

```text
0.73 0.95
16643 2019
```

- Tam bağlı ağın sekiz kat fazla parametresi var ama test doğruluğu belirgin
  biçimde düşük.
- Sebep, ilk bölümde gördüğümüz sorun: şekiller resmin farklı yerlerinde.
  Tam bağlı ağ "sol üstte daire" ile "sağ altta daire"yi ayrı ayrı
  öğrenmek zorunda. CNN'in çekirdekleri aynı deseni her yerde arıyor.
- Bu, evrişimli ağların görüntüde neden standart olduğunun özeti: **daha az
  parametreyle daha iyi genelleme**.

## Özet

- Görüntü sınıflandırmada eğitim döngüsü aynı; girdi `(N, C, H, W)` yığını.
- `CrossEntropyLoss` ham puanları (logit) alır; tahmin `argmax(dim=1)`.
- Ölçerken `model.eval()` ve `torch.no_grad()`; eğitirken `model.train()`.
- Konumu değişen desenlerde CNN, tam bağlı ağdan az parametreyle daha iyi
  sonuç verir.
