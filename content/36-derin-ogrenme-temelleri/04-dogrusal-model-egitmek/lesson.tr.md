# Gradyan İnişiyle Doğrusal Model

Elimizde artık iki araç var: tensörler ve otomatik türev. Bu bölümde
ikisiyle ilk modelimizi **sıfırdan** eğiteceğiz: bir doğru, `y = w·x + b`.
Hazır katman ya da optimizer kullanmadan, gradyan inişinin her adımını
kendimiz yazacağız. Sonra aynı işi PyTorch'un hazır parçalarıyla yapıp
ikisinin aynı olduğunu göreceğiz. Makine öğrenmesi patikasındaki
`LinearRegression`'ın yaptığı iş bu; farkı, burada çözümü adım adım
**arayarak** bulmamız.

## Veri

Gerçek ilişkisi `y = 3x + 2` olan, üstüne gürültü eklenmiş 100 nokta
üretelim. Gerçek değerleri bildiğimiz için modelin onları bulup
bulmadığını görebileceğiz.

```python
import numpy as np
import torch

rng = np.random.default_rng(0)
x_np = rng.uniform(0, 5, 100)
y_np = 3 * x_np + 2 + rng.normal(0, 0.5, 100)
x = torch.tensor(x_np, dtype=torch.float32)
y = torch.tensor(y_np, dtype=torch.float32)
print(x.shape, y.shape, x.dtype)
```

```text
torch.Size([100]) torch.Size([100]) torch.float32
```

Veriyi NumPy'nin sabit tohumlu üreteciyle kurduk; her bilgisayarda aynı
100 nokta çıkıyor.

## Model ve kayıp

Model iki sayıdan ibaret: eğim `w` ve sabit `b`. İkisini de sıfırla
başlatıyoruz ve gradyan istiyoruz. Kayıp **ortalama kare hata** (mean
squared error, MSE): tahmin ile gerçek arasındaki farkların karelerinin
ortalaması.

```python
w = torch.zeros(1, requires_grad=True)
b = torch.zeros(1, requires_grad=True)


def predict(x):
    return w * x + b


def mse(pred, target):
    return ((pred - target) ** 2).mean()


loss = mse(predict(x), y)
loss.backward()
print(round(loss.item()), round(w.grad.item()), round(b.grad.item()))
```

```text
124 -70 -20
```

- Model her noktaya 0 diyor; kayıp büyük (124).
- İki gradyan da **negatif**: `w` ya da `b` artarsa kayıp azalır. Gradyan
  inişi bu yüzden parametreyi gradyanın **tersine** kaydırır:
  `w ← w − lr · w.grad`.

## Eğitim döngüsü

Şimdi bu adımı tekrarlıyoruz. Her turda: tahmin et, kaybı hesapla,
`backward`, iki parametreyi güncelle, gradyanları sıfırla.

```python
w.grad.zero_()
b.grad.zero_()
lr = 0.05
for step in range(301):
    loss = mse(predict(x), y)
    loss.backward()
    with torch.no_grad():
        w -= lr * w.grad
        b -= lr * b.grad
    w.grad.zero_()
    b.grad.zero_()
    if step % 100 == 0:
        print(step, round(loss.item(), 3))
print("w =", round(w.item(), 1), "b =", round(b.item(), 1))
```

```text
0 124.456
100 0.238
200 0.235
300 0.235
w = 3.0 b = 2.0
```

- Kayıp hızla düşüp 0,235 civarında duruyor. Sıfıra inmiyor,
  çünkü veride gürültü var: hiçbir doğru 100 noktanın hepsinden geçemez.
  Gürültünün standart sapması 0,5, karesi 0,25: kalan kayıp bu civarda.
- Model gerçek değerleri buldu: `w ≈ 3`, `b ≈ 2`. Formül kurmadık,
  yalnızca kaybı azaltacak yönde küçük adımlar attık.

## Öğrenme oranı

