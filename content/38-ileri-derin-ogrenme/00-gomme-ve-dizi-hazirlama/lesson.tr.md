# Gömme Katmanı ve Dizileri Hazırlamak

Şimdiye kadarki ağlar sabit boyutlu girdi alıyordu: 6 özellikli bir tablo
satırı ya da 16×16 bir görüntü. Metin, ses ve sensör kayıtları ise **dizi**
(sequence): öğeleri sırayla gelir ve her örneğin uzunluğu farklıdır. Bu
modülün ilk yarısı dizilerle çalışan ağlar; bu bölüm onların hep aynı olan
ilk adımı: **kelimeyi sayıya, sayıyı vektöre çevirmek** ve farklı
uzunluktaki dizileri tek bir tensöre sığdırmak.

Gömmenin fikri Gömmeler ve Dil Modelleri modülünde anlatıldı: her kelime,
anlamca yakın kelimelerin birbirine yakın düştüğü kısa bir vektörle temsil
edilir ve bu vektörler eğitimle öğrenilir. Orada NumPy ile bir matrisin
satırlarını kendimiz seçiyorduk. PyTorch'ta aynı iş tek bir katman:
`nn.Embedding`.

<figure class="fig">
<div class="flow">
<span class="node">metin</span><span class="arrow">→</span>
<span class="node">kimlikler</span><span class="arrow">→</span>
<span class="node">dolgu</span><span class="arrow">→</span>
<span class="node">nn.Embedding</span><span class="arrow">→</span>
<span class="node acc">(B, T, D)</span>
</div>
<figcaption>Bir dizinin ağa girene kadar geçtiği adımlar. B grup boyu, T en uzun dizinin uzunluğu, D gömme boyutu.</figcaption>
</figure>

## Kelimeden kimliğe

Ağ kelime okumaz, sayı okur. Önce bir **sözlük** (vocabulary) kurarız: her
kelimeye bir tam sayı **kimlik** (id) verilir. İlk iki kimliği iki özel
işarete ayırıyoruz: `<pad>` (dolgu, 0) ve `<unk>` (bilinmeyen kelime, 1).
Neden gerektiklerini birazdan göreceğiz.

```python
from dl_data import TEXT

sentences = [s.split() for s in TEXT.split(".") if s.strip()]
words = sorted({w for s in sentences for w in s})
vocab = ["<pad>", "<unk>"] + words
index = {w: i for i, w in enumerate(vocab)}


def encode(sentence):
    return [index.get(w, 1) for w in sentence]


print(len(sentences), len(vocab))
print(sentences[0])
print(encode(sentences[0]))
```

```text
10 26
['the', 'cat', 'sat', 'on', 'the', 'mat']
[21, 5, 17, 14, 21, 13]
```

- Metinde 10 cümle var; sözlük iki özel işaretle birlikte
  26 kelime.
- `index.get(w, 1)`: sözlükte olmayan kelime `<unk>`'in kimliğini alır.
  Böylece eğitimde hiç görülmemiş bir kelime programı durdurmaz.
- "the" iki kez geçiyor ve iki kez aynı kimliği alıyor: kimlik kelimenin
  kendisine bağlı, yerine değil.

## `nn.Embedding`: kimlikten vektöre

`nn.Embedding(sözlük_boyu, D)` içinde `(sözlük_boyu, D)` boyutlu bir
ağırlık matrisi tutar. Kimlik `i` gelince matrisin `i`. satırını verir. Bu
satırlar sıradan parametrelerdir: geri yayılımda türev alır ve eğitimle
değişir.

```python
import torch
from torch import nn

torch.manual_seed(0)
emb = nn.Embedding(len(vocab), 8)
ids = torch.tensor(encode(sentences[0]))
vectors = emb(ids)
print(ids.shape, ids.dtype)
print(vectors.shape, vectors.dtype)
print(emb.weight.shape, emb.weight.numel())
print(torch.equal(vectors, emb.weight[ids]))
```

```text
torch.Size([6]) torch.int64
torch.Size([6, 8]) torch.float32
torch.Size([26, 8]) 208
True
```

- Girdi **tam sayı** olmalı (`int64`); çıkış `float32`. Kayan noktalı bir
  tensör verirsen katman hata verir.
- Şekil kuralı: girdinin şeklinin sonuna `D` eklenir. 6 kimlik → `(6, 8)`.
  Grup olsaydı `(B, T)` → `(B, T, 8)`.
- Parametre sayısı `sözlük_boyu × D` = 208. Sözlük büyüdükçe
  modelin en büyük katmanı çoğu zaman gömme olur.
- Son satır katmanın sırrını gösteriyor: `emb(ids)` ile `emb.weight[ids]`
  birebir aynı. Gömme katmanı bir **satır seçme** işlemi.

## Neden çarpma değil de seçme?

Kimliği tek-sıcak (one-hot) vektöre çevirip ağırlık matrisiyle çarpmak da
aynı sonucu verir: tek-sıcak vektörde yalnızca bir tane 1 vardır ve çarpım o
satırı seçer.

```python
one_hot = nn.functional.one_hot(ids, num_classes=len(vocab)).float()
print(one_hot.shape, one_hot.sum(dim=1).tolist())
print(torch.allclose(one_hot @ emb.weight, vectors))
```

```text
torch.Size([6, 26]) [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
True
```

Sonuç aynı ama yol pahalı: her kelime için 26 sayılık bir
vektör kurup 26 × 8 çarpma yapıyoruz. Sözlük 50 000 kelime
olunca fark dev olur. `nn.Embedding` doğrudan satırı alır.

## Farklı uzunluklar: dolgu

