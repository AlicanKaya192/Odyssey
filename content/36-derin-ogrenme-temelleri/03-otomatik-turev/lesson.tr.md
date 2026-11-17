# Otomatik Türev

Bir modeli eğitmek için her parametrenin **gradyanını** bilmemiz gerekir:
o parametre biraz artarsa kayıp ne kadar ve hangi yönde değişir? ML
Algoritmaları modülünün Sinir Ağı bölümünde bu türevleri zincir kuralıyla
elle çıkarmıştık; her yeni katman için yeni formül yazmak gerekiyordu.
PyTorch'un **otomatik türev** (autograd) sistemi bunu bizim yerimize yapar:
tensörlerle yaptığımız her işlemi kaydeder, `backward()` deyince türevleri
sondan başa doğru hesaplar.

## İlk türev

Bir tensöre `requires_grad=True` dersek PyTorch onunla yapılan işlemleri
izlemeye başlar:

```python
import torch

x = torch.tensor(2.0, requires_grad=True)
y = x ** 2 + 3 * x
y.backward()
print(y.item(), x.grad.item())
```

```text
10.0 7.0
```

- `y = x² + 3x`, `x = 2`'de `4 + 6 = 10`.
- Türevi `2x + 3`; `x = 2`'de `7`. `backward()` bu sayıyı hesaplayıp
  `x.grad`'a yazdı. Formülü biz yazmadık.

## Hesap grafiği

PyTorch her işlemi bir **hesap grafiğine** (computation graph) ekler. Her
sonucun `grad_fn`'i onu hangi işlemin ürettiğini söyler:

```python
a = torch.tensor(1.0, requires_grad=True)
b = 3 * a + 1
c = b ** 2
print(type(b.grad_fn).__name__, type(c.grad_fn).__name__)
print(a.grad_fn, a.is_leaf, c.is_leaf)
c.backward()
print(a.grad.item())
```

```text
AddBackward0 PowBackward0
None True False
24.0
```

<figure class="fig">
  <div class="flow">
    <span class="node acc">a = 1</span><span class="arrow">→</span>
    <span class="node">b = 3a + 1<br><small>AddBackward0</small></span><span class="arrow">→</span>
    <span class="node">c = b²<br><small>PowBackward0</small></span>
  </div>
  <figcaption>İleri hesap soldan sağa; <code>backward()</code> grafiği sağdan sola dolaşıp zincir kuralını uygular.</figcaption>
</figure>

- `a`'yı biz kurduk: grafiğin **yaprağı** (leaf), `grad_fn`'i yok.
  Parametreler hep yapraktır; gradyanları onların `.grad`'ında birikir.
- Zincir kuralı: `dc/da = dc/db · db/da = 2b · 3`. `a = 1`'de `b = 4`,
  sonuç `2 · 4 · 3 = 24`.

## Birden çok girdi, vektörler

Kayıp genelde birçok parametreye bağlıdır. Tek bir `backward()` hepsinin
gradyanını birden hesaplar:

```python
w = torch.tensor([1.0, -2.0, 0.5], requires_grad=True)
x = torch.tensor([3.0, 1.0, 2.0])
b = torch.tensor(0.0, requires_grad=True)
loss = ((w * x).sum() + b - 4) ** 2
loss.backward()
print(loss.item(), w.grad.tolist(), b.grad.item())
```

```text
4.0 [-12.0, -4.0, -8.0] -4.0
```

- Tahmin `w · x + b = 3 - 2 + 1 + 0 = 2`, hedef 4, kayıp `(2 - 4)² = 4`.
- `d kayıp / d w = 2 · (2 - 4) · x = -4x` → `[-12, -4, -8]`;
  `d kayıp / d b = -4`.
- `x` için `requires_grad` demedik; veri sabit, gradyanı gerekmiyor.
- Gradyanın şekli parametrenin şekliyle aynı: `w` üç sayı, `w.grad` da üç
  sayı.

## Gradyanlar birikir

`backward()` gradyanı `.grad`'a **ekler**, üzerine yazmaz:

```python
x = torch.tensor(2.0, requires_grad=True)
for step in range(3):
    y = x ** 2
    y.backward()
    print(step, x.grad.item())
x.grad.zero_()
print(x.grad.item())
```

```text
0 4.0
1 8.0
2 12.0
0.0
```

Türev her seferinde 4, ama `x.grad` 4, 8, 12 diye büyüyor. Eğitim
döngüsünün başındaki `optimizer.zero_grad()` tam olarak bunu önlüyor:
her turun gradyanı yalnızca o turun kaybından gelsin. Birikme bazen
bilerek kullanılır (bellek yetmeyince küçük kümelerin gradyanını toplamak),
ama çoğu zaman unutulmuş bir `zero_grad` hatasıdır.

## `backward` tek sayıdan başlar

`backward()` yalnızca **tek sayılık** (skaler) bir sonuçtan çağrılabilir:

```python
w = torch.tensor([1.0, 2.0], requires_grad=True)
out = w * 3
try:
    out.backward()
except RuntimeError as error:
    print(error)
out.sum().backward()
print(w.grad.tolist())
```

```text
grad can be implicitly created only for scalar outputs
[3.0, 3.0]
```

Kayıp fonksiyonları zaten bütün örneklerin ortalamasını alıp tek sayı
verir. Kendi yazdığın bir hesabın türevini alırken sonu `.sum()` ya da
`.mean()` ile bitir.

## Elle türevle karşılaştırmak

Otomatik türevin doğru olduğunu **sayısal türevle** sınayabiliriz:
`(f(x + h) − f(x − h)) / 2h`. ML Algoritmaları'nda elle yazdığımız geri
hesabı da böyle denetlemiştik.

```python
def f(t):
    return t ** 3 - 2 * t


x = torch.tensor(1.5, dtype=torch.float64, requires_grad=True)
f(x).backward()
h = 1e-4
numeric = (f(1.5 + h) - f(1.5 - h)) / (2 * h)
print(x.grad.item(), round(numeric, 4))
```

```text
4.75 4.75
```

`3x² − 2`, `x = 1,5`'te `6,75 − 2 = 4,75`. İkisi aynı. Fark şu: sayısal
türev her parametre için fonksiyonu iki kez çalıştırır; milyonlarca
parametrede imkânsız. Otomatik türev tek bir geri geçişte hepsini verir.

## Özet

- `requires_grad=True` olan tensörlerle yapılan işlemler hesap grafiğine
  kaydedilir; `backward()` zincir kuralıyla gradyanları hesaplar.
- Gradyan parametrenin `.grad`'ında, parametreyle aynı şekilde durur.
- `backward()` gradyanı ekler; her eğitim turunda `zero_grad` gerekir.
- `backward()` tek sayıdan başlar; kayıp zaten tek sayı.
