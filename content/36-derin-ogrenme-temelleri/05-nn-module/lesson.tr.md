# nn.Module ve Katmanlar

Şimdiye kadar modelleri `nn.Sequential` ile, katmanları art arda dizerek
kurduk. Gerçek PyTorch kodunun çoğunda ise model bir **sınıftır**:
`nn.Module`'den türeyen, katmanlarını `__init__`'te kuran ve hesabı
`forward`'da yazan bir sınıf. Bu bölümde böyle bir sınıf yazacağız, PyTorch'un
parametreleri nasıl bulduğunu göreceğiz ve kısa bir eğitimle sınıfın
çalıştığını sınayacağız.

## İlk model sınıfı

Veri `dl_data.make_table`: 600 satır, 6 özellik, 3 sınıf.

```python
import torch
from torch import nn
from dl_data import make_table


class TableNet(nn.Module):
    def __init__(self, n_features, n_hidden, n_classes):
        super().__init__()
        self.hidden = nn.Linear(n_features, n_hidden)
        self.act = nn.ReLU()
        self.out = nn.Linear(n_hidden, n_classes)

    def forward(self, x):
        h = self.act(self.hidden(x))
        return self.out(h)


torch.manual_seed(0)
model = TableNet(6, 16, 3)
x_np, y_np = make_table(600)
x, y = torch.from_numpy(x_np), torch.from_numpy(y_np)
print(x.shape, y.shape, model(x).shape)
```

```text
torch.Size([600, 6]) torch.Size([600]) torch.Size([600, 3])
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>class TableNet(nn.Module)</code></span><span>Model, PyTorch'un <code>nn.Module</code> sınıfından türüyor.</span></div>
    <div class="anat-row"><span><code>super().__init__()</code></span><span>Ana sınıfı hazırlar; unutulursa katman atarken hata alınır.</span></div>
    <div class="anat-row"><span><code>self.hidden = nn.Linear(...)</code></span><span>Katman özellik olarak atanınca modelin bir parçası olur.</span></div>
    <div class="anat-row"><span><code>def forward(self, x)</code></span><span>Girdiden çıktıya hesap. Geri hesabı yazmıyoruz; otomatik türev yapıyor.</span></div>
    <div class="anat-row"><span><code>model(x)</code></span><span><code>forward</code>'ı çağırır. <code>model.forward(x)</code> yazılmaz.</span></div>
  </div>
  <figcaption>Bir PyTorch modelinin parçaları.</figcaption>
</figure>

`model(x)` yazınca PyTorch `forward`'ı çağırıyor, ama arada kendi işlerini
de yapıyor (ileride göreceğimiz kancalar gibi). Bu yüzden `forward` hiçbir
zaman doğrudan çağrılmaz.

## Parametreler kendiliğinden bulunur

Katmanları `self.` ile atadığımız an `nn.Module` onları ve içlerindeki
parametreleri kaydediyor:

```python
print(model)
for name, p in model.named_parameters():
    print(name, tuple(p.shape), p.requires_grad)
print(sum(p.numel() for p in model.parameters()))
```

```text
TableNet(
  (hidden): Linear(in_features=6, out_features=16, bias=True)
  (act): ReLU()
  (out): Linear(in_features=16, out_features=3, bias=True)
)
hidden.weight (16, 6) True
hidden.bias (16,) True
out.weight (3, 16) True
out.bias (3,) True
163
```

- Parametrelerin adı katmanın özellik adından geliyor: `hidden.weight`,
  `out.bias`.
- Hepsi `requires_grad=True`: `nn.Linear` parametrelerini zaten gradyan
  isteyen tensörler olarak kuruyor.
- `model.parameters()` bu listeyi optimizer'a vermenin yolu:
  `torch.optim.SGD(model.parameters(), ...)`.
- `nn.ReLU`'nun parametresi yok; yine de bir katman olarak listede.

## Sınıfı eğitmek

Model sınıfla yazılmış olsa da eğitim döngüsü değişmiyor:

```python
x_train, y_train, x_test, y_test = x[:480], y[:480], x[480:], y[480:]
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
loss_fn = nn.CrossEntropyLoss()
for epoch in range(200):
    optimizer.zero_grad()
    loss = loss_fn(model(x_train), y_train)
    loss.backward()
    optimizer.step()
with torch.no_grad():
    accuracy = (model(x_test).argmax(dim=1) == y_test).float().mean().item()
print(round(loss.item(), 2), round(accuracy, 2))
```

```text
0.3 0.88
```

Test doğruluğu %88. `make_table`'ın sınıfları bilerek örtüşüyor;
%100 olmuyor. Önemli olan, kendi yazdığımız sınıfın `nn.Sequential` gibi
eğitilebilmesi.

## `forward`'da serbestlik

`nn.Sequential` yalnızca katmanları sırayla uygulayabilir. Sınıfta
`forward` sıradan bir Python fonksiyonu: toplama, `if`, döngü, birden çok
girdi yazabilirsin. Örneğin girdiyi çıktıya ekleyen bir **artık bağlantı**
(residual connection), derin ağların temel taşlarından biri:

```python
class Residual(nn.Module):
    def __init__(self, size):
        super().__init__()
        self.layer = nn.Linear(size, size)

    def forward(self, x):
        return x + torch.relu(self.layer(x))


block = Residual(6)
nn.init.zeros_(block.layer.weight)
nn.init.zeros_(block.layer.bias)
print(block(x[:2]).shape, torch.equal(block(x[:2]), x[:2]))
```

```text
torch.Size([2, 6]) True
```

Katmanın ağırlıkları sıfırken `relu(0) = 0`; blok girdiyi hiç
değiştirmeden geçiriyor (`torch.equal` iki tensörün birebir aynı olduğunu
söylüyor). Artık bağlantı, katman bir şey öğrenmese bile bilginin kaybolmadan
akmasını sağlıyor. Bilgisayarlı Görü modülündeki ResNet bu fikre dayanıyor.

## Eğitim ve değerlendirme kipi

Her modülün bir `training` bayrağı var. Bazı katmanlar (Düzenlileştirme
bölümündeki `Dropout`, Normalizasyon bölümündeki `BatchNorm`) eğitirken ve
tahmin ederken farklı davranır; bayrak onlara hangisinde olduğumuzu söyler:

```python
print(model.training, model.hidden.training)
model.eval()
print(model.training, model.hidden.training)
model.train()
print(model.training)
```

```text
True True
False False
True
```

`model.eval()` bayrağı modelin ve **bütün alt katmanlarının** bayrağını
`False` yapıyor; `model.train()` geri açıyor. Alışkanlık: değerlendirmeden
önce `model.eval()` ve `torch.no_grad()`, eğitime dönerken `model.train()`.

## Özet

- Model `nn.Module`'den türeyen bir sınıf: katmanlar `__init__`'te,
  hesap `forward`'da.
- `self.` ile atanan katmanların parametreleri kendiliğinden kaydedilir;
  `model.parameters()` optimizer'a gider.
- `forward` serbest Python kodu; artık bağlantı gibi yapılar yazılabilir.
- `model.eval()` ve `model.train()` kipi değiştirir.
