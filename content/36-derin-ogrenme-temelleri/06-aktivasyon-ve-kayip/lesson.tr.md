# Aktivasyon ve Kayıp Fonksiyonları

Bir sinir ağında iki tür fonksiyon seçeriz. **Aktivasyonlar** katmanların
arasına girip ağa doğrusal olmayan bir adım kazandırır. **Kayıp
fonksiyonları** ağın çıktısını gerçek cevapla karşılaştırıp eğitimin
küçültmeye çalıştığı tek sayıyı verir. Bu bölümde ikisini de göreceğiz ve
en sık karışan konuyu açacağız: modelin ham çıktısı (**logits**) ile
olasılıklar (**softmax**) arasındaki fark.

## Aktivasyonlar

En yaygın üç aktivasyonu aynı sayılara uygulayalım:

```python
import torch
from torch import nn

z = torch.tensor([-2.0, -0.5, 0.0, 0.5, 2.0])
for name, fn in [("relu", torch.relu), ("sigmoid", torch.sigmoid), ("tanh", torch.tanh)]:
    print(name, [round(v, 3) for v in fn(z).tolist()])
```

```text
relu [0.0, 0.0, 0.0, 0.5, 2.0]
sigmoid [0.119, 0.378, 0.5, 0.622, 0.881]
tanh [-0.964, -0.462, 0.0, 0.462, 0.964]
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>ReLU</span><span><code>max(0, z)</code>. Gizli katmanlarda varsayılan seçim: basit, hızlı, pozitif tarafta gradyanı hep 1.</span></div>
    <div class="anat-row"><span>Sigmoid</span><span>Her sayıyı 0 ile 1 arasına sıkıştırır. İkili sınıflandırmada çıktıyı olasılığa çevirmek için.</span></div>
    <div class="anat-row"><span>Tanh</span><span>−1 ile 1 arasına sıkıştırır, 0 etrafında simetrik. Tekrarlayan ağlarda sık.</span></div>
  </div>
  <figcaption>Üç aktivasyon ve kullanıldıkları yer.</figcaption>
</figure>

Sigmoid ve tanh büyük sayılarda **doyar**: girdi 5 de olsa 50 de olsa
çıktı neredeyse aynı, gradyanı neredeyse sıfır. Derin ağlarda gradyan
katmanlar boyunca çarpılarak geri aktığı için doyan aktivasyonlar öğrenmeyi
yavaşlatır; gizli katmanlarda ReLU'nun tercih edilmesinin sebebi bu.

## Aktivasyon neden şart?

Aktivasyonsuz iki doğrusal katman, tek bir doğrusal katmandan farksızdır:

```python
torch.manual_seed(0)
first = nn.Linear(4, 8, bias=False)
second = nn.Linear(8, 3, bias=False)
x = torch.randn(5, 4)
combined = second.weight @ first.weight
print(combined.shape, torch.allclose(second(first(x)), x @ combined.T, atol=1e-6))
```

```text
torch.Size([3, 4]) True
```

İki katmanın ağırlıkları tek bir `(3, 4)` matrisle değiştirilebiliyor: ne
kadar katman eklersen ekle, ağ hâlâ bir doğru (düzlem) çizer. Araya giren
ReLU bu çarpımı bozar ve ağa eğri sınırlar çizme gücü verir.

## Logits ve softmax

Sınıflandırma ağının son katmanı her sınıf için bir **ham puan** verir.
Bunlara **logits** denir: herhangi bir gerçek sayı olabilirler, toplamları
1 değildir. Olasılığa çevirmek için **softmax** uygulanır:
`softmax(z)ᵢ = exp(zᵢ) / Σ exp(zⱼ)`.

```python
logits = torch.tensor([[2.0, 1.0, 0.1], [0.5, 2.5, -1.0]])
probs = torch.softmax(logits, dim=1)
print([[round(v, 3) for v in row] for row in probs.tolist()])
print([round(v, 4) for v in probs.sum(dim=1).tolist()])
print(logits.argmax(dim=1).tolist(), probs.argmax(dim=1).tolist())
```

```text
[[0.659, 0.242, 0.099], [0.116, 0.858, 0.026]]
[1.0, 1.0]
[0, 1] [0, 1]
```

- Softmax her satırı toplamı 1 olan olasılıklara çevirdi; büyük logit
  büyük olasılık.
- Sıralamayı değiştirmiyor: logits'in `argmax`'ı ile olasılıkların
  `argmax`'ı aynı. **Yalnızca tahmin gerekiyorsa softmax'a gerek yok.**

<figure class="fig">
  <div class="flow">
    <span class="node">Girdi</span><span class="arrow">→</span>
    <span class="node">Katmanlar</span><span class="arrow">→</span>
    <span class="node acc">Logits<br><small>ham puan</small></span><span class="arrow">→</span>
    <span class="node">softmax<br><small>yalnızca olasılık gerekirse</small></span>
  </div>
  <figcaption>Modelin çıktısı logits'tir. Kayıp fonksiyonu da logits'i alır; softmax'ı sona, yalnızca olasılık göstermek için uygularız.</figcaption>
</figure>

## `CrossEntropyLoss` logits ister

Çok sınıflı sınıflandırmanın kaybı **çapraz entropi**: doğru sınıfın
olasılığının eksi logaritması. PyTorch'un `nn.CrossEntropyLoss`'u softmax'ı
**kendi içinde** yapar; ona logits verilir:

```python
targets = torch.tensor([0, 1])
loss_fn = nn.CrossEntropyLoss()
by_hand = -torch.log(probs[torch.arange(2), targets]).mean()
print(round(loss_fn(logits, targets).item(), 4), round(by_hand.item(), 4))
print(round(loss_fn(probs, targets).item(), 4))
```

```text
0.2851 0.2851
0.725
```

- İlk iki sayı aynı: `CrossEntropyLoss(logits)` = softmax + eksi log +
  ortalama.
- Üçüncüsü yanlış kullanım: olasılıkları vermek. Kayıp yine hesaplanıyor,
  **hata vermiyor**, ama softmax iki kez uygulanmış oluyor ve sayı farklı.
  Model bu şekilde de eğitilir gibi görünür ama daha kötü öğrenir (ilk
  notta neden olduğunu göreceğiz).

Kural: **modelin son katmanında softmax olmaz**; kayıp logits'i alır.
Tahmin için `argmax(logits)`, olasılık göstermek için
`torch.softmax(logits, dim=1)`.

## İkili sınıflandırma: sigmoid ve `BCEWithLogitsLoss`

İki sınıf için çıktı tek bir logit olabilir; sigmoid onu "1 olma
olasılığına" çevirir. Kayıp ikili çapraz entropi. Burada da logits alan
sürüm önerilir:

```python
z = torch.tensor([1.5, -0.5, 3.0])
target = torch.tensor([1.0, 0.0, 0.0])
with_logits = nn.BCEWithLogitsLoss()(z, target)
two_steps = nn.BCELoss()(torch.sigmoid(z), target)
print(round(with_logits.item(), 4), round(two_steps.item(), 4))
```

```text
1.2414 1.2414
```

İkisi aynı sonucu veriyor. `BCEWithLogitsLoss` sigmoid ile logaritmayı tek
formülde birleştirdiği için çok büyük ya da çok küçük logitlerde de
sayısal olarak güvenli. Hedefler burada **ondalık** (`1.0`, `0.0`);
`CrossEntropyLoss`'ta ise sınıf numarası (`int64`).

## Regresyon kayıpları

Sayı tahmininde iki temel kayıp var: ortalama kare hata (`MSELoss`) ve
ortalama mutlak hata (`L1Loss`). Farkları **aykırı değerde** ortaya çıkar:

```python
pred = torch.tensor([2.0, 3.0, 4.0, 5.0])
clean = torch.tensor([2.5, 3.0, 3.5, 5.0])
outlier = torch.tensor([2.5, 3.0, 3.5, 25.0])
for name, fn in [("mse", nn.MSELoss()), ("l1", nn.L1Loss())]:
    print(name, fn(pred, clean).item(), fn(pred, outlier).item())
```

```text
mse 0.125 100.125
l1 0.25 5.25
```

Tek bir aykırı nokta MSE'yi 801 katına çıkarıyor, çünkü 20'lik
hatanın karesi 400. L1 ise yalnızca 21 katına çıkıyor. Aykırı
değerlerin çok olduğu veride L1 (ya da ikisinin arası `SmoothL1Loss`) daha
sakin bir eğitim verir.

## Özet

- Gizli katmanlarda ReLU; aktivasyonsuz katmanlar tek bir doğrusal katmana
  çöker.
- Modelin ham çıktısı **logits**; softmax onu olasılığa çevirir ama
  sıralamayı değiştirmez.
- `CrossEntropyLoss` logits ve sınıf numarası ister; son katmana softmax
  koyma.
- İkili sınıflandırmada `BCEWithLogitsLoss` ve ondalık hedefler.
- Regresyonda MSE aykırı değere çok duyarlı, L1 daha az.
