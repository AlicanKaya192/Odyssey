# Dizi Sınıflandırma

İlk iki bölümde dizileri hazırlamayı ve LSTM'in biçimlerini gördük. Şimdi
bir ağ eğitiyoruz: bir diziyi okuyup tek bir etiket veren **dizi
sınıflandırıcı** (sequence classifier). Duygu analizi, spam ayıklama, bir
sensör kaydının arızalı olup olmadığı hep bu kalıptır.

Görevi bilerek **sıraya bağlı** seçiyoruz: 0–9 arası 12 sayıdan oluşan
dizilerde "3'ün hemen ardından 5 geliyor mu?" Bir dizide 3 ve 5'in ikisinin
de bulunması yetmez; yan yana ve bu sırada olmaları gerekir. Sırayı göremeyen
bir model burada zorlanmalı.

## Veri

```python
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
from dl_data import make_sequences

x, y = make_sequences(1200, length=12, seed=7)
x, y = torch.from_numpy(x), torch.from_numpy(y)
train = TensorDataset(x[:1000], y[:1000])
x_test, y_test = x[1000:], y[1000:]
print(x.shape, x.dtype)
print(x[0].tolist(), y[0].item())
print(round(y.float().mean().item(), 2))
```

```text
torch.Size([1200, 12]) torch.int64
[9, 6, 6, 8, 5, 7, 8, 2, 0, 3, 2, 8] 0
0.54
```

- Her sayı bir "kelime"; sözlük 10 kimlik. Bu sefer dolgu yok: bütün
  diziler 12 uzunlukta, `make_sequences` öyle üretiyor.
- Etiketlerin yaklaşık yarısı 1: "hep 0 de" diyen bir model %50 civarında
  kalır. Başarıyı buna göre okuyacağız.
- İlk 1000 dizi eğitim, son 200 test.

## Model: gömme → LSTM → doğrusal

```python
class SeqClassifier(nn.Module):
    def __init__(self, vocab=10, dim=8, hidden=16):
        super().__init__()
        self.emb = nn.Embedding(vocab, dim)
        self.lstm = nn.LSTM(dim, hidden, batch_first=True)
        self.head = nn.Linear(hidden, 2)

    def forward(self, x):
        out, (h, c) = self.lstm(self.emb(x))
        return self.head(h[-1])


torch.manual_seed(0)
model = SeqClassifier()
print(model(x[:4]).shape)
print(sum(p.numel() for p in model.parameters()))
```

```text
torch.Size([4, 2])
1778
```

- `h[-1]` son katmanın son gizli durumu `(B, 16)`: dizinin tek vektörlük
  özeti. Doğrusal katman ondan iki sınıfın **logit**'ini (softmax'tan önceki
  ham puanını) çıkarır.
- Çıkış `(4, 2)`: 4 dizi, 2 sınıf. Kayıp `nn.CrossEntropyLoss` softmax'ı
  kendisi uyguladığı için modelin sonunda softmax yok (Derin Öğrenmenin
  Temelleri modülündeki aktivasyon ve kayıp bölümü).

## Eğitim

Eğitim döngüsü tablo verisindekinin aynısı; dizi olması hiçbir şeyi
değiştirmiyor. Tekrar kullanmak için iki küçük fonksiyon yazıyoruz.

```python
def train_model(model, epochs=8, lr=0.01):
    loader = DataLoader(train, batch_size=32, shuffle=True,
                        generator=torch.Generator().manual_seed(0))
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    for epoch in range(epochs):
        model.train()
        for xb, yb in loader:
            opt.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            opt.step()
    return model


def accuracy(model, x, y):
    model.eval()
    with torch.no_grad():
        return (model(x).argmax(dim=1) == y).float().mean().item()


torch.manual_seed(0)
lstm_model = train_model(SeqClassifier())
acc = accuracy(lstm_model, x_test, y_test)
print(round(acc, 2), acc > 0.9)
```

```text
1.0 True
```

LSTM testte %100 doğruluğa ulaştı: deseni öğrendi. Bu
bilgisayarda eğitim birkaç saniye sürdü.

## Sırayı görmeyen bir rakip

Gömmelerin ortalamasını alan bir model (kelime torbası, bag of words) hangi
sayıların bulunduğunu bilir ama sırasını bilmez.

```python
class BagClassifier(nn.Module):
    def __init__(self, vocab=10, dim=8):
        super().__init__()
        self.emb = nn.Embedding(vocab, dim)
        self.head = nn.Linear(dim, 2)

    def forward(self, x):
        return self.head(self.emb(x).mean(dim=1))


torch.manual_seed(0)
bag_model = train_model(BagClassifier())
bag_acc = accuracy(bag_model, x_test, y_test)
print(round(bag_acc, 1), bag_acc < acc)
```

```text
0.8 True
```

Kelime torbası %80 civarında kaldı. "3 ve 5 var mı" sorusunu
öğrenebiliyor (bu yüzden %50'den iyi) ama "3'ten hemen sonra 5" sorusunu
öğrenemiyor.

## Sırayı ters çevirmek

Kanıtı doğrudan görelim: test dizilerini tersine çevirelim. Ters dizide
"3, 5" "5, 3" olur; doğru etiket değişebilir. Kelime torbası için ise ters
dizi aynı dizidir.

```python
x_rev = x_test.flip(dims=[1])
with torch.no_grad():
    bag_same = torch.equal(bag_model(x_test).argmax(1), bag_model(x_rev).argmax(1))
    lstm_same = torch.equal(lstm_model(x_test).argmax(1), lstm_model(x_rev).argmax(1))
print(bag_same, lstm_same)
```

```text
True False
```

- `True`: kelime torbasının 200 tahmininin hepsi ters dizide de aynı.
  Ortalama sıradan bağımsız olduğu için başka türlü olamaz.
- `False`: LSTM ters diziyi başka bir dizi olarak okuyor.

## Özet

- Dizi sınıflandırıcı: `nn.Embedding` → `nn.LSTM` → son durum `h[-1]` →
  `nn.Linear` → logit. Softmax kayıp fonksiyonunun içinde.
- Eğitim döngüsü tablo verisindekinin aynısı; değişen yalnızca modelin
  içi.
- Gömmelerin ortalaması sırayı göremez; sıraya bağlı bir görevde LSTM
  açık ara önde.
- Başarıyı bir taban çizgisiyle (hep aynı sınıfı demek, kelime torbası)
  karşılaştır; tek başına bir yüzde az şey söyler.
