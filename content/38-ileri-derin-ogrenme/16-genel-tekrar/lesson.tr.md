# Genel Tekrar

Diziler, Üretken Modeller ve Dağıtım modülünün sonuna geldin. Kelimeleri ve
sayıları gömme katmanıyla vektöre çevirip dizileri RNN, LSTM, 1B evrişim ve
Transformer ile okuduk. Sonra veri üreten modellere geçtik: otomatik
kodlayıcı, VAE, GAN; etiketsiz öğrenmeyi karşıtlıklı kayıpla, büyük bir
modeli az parametreyle uyarlamayı LoRA ile gördük. Son kısımda eğitilmiş bir
modelin hayatına baktık: hızını ölçmek, dışa aktarmak, küçültmek, sonuçları
tekrarlanabilir kılmak ve bir fonksiyonun arkasında sunmak. Bu bölüm yolu
bir kez daha yürüyor; sonunda parçaların birlikte çalıştığı kısa bir örnek
var.

<figure class="fig">
<div class="flow">
<span class="node">Diziler<br><small>00–06</small></span><span class="arrow">→</span>
<span class="node">Üretken<br><small>07–08</small></span><span class="arrow">→</span>
<span class="node">Az etiket<br><small>09–10</small></span><span class="arrow">→</span>
<span class="node">Dağıtım<br><small>11–14</small></span><span class="arrow">→</span>
<span class="node acc">Proje<br><small>15</small></span>
</div>
<figcaption>Modülün yolu: diziyi oku, veri üret, az etiketle öğren, modeli teslime hazırla, uçtan uca bir algılayıcı kur.</figcaption>
</figure>

## 1. Diziler (Bölüm 0–6)

- **Gömme ve dolgu:** kelime → kimlik → `nn.Embedding`; kısa diziler
  dolgu kimliğiyle uzatılır, `padding_idx` ve maske dolgunun izini sürer
  (00).
- **RNN, LSTM, GRU:** gizli durum dizinin o ana kadarki özeti; LSTM ve GRU
  kapılarla uzun bağımlılığı taşır. `batch_first=True` ile girdi
  `(B, T, D)`; paketli dizi dolguyu atlatır (01).
- **Sınıflandırma ve tahmin:** son gizli durum ya da havuzlama → doğrusal
  katman (02); kayan pencere ve özyinelemeli tahmin, taban çizgisine karşı
  ölçmek (03).
- **1B evrişim:** yerel desenler, alıcı alan, genişletilmiş evrişim;
  çoğu zaman RNN'den hızlı (04).
- **Dil modeli:** sonraki karakteri tahmin, sıcaklıkla örnekleme (05).
- **Dikkat ve Transformer:** sorgu–anahtar–değer, nedensel maske, konum
  gömmesi; `nn.TransformerEncoder` (06).

## 2. Üretken modeller (Bölüm 7–8)

- **Otomatik kodlayıcı:** dar koddan yeniden kurma; yeniden kurma hatası
  anomali ölçüsü (07).
- **VAE:** kod bir dağılım; yeniden parametreleme `z = mu + σ·ε`, kayıp
  yeniden kurma + KL (07).
- **GAN:** iki ağ, iki optimizer; ayırt edicinin adımında `fake.detach()`,
  üreticinin kaybı "sahteye 1 de"; başarı örneklerden ölçülür (08).

## 3. Az etiketle öğrenmek (Bölüm 9–10)

- **Karşıtlıklı öğrenme:** aynı örneğin iki görünümü yakın; NT-Xent,
  sıcaklık; negatifler çöküşü önler (09).
- **LoRA:** taban donmuş, `ΔW = B·A` eğitilir; `r · (giriş + çıkış)`
  parametre, uyarlama takılıp çıkarılır ya da ağırlığa katılır (10).

## 4. Dağıtım (Bölüm 11–14)

- **Performans:** önce ölç, oran karşılaştır; toplu iş, `inference_mode`,
  `autocast`, profil (11).
- **Dışa aktarma:** `torch.export`, serbest grup boyu (`Dim`), `.pt2`
  sınıfsız yüklenir; veriye bağlı dal için `torch.cond` (12).
- **Küçültme:** `int8` nicemleme (4 kat), kanal başına ölçek; budama ve
  yapısal budama (13).
- **Tekrarlanabilirlik ve sunum:** tohumlar, deney kaydı, veri özeti;
  modeli bir kez yükleyen, girdiyi denetleyen tahmin fonksiyonu (14).

## 5. Proje (Bölüm 15)

Sensör arıza algılayıcı: veriyi tanı, basit kuralla taban çizgisi, 1B
evrişimli ağ, kesinlik ve duyarlılık, teslim paketi.

## Hepsi birlikte

Aşağıdaki kısa örnek modülün dört parçasını birleştiriyor: dizileri gömme ve
1B evrişimle okumak (00, 04), tohumla tekrarlanabilir eğitim (14), `int8`
nicemleme (13) ve dışa aktarıp altın çıktıyla denetlemek (12). Görev: 0–9
arası sayı dizilerinde art arda "3, 5" geçiyor mu?

```python
import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_sequences


class Detector(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = nn.Embedding(10, 8)
        self.conv = nn.Conv1d(8, 16, kernel_size=2)
        self.head = nn.Linear(16, 2)

    def forward(self, ids):
        h = self.embed(ids).transpose(1, 2)
        return self.head(torch.relu(self.conv(h)).amax(dim=2))


x_np, y_np = make_sequences(600, seed=7)
x, y = torch.tensor(x_np), torch.tensor(y_np)
torch.manual_seed(0)
model = Detector()
opt = torch.optim.Adam(model.parameters(), lr=0.01)
gen = torch.Generator().manual_seed(1)
for epoch in range(20):
    perm = torch.randperm(500, generator=gen)
    for i in range(0, 500, 50):
        idx = perm[i:i + 50]
        opt.zero_grad()
        F.cross_entropy(model(x[idx]), y[idx]).backward()
        opt.step()
model.eval()


def accuracy(m):
    with torch.no_grad():
        return (m(x[500:]).argmax(1) == y[500:]).float().mean().item()


acc = accuracy(model)
with torch.no_grad():
    for layer in (model.conv, model.head):
        scale = layer.weight.abs().max() / 127
        q = torch.round(layer.weight / scale).clamp(-127, 127).to(torch.int8)
        layer.weight.copy_(q.float() * scale)
batch = torch.export.Dim("batch")
ep = torch.export.export(model, (x[:4],), dynamic_shapes=({0: batch},))
with torch.no_grad():
    golden = model(x[500:])
print(acc > 0.95, abs(accuracy(model) - acc) < 0.02)
print(torch.allclose(ep.module()(x[500:]), golden, atol=1e-5), ep.module()(x[:7]).shape)
```

```text
True True
True torch.Size([7, 2])
```

- `transpose(1, 2)`: gömme `(B, T, D)` verir, `Conv1d` `(B, D, T)` ister.
- Çekirdek boyu 2'lik evrişim art arda iki sayıya bakıyor; `amax(dim=2)`
  desenin dizinin neresinde olduğunu önemsizleştiriyor.
- `int8`'e indirilmiş ağırlıklarla doğruluk yakın kaldı; dışa aktarılan model
  altın çıktıyla aynı ve 7'lik grupta da çalışıyor.

## Sonra

Bu modülde her şeyi küçük, CPU'da saniyeler içinde biten modellerle yaptık.
Gerçek sistemler aynı parçalardan kurulur; fark ölçekte, veride ve donanımda.
Notlarda modülün tek sayfalık özeti ve buradan nereye gidileceği var.
