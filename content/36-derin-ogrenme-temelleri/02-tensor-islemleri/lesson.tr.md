# Tensör İşlemleri ve Yayınlama

Bir sinir ağının içinde olan biten, tensörler üzerinde birkaç tür işlemden
ibaret: eleman eleman aritmetik, matris çarpımı, toplama/ortalama gibi
**indirgemeler** (reduction) ve farklı şekilli tensörleri birlikte işlemeye
yarayan **yayınlama** (broadcasting). Bu bölümde bu dördünü görüp sonunda
`nn.Linear` katmanını tek satırlık bir matris çarpımıyla yeniden yazacağız.

## Eleman eleman işlemler

`+`, `-`, `*`, `/`, `**` aynı şekilli iki tensörde karşılıklı elemanlar
arasında çalışır:

```python
import torch

a = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
b = torch.tensor([[10.0, 20.0], [30.0, 40.0]])
print((a + b).tolist())
print((a * b).tolist())
print((a ** 2).tolist(), torch.sqrt(a)[1, 1].item())
```

```text
[[11.0, 22.0], [33.0, 44.0]]
[[10.0, 40.0], [90.0, 160.0]]
[[1.0, 4.0], [9.0, 16.0]] 2.0
```

`a * b` **matris çarpımı değil**: aynı yerdeki elemanları çarpıyor. `torch`
içinde `sqrt`, `exp`, `log`, `abs` gibi fonksiyonlar da her elemana ayrı ayrı
uygulanıyor.

## Matris çarpımı

Matris çarpımı `@` işaretiyle (ya da `torch.matmul`) yazılır. `(a, b)`
şekilli bir matris `(b, c)` şekilli bir matrisle çarpılabilir; sonuç
`(a, c)`:

```python
x = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
w = torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
print(x.shape, w.shape, (x @ w).shape)
print((x @ w).tolist())
```

```text
torch.Size([2, 3]) torch.Size([3, 2]) torch.Size([2, 2])
[[4.0, 5.0], [10.0, 11.0]]
```

Sonucun her elemanı bir satır ile bir sütunun **nokta çarpımı**: ilk satır
`[1, 2, 3]` ile ilk sütun `[1, 0, 1]` → `1 + 0 + 3 = 4`. Sinir ağlarının
işinin büyük kısmı bu çarpım.

## İndirgemeler ve `dim`

`sum`, `mean`, `max` bir tensörü küçültür. Hangi boyut boyunca
indirgeneceğini `dim` söyler:

```python
t = torch.tensor([[1.0, 5.0, 3.0], [4.0, 2.0, 6.0]])
print(t.sum().item(), t.sum(dim=0).tolist(), t.sum(dim=1).tolist())
print(t.mean(dim=1, keepdim=True).shape)
values, indices = t.max(dim=1)
print(values.tolist(), indices.tolist(), t.argmax(dim=1).tolist())
```

```text
21.0 [5.0, 7.0, 9.0] [9.0, 12.0]
torch.Size([2, 1])
[5.0, 6.0] [1, 2] [1, 2]
```

<figure class="fig">
  <div class="versus">
    <div><h5><code>dim=0</code></h5>Satırlar boyunca indirger: her <b>sütun</b> için bir sonuç. <code>(2, 3)</code> → <code>(3,)</code></div>
    <div><h5><code>dim=1</code></h5>Sütunlar boyunca indirger: her <b>satır</b> için bir sonuç. <code>(2, 3)</code> → <code>(2,)</code></div>
  </div>
  <figcaption><code>dim</code> "yok edilecek boyut" diye okunur: o boyut sonuçta kalmıyor.</figcaption>
</figure>

- `keepdim=True` indirgenen boyutu 1 uzunlukta bırakıyor: `(2, 3)` →
  `(2, 1)`. Sonucu yeniden ilk tensörle işleme sokarken işe yarıyor.
- `max(dim=1)` iki şey döndürüyor: en büyük değerler ve yerleri. Yalnızca
  yer gerekiyorsa `argmax`.

## Yayınlama

Farklı şekilli iki tensörü toplamak da mümkün. PyTorch küçük olanı
**yayınlar** (broadcasting): eksik ya da 1 uzunluklu boyutlarda kopyalanmış
gibi davranır, ama gerçekten kopyalamaz.