`lr`'nin değeri her şeyi değiştirir. Aynı döngüyü üç farklı öğrenme
oranıyla 100 tur çalıştıralım:

```python
def train(lr, steps=100):
    w = torch.zeros(1, requires_grad=True)
    b = torch.zeros(1, requires_grad=True)
    for _ in range(steps):
        loss = ((w * x + b - y) ** 2).mean()
        loss.backward()
        with torch.no_grad():
            w -= lr * w.grad
            b -= lr * b.grad
        w.grad.zero_()
        b.grad.zero_()
    return loss.item()


print(round(train(0.001), 2))
print(round(train(0.05), 2))
print(train(0.1) > 1e6)
```

```text
2.26
0.24
True
```

<figure class="fig">
  <div class="versus">
    <div class="no"><h5>Çok küçük (0,001)</h5>Doğru yönde ama çok yavaş: 100 turda kayıp hâlâ büyük.</div>
    <div class="ok"><h5>Uygun (0,05)</h5>Kayıp gürültü düzeyine iniyor.</div>
    <div class="no"><h5>Çok büyük (0,1)</h5>Her adım çukurun öbür yanına fazla atlıyor; kayıp patlıyor.</div>
  </div>
  <figcaption>Öğrenme oranı adım büyüklüğü: küçüğü yavaş, büyüğü kararsız.</figcaption>
</figure>

Çok büyük öğrenme oranında her güncelleme parametreyi en iyi değerin öbür
yanına, öncekinden daha uzağa fırlatıyor. 0,05 ile 0,1 arasındaki
fark yalnızca iki kat, ama biri iniyor öteki patlıyor; kayıp her turda büyüyor
(ıraksama, divergence). Kaybın `nan` ya da çok büyük çıkması çoğu zaman
öğrenme oranı fazla yüksek demektir.

## Aynı iş hazır parçalarla

PyTorch'ta bu döngünün her parçasının hazırı var: model için
`nn.Linear(1, 1)`, kayıp için `nn.MSELoss()`, güncelleme için
`torch.optim.SGD`.

```python
from torch import nn

model = nn.Linear(1, 1)
nn.init.zeros_(model.weight)
nn.init.zeros_(model.bias)
optimizer = torch.optim.SGD(model.parameters(), lr=0.05)
loss_fn = nn.MSELoss()
X = x.unsqueeze(1)
Y = y.unsqueeze(1)
for step in range(301):
    optimizer.zero_grad()
    loss = loss_fn(model(X), Y)
    loss.backward()
    optimizer.step()
print(X.shape, round(loss.item(), 3))
print("w =", round(model.weight.item(), 1), "b =", round(model.bias.item(), 1))
```

```text
torch.Size([100, 1]) 0.235
w = 3.0 b = 2.0
```

- `nn.Linear` girdi olarak `(adet, özellik)` ister; tek özellikli `x`'i
  `unsqueeze(1)` ile `(100, 1)` yaptık.
- Ağırlıkları elle yazdığımız sürümdeki gibi sıfırdan başlattık
  (`nn.init.zeros_`); sonuç aynı çıktı.
- Elle yazdığımız dört adım burada da var: `zero_grad`, kayıp, `backward`,
  `step`. `optimizer.step()` bizim `w -= lr * w.grad` satırımızın aynısını
  bütün parametrelere uyguluyor. Giriş bölümündeki rakam modeli de tam
  olarak bunu yapıyordu; yalnızca modeli daha büyüktü.

## Özet

- Gradyan inişi: kaybı hesapla, gradyanı al, parametreyi gradyanın tersine
  `lr` kadar kaydır, gradyanı sıfırla; tekrarla.
- Parametre güncellemesi `torch.no_grad()` içinde yapılır.
- Öğrenme oranı küçükse yavaş, büyükse ıraksar.
- `nn.Linear`, `nn.MSELoss` ve `optim.SGD` aynı algoritmanın hazır hâli.
