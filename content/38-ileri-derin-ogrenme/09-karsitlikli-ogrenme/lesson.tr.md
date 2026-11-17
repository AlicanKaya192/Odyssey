# Karşıtlıklı Öğrenme

Etiket pahalıdır; etiketsiz görüntü boldur. **Öz denetimli öğrenmede**
(self-supervised learning) etiket verinin kendisinden çıkarılır. Otomatik
kodlayıcı bunun bir örneğiydi: hedef girdinin kendisi. **Karşıtlıklı
öğrenme** (contrastive learning) başka bir yol izler: aynı görüntünün iki
farklı bozulmuş hâli (iki **görünüm**, view) yakın, farklı görüntülerinkiler
uzak düşsün diye bir kodlayıcı eğitir. Hiç etiket kullanılmaz; yine de
kodlayıcı "kaydırılmış bir kare hâlâ karedir" gibi şeyleri öğrenir.

<figure class="fig">
<div class="flow">
<span class="node">görüntü</span><span class="arrow">→</span>
<span class="node">iki görünüm</span><span class="arrow">→</span>
<span class="node acc">kodlayıcı</span><span class="arrow">→</span>
<span class="node">iki vektör</span><span class="arrow">→</span>
<span class="node ok">yakın olsun</span>
</div>
<figcaption>Aynı görüntünün iki görünümü pozitif çifttir; gruptaki öbür bütün görünümler negatiftir. Kayıp pozitifleri yaklaştırıp negatifleri uzaklaştırır.</figcaption>
</figure>

## Veri ve iki görünüm

`make_shapes` daire, kare ve üçgen görüntüleri veriyor. Etiketleri yalnızca
en sonda, kodlayıcının ne öğrendiğini ölçmek için kullanacağız. Bir görünüm:
görüntüyü 2 piksele kadar kaydırmak, yarı olasılıkla yatay çevirmek,
parlaklığı değiştirmek ve gürültü eklemek.

```python
import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_shapes

x_np, y_np = make_shapes(600, seed=7)
x, y = torch.tensor(x_np), torch.tensor(y_np)
x_train, y_train, x_test, y_test = x[:500], y[:500], x[500:], y[500:]


def augment(batch, gen):
    n = len(batch)
    shifts = torch.randint(-2, 3, (n, 2), generator=gen)
    out = torch.stack([torch.roll(img, (int(a), int(b)), dims=(1, 2))
                       for img, (a, b) in zip(batch, shifts)])
    flip = torch.rand(n, generator=gen) < 0.5
    out[flip] = out[flip].flip(-1)
    out = out * (0.7 + 0.6 * torch.rand(n, 1, 1, 1, generator=gen))
    return (out + 0.1 * torch.randn(out.shape, generator=gen)).clamp(0, 1)


gen = torch.Generator().manual_seed(1)
v1, v2 = augment(x_train[:8], gen), augment(x_train[:8], gen)
print(v1.shape, bool((v1 != v2).any()))
```

```text
torch.Size([8, 1, 16, 16]) True
```

- Aynı 8 görüntüden iki ayrı görünüm grubu çıktı; ikisi farklı.
- Hangi bozulmaların seçildiği, kodlayıcının neye **duyarsız** olacağını
  belirler. Burada konuma, yöne ve parlaklığa duyarsız olsun istiyoruz;
  şekil bilgisi her görünümde korunuyor.

## Kayıp: InfoNCE / NT-Xent

Grupta `n` görüntü var, her birinden iki görünüm: `2n` vektör. Her vektör
için soru şu: öbür `2n − 1` vektörün içinden **kendi eşini** bulabilir mi?
Bu bir sınıflandırma problemi: benzerlikler logit, doğru sınıf eşin sırası.
Kaybın adı InfoNCE; benzerlik kosinüs ve bir **sıcaklıkla** (temperature,
`tau`) bölünürse NT-Xent (normalised temperature-scaled cross-entropy).