Bir grup (batch) tek bir tensördür ve tensörün her satırı aynı uzunlukta
olmalı. Cümleler ise 5, 6, 9 kelime. Çözüm **dolgu** (padding): kısa
dizilerin sonuna `<pad>`'in kimliği (0) eklenir, hepsi en uzunun boyuna
gelir. `pad_sequence` bunu yapar.

```python
from torch.nn.utils.rnn import pad_sequence

batch = [torch.tensor(encode(s)) for s in sentences[:3]]
padded = pad_sequence(batch, batch_first=True, padding_value=0)
print([len(b) for b in batch])
print(padded.shape)
print(padded[2].tolist())
```

```text
[6, 6, 5]
torch.Size([3, 6])
[21, 5, 18, 21, 7, 0]
```

- `batch_first=True` şekli `(B, T)` yapar. Yazılmazsa varsayılan `(T, B)`:
  zaman önde. Bu fark bir sonraki bölümde LSTM'de de karşımıza çıkacak.
- Üçüncü cümle 5 kelime; sonuna bir tane `0` eklendi.

## Dolgunun izini sürmek: `padding_idx` ve maske

Dolgu bir hiledir; ağın onu gerçek bir kelime gibi öğrenmesini istemeyiz.
İki araç var:

- `nn.Embedding(..., padding_idx=0)`: 0 kimliğinin vektörü **sıfır** başlar
  ve hiç türev almaz, yani eğitimde de sıfır kalır.
- **Maske** (mask): hangi konumun gerçek, hangisinin dolgu olduğunu söyleyen
  mantıksal tensör, `padded != 0`. Ortalama, toplam ya da dikkat gibi bir
  işlemde dolguyu dışarıda bırakmak için kullanılır.

```python
torch.manual_seed(0)
emb = nn.Embedding(len(vocab), 8, padding_idx=0)
out = emb(padded)
mask = padded != 0
lengths = mask.sum(dim=1)
print(out.shape, mask.dtype, lengths.tolist())
print(out[~mask].abs().sum().item())

mean_all = out.mean(dim=1)
mean_real = (out * mask.unsqueeze(-1)).sum(dim=1) / lengths.unsqueeze(-1)
print(torch.allclose(mean_all[0], mean_real[0]))
print(torch.allclose(mean_all[2], mean_real[2]))
```

```text
torch.Size([3, 6, 8]) torch.bool [6, 6, 5]
0.0
True
False
```

- Dolgu konumlarındaki bütün sayıların toplamı 0: `padding_idx` çalışıyor.
- Ama sıfır vektör de ortalamaya **girer**. İlk cümlede dolgu yok, iki
  ortalama aynı (`True`). Üçüncü cümlede bir dolgu var: düz `mean` 6'ya
  bölüyor, gerçek uzunluk 5; sonuç farklı (`False`). Dolgulu dizide
  ortalamayı maskeyle almak gerekir.
- `mask.unsqueeze(-1)` maskeyi `(B, T)`'den `(B, T, 1)`'e getirir ki
  `(B, T, 8)` ile yayınlanabilsin (yayınlama, Derin Öğrenmenin Temelleri
  modülünde).

Dolgunun gerçekten türev almadığını görelim. Çıkışın toplamının bir
kelimenin satırına türevi, o kelime kaç kez geçtiyse her sütunda o kadardır:

```python
out.sum().backward()
grad = emb.weight.grad
print(grad[0].abs().sum().item())
print(grad[index["the"]].sum().item())
```

```text
0.0
48.0
```

- Dolgu satırı (`0`) sıfır türev aldı: ne kadar dolgu olursa olsun bu satır
  değişmez.
- "the" üç cümlede ikişer kez, toplam 6 kez geçiyor; 8 sütunun her biri 6
  türev alıyor: 6 × 8 = 48.

## DataLoader ile gruplar

`DataLoader` (Derin Öğrenmenin Temelleri modülündeki Dataset ve DataLoader
bölümü) örnekleri varsayılan olarak üst üste koyar; farklı uzunluktaki
dizilerde bu hata verir. Kendi **birleştirme fonksiyonumuzu** (`collate_fn`)
veririz: liste hâlinde gelen örnekleri dolgulayıp tensöre çevirir, gerçek
uzunlukları da yanında döndürür.

```python
from torch.utils.data import DataLoader


def collate(items):
    seqs = [torch.tensor(encode(s)) for s in items]
    lengths = torch.tensor([len(s) for s in seqs])
    return pad_sequence(seqs, batch_first=True), lengths


loader = DataLoader(sentences, batch_size=4, collate_fn=collate)
for x, lengths in loader:
    print(tuple(x.shape), lengths.tolist())
```

```text
(4, 9) [6, 6, 5, 9]
(4, 9) [6, 3, 9, 9]
(2, 9) [7, 9]
```

- Her grubun ikinci boyutu **o grubun** en uzun cümlesi; gruplar arasında
  aynı olması gerekmiyor.
- Uzunlukları saklamak boşuna değil: bir sonraki bölümde LSTM'e dolguyu
  atlatmak için onları kullanacağız.

## Özet

- Dizi hazırlamanın yolu: metin → sözlükle kimlikler → dolgu → gömme →
  `(B, T, D)`.
- `nn.Embedding` bir satır seçme tablosu; tek-sıcak çarpımıyla aynı sonuç,
  çok daha ucuz. Girdi `int64`.
- `<pad>` dolgu, `<unk>` bilinmeyen kelime için. `padding_idx` dolgu
  vektörünü sıfır ve türevsiz tutar.
- Sıfır vektör de ortalamaya girer: dolgulu dizide toplama ve ortalamayı
  maskeyle al.
- Farklı uzunluktaki örnekler için `DataLoader`'a `collate_fn` ver ve
  uzunlukları da döndür.
