# Otomatik Kodlayıcı ve VAE

Üretken YZ Temelleri modülünde otomatik kodlayıcıyı (autoencoder) ve
değişimsel otomatik kodlayıcıyı (variational autoencoder, VAE) NumPy ile
kurduk. Kısaca: **kodlayıcı** (encoder) girdiyi birkaç sayılık bir **gizli
koda** (latent code) sıkıştırır, **kod çözücü** (decoder) o koddan girdiyi
yeniden kurmaya çalışır; ağ, yeniden kurma hatasını küçülterek verinin özünü
dar bir yerden geçirmeyi öğrenir. VAE kodu tek bir nokta değil bir
**dağılım** (ortalama ve varyans) olarak üretir; böylece o dağılımdan yeni
kodlar çekip **yeni örnekler** üretebiliriz.

Orada türevleri elle yazmıştık. PyTorch'ta autograd yazıyor; bu bölümün
PyTorch'a özgü dersi VAE'deki **yeniden parametreleme hilesi**
(reparameterization trick): rastgele örneklemenin içinden türev geçirmek.

## Veri: 8×8 rakamlar

```python
import torch
from torch import nn
import torch.nn.functional as F
from sklearn.datasets import load_digits

digits = load_digits()
x = torch.tensor(digits.data / 16.0, dtype=torch.float32)
x_train, x_test = x[:1500], x[1500:]
print(x.shape, x.min().item(), x.max().item())
```

```text
torch.Size([1797, 64]) 0.0 1.0
```

scikit-learn'ün içinde gelen 1797 el yazısı rakam; her biri 64 piksel,
0–16 arası. 16'ya bölüp `[0, 1]`'e getirdik.

## Otomatik kodlayıcı

```python
class AutoEncoder(nn.Module):
    def __init__(self, code=4):
        super().__init__()
        self.encoder = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, code))
        self.decoder = nn.Sequential(nn.Linear(code, 32), nn.ReLU(), nn.Linear(32, 64),
                                     nn.Sigmoid())

    def forward(self, x):
        return self.decoder(self.encoder(x))


def train(model, loss_fn, epochs=30):
    loader = torch.utils.data.DataLoader(x_train, batch_size=64, shuffle=True,
                                         generator=torch.Generator().manual_seed(0))
    opt = torch.optim.Adam(model.parameters(), lr=0.005)
    for epoch in range(epochs):
        model.train()
        for xb in loader:
            opt.zero_grad()
            loss_fn(model, xb).backward()
            opt.step()
    return model.eval()


def ae_loss(model, xb):
    return F.mse_loss(model(xb), xb)


torch.manual_seed(0)
ae = train(AutoEncoder(), ae_loss)
with torch.no_grad():
    code = ae.encoder(x_test)
    err = F.mse_loss(ae(x_test), x_test).item()
baseline = F.mse_loss(x_train.mean(dim=0).expand_as(x_test), x_test).item()
print(code.shape)
print(err < baseline / 2)
```

```text
torch.Size([297, 4])
True
```

- 64 piksel 4 sayıya sıkıştı: `code` `(297, 4)`.
- Son katmandaki `nn.Sigmoid` çıkışı `[0, 1]`'e sıkıştırır; pikseller de bu
  aralıkta.
- Taban çizgisi: her test rakamına eğitimin **ortalama rakamını** demek.
  Otomatik kodlayıcının hatası onun yarısından da az: 4 sayı rakamın
  biçimini taşıyor.
- `DataLoader`'a doğrudan tensör verdik; etiket gerekmiyor, girdi hedefin
  kendisi.

## VAE: kod bir dağılım

VAE'nin kodlayıcısı iki şey üretir: ortalama `mu` ve logaritmik varyans
`logvar`. Kod bu dağılımdan çekilir. Sorun: "rastgele çek" işleminin
türevi yoktur; türev `mu`'ya ve `logvar`'a ulaşamaz. **Yeniden
parametreleme** rastgeleliği dışarı alır: `z = mu + σ · ε`, `ε` standart
normalden. Rastgelelik artık `ε`'da; `mu` ve `σ` sıradan hesabın parçası
ve türev alır.

```python
class VAE(nn.Module):
    def __init__(self, code=4):
        super().__init__()
        self.body = nn.Sequential(nn.Linear(64, 32), nn.ReLU())
        self.mu = nn.Linear(32, code)
        self.logvar = nn.Linear(32, code)
        self.decoder = nn.Sequential(nn.Linear(code, 32), nn.ReLU(), nn.Linear(32, 64),
                                     nn.Sigmoid())

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        return mu + std * torch.randn_like(std)

    def forward(self, x):
        h = self.body(x)
        mu, logvar = self.mu(h), self.logvar(h)
        return self.decoder(self.reparameterize(mu, logvar)), mu, logvar


def kl_term(mu, logvar):
    return -0.5 * torch.mean(torch.sum(1 + logvar - mu ** 2 - logvar.exp(), dim=1))


print(kl_term(torch.zeros(3, 4), torch.zeros(3, 4)).item() + 0.0)
mu = torch.zeros(2, 4, requires_grad=True)
logvar = torch.zeros(2, 4, requires_grad=True)
VAE().reparameterize(mu, logvar).sum().backward()
print(mu.grad.shape, logvar.grad is not None)
```

```text
0.0
torch.Size([2, 4]) True
```

- KL terimi (Kullback–Leibler ıraksaması) kodun dağılımını standart
  normale çeker. Kod zaten standart normalse (`mu = 0`, `logvar = 0`) KL
  tam 0 (`+ 0.0` hesabın verdiği eksi sıfırı `0.0` yazdırır).
- Son satır yeniden parametrelemenin işe yaradığını gösteriyor: rastgele
  çekilmiş `z`'nin toplamından `mu` ve `logvar`'a türev ulaştı.

## VAE'yi eğitmek ve yeni rakam üretmek

```python
def vae_loss(model, xb):
    recon, mu, logvar = model(xb)
    rec = F.binary_cross_entropy(recon, xb, reduction="sum") / len(xb)
    return rec + kl_term(mu, logvar)


torch.manual_seed(0)
vae = train(VAE(), vae_loss)
with torch.no_grad():
    z = torch.randn(5, 4, generator=torch.Generator().manual_seed(1))
    samples = vae.decoder(z)
print(samples.shape, bool(samples.min() >= 0), bool(samples.max() <= 1))
```

```text
torch.Size([5, 64]) True True
```

- Yeniden kurma terimi ikili çapraz entropi: pikseller `[0, 1]`'de olduğu
  için "pikselin açık olma olasılığı" gibi okunabiliyor.
- Üretim için kodlayıcıya hiç gerek yok: standart normalden 5 kod çekip
  **yalnızca kod çözücüden** geçirdik; 5 yeni 64 piksellik görüntü çıktı.
  KL terimi bu yüzden önemli: eğitimde kodlar standart normale yakın
  tutulduğu için oradan çekilen bir kod anlamlı bir rakama düşer.

## Özet

- Otomatik kodlayıcı: kodlayıcı → dar kod → kod çözücü; kayıp yeniden
  kurma hatası, etiket yok.
- VAE kodu dağılım olarak üretir (`mu`, `logvar`); kayıp yeniden kurma + KL.
- Yeniden parametreleme: `z = mu + exp(0.5·logvar) · ε`. Rastgelelik `ε`'ya
  taşınır, türev `mu` ve `logvar`'a ulaşır.
- Üretimde standart normalden kod çek ve yalnızca kod çözücüyü çalıştır.
