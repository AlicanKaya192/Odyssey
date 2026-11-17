# Karakter Düzeyinde Dil Modeli

Dil modeli bir dizinin **sonraki öğesini** tahmin eder. Gömmeler ve Dil
Modelleri modülünde kelime düzeyinde n-gram ve NumPy ile bir RNN dil modeli
kurduk, metin üretmeyi ve kod çözme yöntemlerini (açgözlü seçim, sıcaklık,
ışın araması) gördük. Bu bölüm aynı fikri PyTorch'ta **karakter düzeyinde**
kuruyor: sözlük kelimeler değil harfler, yani çok küçük; model kelimeleri
harf harf yazmayı kendisi öğrenmeli.

Bu bölümün PyTorch'a özgü iki dersi var: dil modelinde **her adımın**
çıkışı kullanılır (sınıflandırmada yalnızca son durum kullanılıyordu) ve
kayıp fonksiyonu `(B, T, V)` şekilli çıkışı doğrudan kabul etmez.

## Karakterler ve hedefler

```python
import math

import torch
from torch import nn
from dl_data import TEXT

chars = sorted(set(TEXT))
index = {c: i for i, c in enumerate(chars)}
data = torch.tensor([index[c] for c in TEXT])
T = 32
x = torch.stack([data[i:i + T] for i in range(len(data) - T)])
y = torch.stack([data[i + 1:i + T + 1] for i in range(len(data) - T)])
print(len(TEXT), len(chars), repr("".join(chars[:6])))
print(x.shape, y.shape)
print(torch.equal(x[0, 1:], y[0, :-1]))
```

```text
289 21 ' .abcd'
torch.Size([257, 32]) torch.Size([257, 32])
True
```

- Metin 289 karakter; sözlük boşluk ve nokta dahil
  21 karakter.
- Hedef, girdinin **bir kaydırılmışı**: `y[t] = x[t + 1]`. Son satır bunu
  doğruluyor. Her pencere 32 tahmin içerir; etiketi kimse elle yazmadı,
  metnin kendisinden geliyor (öz denetimli öğrenme, self-supervised
  learning).

## Model: her adımda bir tahmin

```python
class CharLM(nn.Module):
    def __init__(self, vocab, dim=16, hidden=64):
        super().__init__()
        self.emb = nn.Embedding(vocab, dim)
        self.lstm = nn.LSTM(dim, hidden, batch_first=True)
        self.head = nn.Linear(hidden, vocab)

    def forward(self, x, state=None):
        out, state = self.lstm(self.emb(x), state)
        return self.head(out), state


torch.manual_seed(0)
model = CharLM(len(chars))
logits, _ = model(x[:4])
print(logits.shape)
loss = nn.functional.cross_entropy(logits.reshape(-1, len(chars)), y[:4].reshape(-1))
print(abs(loss.item() - math.log(len(chars))) < 0.1)
```

```text
torch.Size([4, 32, 21])
True
```

- `self.head(out)`: doğrusal katman `(B, T, 64)`'ün son boyutuna uygulanır,
  çıkış `(B, T, V)`: her adımda sözlüğün her karakteri için bir logit.
- `cross_entropy` sınıf boyutunu **ikinci** sırada (`(N, V)` ya da
  `(B, V, T)`) bekler. En açık yol iki tensörü düzleştirmek: `(B·T, V)` ve
  `(B·T,)`. `(B, T, V)`'yi olduğu gibi verirsen T'yi sınıf sanar ve hata
  verir (ya da şekiller tesadüfen uyarsa yanlış hesaplar).
- Eğitilmemiş modelin kaybı `log V`'ye yakın: her karaktere aşağı yukarı
  eşit şans.
- `forward` durumu (`state`) da döndürüyor; üretimde lazım olacak.

## Eğitim

```python
opt = torch.optim.Adam(model.parameters(), lr=0.01)
for step in range(150):
    gen = torch.Generator().manual_seed(step)
    batch = torch.randint(0, len(x), (32,), generator=gen)
    logits, _ = model(x[batch])
    flat = logits.reshape(-1, len(chars))
    loss = nn.functional.cross_entropy(flat, y[batch].reshape(-1))
    opt.zero_grad()
    loss.backward()
    opt.step()
print(loss.item() < 1.0)
```

```text
True
```

Her adımda rastgele 32 pencere seçiyoruz (seçim tohumlu, her çalıştırmada
aynı). 150 adım sonra kayıp 1'in altında. Metin çok küçük; model büyük
ölçüde onu **ezberliyor**. Gerçek bir dil modelinde aynı döngü milyonlarca
karakterle döner ve ayrı bir doğrulama metni ezberi ölçer.

## Metin üretmek

Üretimde ağa bir başlangıç verilir, en olası karakter seçilir (açgözlü
seçim) ve **yeniden girdi** yapılır. Her seferinde bütün metni baştan
okutmak yerine LSTM'in durumunu taşıyoruz: ağ yalnızca son karakteri okur.

```python
def generate(model, start, n):
    model.eval()
    text = start
    with torch.no_grad():
        ids = torch.tensor([[index[c] for c in start]])
        logits, state = model(ids)
        for _ in range(n):
            next_id = logits[0, -1].argmax().item()
            text += chars[next_id]
            logits, state = model(torch.tensor([[next_id]]), state)
    return text


print(generate(model, "the c", 20))
print(generate(model, "a bird", 20))
```

```text
the cat saw the dog. the 
a bird sat on the tree. th
```

- Model kelimeleri harf harf yazmayı öğrendi; ürettiği her kelime metinde
  var. Cümleler metindeki cümlelerin parçaları: bu kadar küçük bir metinde
  beklenen bu.
- `state` taşımak, her adımda bütün metni yeniden okutmakla aynı sonucu
  verir ama adım başına tek karakterlik iş yapar (not).

## Özet

- Dil modelinde hedef girdinin bir kaydırılmışı: `y[t] = x[t + 1]`;
  etiket metnin kendisinden gelir.
- Çıkış `(B, T, V)`; kayıp için `(B·T, V)` ve `(B·T,)` olarak düzleştir.
- Eğitilmemiş modelin kaybı `log V` civarında; bu iyi bir ilk denetim.
- Üretimde LSTM'in durumunu taşı, yalnızca son karakteri ver.