```python
def nt_xent(z1, z2, tau=0.1):
    z = F.normalize(torch.cat([z1, z2]), dim=1)
    sim = z @ z.T / tau
    sim.fill_diagonal_(float("-inf"))
    n = len(z1)
    target = torch.cat([torch.arange(n, 2 * n), torch.arange(0, n)])
    return F.cross_entropy(sim, target)


eye = torch.eye(4)
print(round(nt_xent(eye, eye, tau=0.2).item(), 3))
same = torch.ones(4, 4)
collapsed = nt_xent(same, same, tau=0.2).item()
print(round(collapsed, 3), round(torch.log(torch.tensor(7.0)).item(), 3))
```

```text
0.04
1.946 1.946
```

- `F.normalize` her vektörü birim uzunluğa getirir; `z @ z.T` artık kosinüs
  benzerliği tablosu.
- `fill_diagonal_(-inf)`: bir vektörün kendisiyle benzerliği hep en büyük;
  onu adaylardan çıkarıyoruz.
- `target`: ilk yarıdaki `i`'nin eşi `n + i`, ikinci yarıdakinin eşi `i`.
- **Mükemmel durum** (`eye`): her eş birebir aynı, öbürleri dik; kayıp
  sıfıra yakın.
- **Çöküş** (`same`): her vektör aynı. Eş öbürlerinden ayırt edilemez;
  kayıp `log(2n − 1) = log 7`. Otomatik kodlayıcının aksine burada her şeye
  aynı vektörü vermek **kazandırmaz**: negatifler buna izin vermiyor.

## Etiketsiz eğitim

```python
torch.manual_seed(0)
encoder = nn.Sequential(nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                        nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(),
                        nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(32, 16))


def knn_accuracy(enc, queries):
    with torch.no_grad():
        a = F.normalize(enc(x_train), dim=1)
        b = F.normalize(enc(queries), dim=1)
    return (y_train[(b @ a.T).argmax(dim=1)] == y_test).float().mean().item()


queries = augment(x_test, torch.Generator().manual_seed(6))
before = knn_accuracy(encoder, queries)
opt = torch.optim.Adam(encoder.parameters(), lr=0.003)
gen = torch.Generator().manual_seed(1)
for epoch in range(20):
    perm = torch.randperm(500, generator=gen)
    for i in range(0, 500, 100):
        xb = x_train[perm[i:i + 100]]
        loss = nt_xent(encoder(augment(xb, gen)), encoder(augment(xb, gen)))
        opt.zero_grad()
        loss.backward()
        opt.step()
after = knn_accuracy(encoder, queries)
print(round(before, 1), after > before + 0.15)
```

```text
0.5 True
```

- Döngüde `y_train` hiç geçmiyor: kodlayıcı yalnızca "bu iki görünüm aynı
  görüntüden" bilgisiyle eğitildi.
- Ölçü **en yakın komşu doğruluğu**: test görüntüsünün bozulmuş bir
  görünümünü vektöre çevir, eğitim görüntüleri içinde en benzerini bul, onun
  etiketini tahmin say. Etiket yalnızca burada kullanılıyor.
- Rastgele kodlayıcıyla doğruluk yaklaşık 0,5; etiketsiz eğitimden sonra
  belirgin biçimde yüksek (bu bilgisayarda 0,8'in üstünde). Kodlayıcı,
  kaydırılmış ya da çevrilmiş bir şeklin aynı şekil olduğunu etiket görmeden
  öğrendi.

Gerçek kullanımda bu ön eğitim milyonlarca etiketsiz görüntüyle yapılır;
sonra kodlayıcı az etiketle ince ayar ya da doğrusal bir sınıflandırıcı
için hazır bir özellik çıkarıcı olur (Bilgisayarlı Görü modülündeki
özellik çıkarmaya benzer).

## Özet

- Karşıtlıklı öğrenme: aynı örneğin iki görünümü yakın, farklı örneklerinki
  uzak.
- NT-Xent: normalize edilmiş vektörlerin benzerlik tablosu / `tau`,
  köşegen `-inf`, hedef eşin sırası, `cross_entropy`.
- Negatifler çöküşü önler: hepsine aynı vektör kayıp `log(2n − 1)`.
- Hangi bozulmalar seçilirse kodlayıcı onlara duyarsız olur.
- Etiketler yalnızca değerlendirmede (en yakın komşu doğruluğu).
