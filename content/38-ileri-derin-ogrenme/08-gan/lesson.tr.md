# Çekişmeli Üretici Ağlar (GAN)

Üretken YZ Temelleri modülünde GAN'ı (generative adversarial network) NumPy
ile kurduk. Kısaca: iki ağ birbirine karşı oynar. **Üretici** (generator)
rastgele bir gürültüden örnek üretir; **ayırt edici** (discriminator) bir
örneğe bakıp "gerçek mi" diye bir olasılık söyler. Ayırt edici ikisini
ayırmayı, üretici onu kandırmayı öğrenir; oyun dengeye gelince üretilen
örnekler gerçeklerden ayırt edilemez olur.

<figure class="fig">
<div class="flow">
<span class="node">gürültü z</span><span class="arrow">→</span>
<span class="node acc">üretici G</span><span class="arrow">→</span>
<span class="node">sahte örnek</span><span class="arrow">→</span>
<span class="node ok">ayırt edici D</span><span class="arrow">→</span>
<span class="node">gerçek mi?</span>
</div>
<figcaption>Ayırt ediciye sırayla gerçek ve sahte örnekler gösterilir. Üretici gerçek veriyi hiç görmez; ne öğrenirse ayırt edicinin tepkisinden öğrenir.</figcaption>
</figure>

Orada iki ağın türevlerini elle yazmıştık. PyTorch'ta autograd yazıyor; bu
bölümün asıl konusu PyTorch'a özgü üç şey: **iki ayrı optimizer**,
`detach()` ile türevin nereye gideceğini seçmek ve eğitim adımlarının
sırası.

## Veri ve iki ağ

Hedefimiz basit: ortalaması 3, standart sapması 0,5 olan sayılar üretmek.
Tek boyutlu veri, ne öğrenildiğini tek bir sayıyla görmemizi sağlıyor.

```python
import torch
from torch import nn

torch.manual_seed(0)
real = 3 + 0.5 * torch.randn(2000, 1, generator=torch.Generator().manual_seed(1))
G = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 1))
D = nn.Sequential(nn.Linear(1, 16), nn.LeakyReLU(0.2), nn.Linear(16, 1))
z = torch.randn(64, 4)
print(G(z).shape, D(G(z)).shape)
print(sum(p.numel() for p in G.parameters()), sum(p.numel() for p in D.parameters()))
print(round(real.mean().item(), 1), round(real.std().item(), 1))
```

```text
torch.Size([64, 1]) torch.Size([64, 1])
97 49
3.0 0.5
```

- Üretici 4 sayılık gürültüyü tek sayıya çeviriyor; ayırt edici tek sayıyı
  tek bir puana (logit) çeviriyor.
- Ayırt edicinin sonunda `Sigmoid` yok: kaybı `nn.BCEWithLogitsLoss` ile
  hesaplayacağız, o sigmoid'i kendi içinde ve sayısal olarak daha güvenli
  biçimde uyguluyor.
- Ayırt edicide `LeakyReLU`: eksi tarafta da küçük bir eğim bırakır, türev
  üreticiye kesilmeden ulaşsın diye GAN'larda yaygındır.

## `detach`: türev nereye gitsin?

Ayırt ediciyi eğitirken sahte örneği ona "0" etiketiyle gösteririz. Ama bu
adımda **yalnızca ayırt edici** değişmeli; türevin üreticiye kadar gitmesi
hem boşa hesap hem de yanlış: üretici "daha kolay yakalanayım" yönünde
türev biriktirir. `fake.detach()` sahte örneği hesap grafiğinden koparır.

```python
loss_fn = nn.BCEWithLogitsLoss()
fake = G(z)
d_loss = loss_fn(D(fake.detach()), torch.zeros(64, 1))
d_loss.backward()
print(G[0].weight.grad is None, D[0].weight.grad is not None)
D.zero_grad()
loss_fn(D(fake), torch.zeros(64, 1)).backward()
print(G[0].weight.grad is None)
```

```text
True True
False
```

- `detach` ile: üreticinin ağırlığında türev yok (`None`), ayırt edicide
  var.
- `detach` olmadan aynı kayıp üreticiye de türev yazdı.

## Eğitim döngüsü

Her adımda iki iş sırayla yapılır:

1. **Ayırt edici:** gerçeklere "1", sahtelere (koparılmış) "0" der; yalnızca
   `opt_d` adım atar.
2. **Üretici:** aynı sahteleri bu kez **koparmadan** ayırt ediciye gösterir
   ve etiket olarak "1" ister: "beni gerçek san". Yalnızca `opt_g` adım
   atar.

```python
def train_gan(G, D, steps=1500, lr=0.002):
    opt_g = torch.optim.Adam(G.parameters(), lr=lr, betas=(0.5, 0.999))
    opt_d = torch.optim.Adam(D.parameters(), lr=lr, betas=(0.5, 0.999))
    gen = torch.Generator().manual_seed(2)
    ones, zeros = torch.ones(64, 1), torch.zeros(64, 1)
    for step in range(steps):
        xb = real[torch.randint(0, len(real), (64,), generator=gen)]
        fake = G(torch.randn(64, 4, generator=gen))
        opt_d.zero_grad()
        d_loss = loss_fn(D(xb), ones) + loss_fn(D(fake.detach()), zeros)
        d_loss.backward()
        opt_d.step()
        opt_g.zero_grad()
        loss_fn(D(fake), ones).backward()
        opt_g.step()


def samples(G):
    with torch.no_grad():
        return G(torch.randn(2000, 4, generator=torch.Generator().manual_seed(3)))


print(abs(samples(G).mean().item() - 3) < 0.2)
train_gan(G, D)
s = samples(G)
print(abs(s.mean().item() - 3) < 0.2)
print(abs(torch.sigmoid(D(s)).mean().item() - 0.5) < 0.05)
```

```text
False
True
True
```

- Eğitimden önce üretilen sayıların ortalaması 3'ten uzak; sonra 0,2'den
  yakın.
- Son satır dengeyi gösteriyor: ayırt edici üretilen örneklere ortalama
  olarak yaklaşık 0,5 diyor, yani artık yazı tura atıyor.
- Üreticinin adımında `D(fake)` ayırt edicinin ağırlıklarına da türev
  yazıyor; zararı yok, çünkü o ağırlıklar `opt_d` ile değişiyor ve bir
  sonraki adımda `opt_d.zero_grad()` onları siliyor. Yanlış olan, üreticinin
  adımında `opt_d.step()` çağırmak olurdu.
- `betas=(0.5, 0.999)`: Adam'ın momentumunu biraz kısmak GAN'larda yaygın
  bir ayardır; iki ağ sürekli birbirine göre değiştiği için uzun hafıza
  salınımı büyütür.

Ortalama her denemede 3'e yaklaşıyor ama standart sapma tohuma göre
belirgin biçimde değişiyor (bu bilgisayarda beş tohumda 0,3 ile 0,8
arasında). GAN dağılımın tamamını değil, ayırt ediciyi kandırmaya yetecek
kadarını öğrenir; notlarda bunun en bilinen sonucu olan mod çöküşüne
bakacağız.

## Özet

- GAN: üretici gürültüden örnek üretir, ayırt edici gerçeği sahteden ayırır.
- PyTorch'ta iki ağ, iki optimizer; her adımda önce ayırt edici, sonra
  üretici.
- Ayırt edicinin adımında `fake.detach()`: türev üreticiye gitmez.
- Üreticinin kaybı "sahteye 1 de" (`BCEWithLogitsLoss(D(fake), ones)`).
- Başarı kayıptan değil üretilen örneklerden ölçülür.