```python
m = torch.tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
print((m + torch.tensor([10.0, 100.0])).tolist())
col = torch.tensor([[1.0], [2.0], [3.0]])
row = torch.tensor([[10.0, 20.0, 30.0, 40.0]])
print(col.shape, row.shape, (col + row).shape)
try:
    m + torch.tensor([1.0, 2.0, 3.0])
except RuntimeError as error:
    print(str(error).replace(" at ", "\nat "))
```

```text
[[11.0, 102.0], [13.0, 104.0], [15.0, 106.0]]
torch.Size([3, 1]) torch.Size([1, 4]) torch.Size([3, 4])
The size of tensor a (2) must match the size of tensor b (3)
at non-singleton dimension 1
```

Kural, şekilleri **sağdan** başlayarak karşılaştırmak: her boyutta iki
uzunluk ya eşit olmalı ya da biri 1 (ya da hiç olmamalı).

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>(3, 2) + (2,)</code></span><span>Sağdaki 2 ile 2 eşit; eksik boyut 1 sayılır → <code>(3, 2)</code></span></div>
    <div class="anat-row"><span><code>(3, 1) + (1, 4)</code></span><span>1 olanlar uzar → <code>(3, 4)</code></span></div>
    <div class="anat-row"><span><code>(3, 2) + (3,)</code></span><span>Sağdaki 2 ile 3 uyuşmuyor → hata</span></div>
  </div>
  <figcaption>Yayınlama kuralı: sağdan hizala, her boyut eşit ya da 1.</figcaption>
</figure>

Hata mesajı uyuşmayan boyutu söylüyor: 1 numaralı boyutta (sütunlar) 2
ile 3. Satır başına
bir değer eklemek istiyorsan değeri sütun şekline getir: `(3,)` yerine
`(3, 1)`.

## Uygulama: sütunları ölçeklemek

Makine öğrenmesi patikasında `StandardScaler` her özelliği ortalaması 0,
standart sapması 1 olacak şekilde ölçekliyordu. Yayınlamayla tek satır:

```python
from dl_data import make_table

x_np, y_np = make_table(600)
x = torch.from_numpy(x_np)
scaled = (x - x.mean(dim=0)) / x.std(dim=0)
print(x.shape, x.mean(dim=0).shape)
print(scaled.mean(dim=0).abs().max().item() < 1e-5)
print(torch.allclose(scaled.std(dim=0), torch.ones(6)))
```

```text
torch.Size([600, 6]) torch.Size([6])
True
True
```

`x.mean(dim=0)` her sütunun ortalaması, şekli `(6,)`; `(600, 6)` şekilli
`x`'ten çıkarılırken her satıra yayınlanıyor. Ölçeklenmiş verinin
ortalaması sıfıra çok yakın, standart sapması 1.

## `nn.Linear` aslında ne yapıyor?

Giriş bölümündeki `nn.Linear(64, 32)` katmanı, bir matris çarpımı artı bir
yayınlanmış toplamadan ibaret: `x @ W.T + b`.

```python
torch.manual_seed(0)
layer = torch.nn.Linear(6, 3)
by_hand = x @ layer.weight.T + layer.bias
print(layer.weight.shape, layer.bias.shape)
print(by_hand.shape, torch.allclose(layer(x), by_hand))
```

```text
torch.Size([3, 6]) torch.Size([3])
torch.Size([600, 3]) True
```

- Ağırlık `(çıktı, girdi)` = `(3, 6)` şeklinde saklanıyor; bu yüzden
  transpozu (`W.T`, `(6, 3)`) ile çarpılıyor: `(600, 6) @ (6, 3)` →
  `(600, 3)`.
- Sabit `b` `(3,)` şeklinde ve 600 satırın her birine yayınlanıyor.
- `torch.allclose` iki tensörün (küçük yuvarlama farkları dışında) aynı
  olduğunu söylüyor. Katman bizim yazdığımızla birebir aynı hesabı yapıyor.

## Özet

- `*` eleman eleman, `@` matris çarpımı. `(a, b) @ (b, c)` → `(a, c)`.
- `dim` indirgenecek (sonuçtan kalkacak) boyut; `keepdim=True` onu 1
  uzunlukta bırakır.
- Yayınlama: şekiller sağdan hizalanır, her boyut eşit ya da 1 olmalı.
- `nn.Linear` = `x @ W.T + b`.
