# Dikkat ve Transformer

Gömmeler ve Dil Modelleri modülünde dikkati (attention) ve Transformer
bloğunu NumPy ile sıfırdan kurduk. Kısaca: her konum bir **sorgu** (query)
üretir, bütün konumların **anahtarlarıyla** (key) benzerliğine bakar, bu
benzerlikleri softmax ile ağırlığa çevirir ve konumların **değerlerinin**
(value) ağırlıklı ortalamasını alır. Bütün konumlar aynı anda hesaplanır;
uzak iki kelime tek adımda birbirini görür. Transformer bloğu dikkati, bir
ileri beslemeli ağı, artık bağlantıları ve katman normalizasyonunu üst üste
koyar.

PyTorch'ta bunlar hazır: `nn.MultiheadAttention`,
`F.scaled_dot_product_attention`, `nn.TransformerEncoderLayer`. Bu bölümde
onların biçimlerini, iki maskeyi (dolgu ve gelecek) ve Transformer'ın neden
**konum bilgisine** ihtiyaç duyduğunu görüp sıraya bağlı görevde küçük bir
Transformer eğitiyoruz.

## `nn.MultiheadAttention`

```python
import torch
from torch import nn
import torch.nn.functional as F

torch.manual_seed(0)
attn = nn.MultiheadAttention(embed_dim=8, num_heads=2, batch_first=True)
x = torch.randn(2, 5, 8)
out, weights = attn(x, x, x)
print(out.shape, weights.shape)
print(torch.allclose(weights.sum(dim=-1), torch.ones(2, 5)))
print(sum(p.numel() for p in attn.parameters()))
```

```text
torch.Size([2, 5, 8]) torch.Size([2, 5, 5])
True
288
```

- `attn(x, x, x)`: sorgu, anahtar ve değer aynı diziden; buna **öz
  dikkat** (self-attention) denir. Çeviride sorgu bir diziden, anahtar ve
  değer ötekinden gelebilir.
- `batch_first=True` burada da var; yazılmazsa `(T, B, D)` bekler.
- `weights` `(B, T, T)`: her sorgunun her anahtara verdiği ağırlık, iki
  başın (head) ortalaması. Her satırın toplamı 1.
- Parametreler: Q, K, V ve çıkış için dört `8 × 8` matris ve yanlılıkları,
  `4 × (64 + 8) = 288`. Başlar bu 8 boyutu ikiye bölüyor; baş sayısı
  parametre sayısını değiştirmiyor.

## İçinde ne var?

Dikkatin çekirdeği tek fonksiyon: `F.scaled_dot_product_attention`.
NumPy'de yazdığımız formülle karşılaştıralım.

```python
q, k, v = torch.randn(3, 1, 4, 6).unbind(0)
manual = torch.softmax(q @ k.transpose(-2, -1) / 6 ** 0.5, dim=-1) @ v
print(q.shape)
print(torch.allclose(F.scaled_dot_product_attention(q, k, v), manual, atol=1e-6))
```

```text
torch.Size([1, 4, 6])
True
```

`√d`'ye bölmek (burada `√6`) benzerlikleri küçültür; yoksa büyük boyutta
softmax tek bir konuma yapışır ve türev kaybolur. Hazır fonksiyonun asıl
faydası hız: işlemciye ve donanıma göre en hızlı yolu kendisi seçer.

## Maske 1: dolguyu görmemek

Dolgulu bir dizide sorgular dolgu konumlarına ağırlık vermemeli.
`key_padding_mask` `(B, S)` mantıksal tensör; **`True` "bu anahtarı yok
say"** demek (önceki bölümlerdeki `padded != 0` maskesinin tersi).

```python
ids = torch.tensor([[4, 7, 2, 0, 0], [5, 1, 3, 8, 6]])
pad_mask = ids == 0
out, weights = attn(x, x, x, key_padding_mask=pad_mask)
print(weights[0, :, 3:].abs().sum().item())
print(torch.allclose(weights.sum(dim=-1), torch.ones(2, 5)))
```

```text
0.0
True
```

İlk dizinin son iki konumu dolgu: hiçbir sorgu onlara ağırlık vermedi, toplam
0. Ağırlıklar kalan üç konuma dağıldı; satır toplamları yine 1. PyTorch
maskelenen konuma softmax'tan önce eksi sonsuz yazar, `exp(−∞) = 0`.

## Maske 2: geleceği görmemek

Dil modeli sonraki kelimeyi tahmin ederken sağdaki kelimelere bakarsa hile
yapmış olur. **Nedensel maske** (causal mask) her konumun yalnızca kendisini
ve solundakileri görmesini sağlar. Mantıksal `attn_mask`'ta `True` "bakma"
demek.

```python
causal = torch.triu(torch.ones(5, 5, dtype=torch.bool), diagonal=1)
out, weights = attn(x, x, x, attn_mask=causal)
print(causal[1].tolist())
print(weights[0].triu(diagonal=1).abs().sum().item(), weights[0, 0, 0].item())
```

```text
[False, False, True, True, True]
0.0 1.0
```

- `torch.triu(..., diagonal=1)` köşegenin üstünü `True` yapar: 1. konum
  0 ve 1'i görür, 2, 3, 4'ü görmez.
- Köşegenin üstündeki bütün ağırlıklar 0. İlk konum yalnızca kendisini
  görüyor, ağırlığı tam 1.

## Transformer kodlayıcısı ve konum bilgisi

`nn.TransformerEncoderLayer` bir bloğun tamamı: öz dikkat, ileri beslemeli
ağ, artık bağlantılar, normalizasyon. `nn.TransformerEncoder` blokları üst
üste koyar. Aşağıda dizinin konumlarını karıştırıp (permütasyon) ne olduğuna
bakıyoruz.

```python
torch.manual_seed(0)
layer = nn.TransformerEncoderLayer(d_model=8, nhead=2, dim_feedforward=16,
                                   dropout=0.0, batch_first=True)
encoder = nn.TransformerEncoder(layer, num_layers=2)
encoder.eval()
perm = torch.tensor([4, 2, 0, 1, 3])
with torch.no_grad():
    out = encoder(x)
    out_perm = encoder(x[:, perm])
print(out.shape, sum(p.numel() for p in encoder.parameters()))
print(torch.allclose(out[:, perm], out_perm, atol=1e-5))
```

```text
torch.Size([2, 5, 8]) 1200
True
```

`True`: konumları karıştırınca çıkış da **aynı biçimde** karıştı, başka hiçbir
şey değişmedi. Dikkat bir kümeye bakar gibi bakar; hangi öğenin kaçıncı
sırada olduğunu bilmez. LSTM sırayı okuyarak öğreniyordu; Transformer'a
sırayı **biz vermeliyiz**: her konuma bir **konum gömmesi** (positional
embedding) eklenir. NumPy bölümünde sinüslü konum kodlaması kullanmıştık;
burada öğrenilen bir `nn.Embedding` kullanıyoruz.

## Sıraya bağlı görevde küçük bir Transformer

Dizi sınıflandırma bölümündeki görev: "3'ün hemen ardından 5 var mı?"

```python
from torch.utils.data import TensorDataset, DataLoader
from dl_data import make_sequences


class TinyTransformer(nn.Module):
    def __init__(self, vocab=10, length=12, d=32):
        super().__init__()
        self.tok = nn.Embedding(vocab, d)
        self.pos = nn.Embedding(length, d)
        layer = nn.TransformerEncoderLayer(d, nhead=2, dim_feedforward=32,
                                           dropout=0.0, batch_first=True)
        self.encoder = nn.TransformerEncoder(layer, num_layers=1)
        self.head = nn.Linear(d, 2)

    def forward(self, x):
        positions = torch.arange(x.shape[1])
        h = self.encoder(self.tok(x) + self.pos(positions))
        return self.head(h.max(dim=1).values)


xs, ys = make_sequences(1200, length=12, seed=7)
xs, ys = torch.from_numpy(xs), torch.from_numpy(ys)
loader = DataLoader(TensorDataset(xs[:1000], ys[:1000]), batch_size=32, shuffle=True,
                    generator=torch.Generator().manual_seed(0))
torch.manual_seed(0)
model = TinyTransformer()
opt = torch.optim.Adam(model.parameters(), lr=0.005)
for epoch in range(15):
    model.train()
    for xb, yb in loader:
        opt.zero_grad()
        F.cross_entropy(model(xb), yb).backward()
        opt.step()
model.eval()
with torch.no_grad():
    acc = (model(xs[1000:]).argmax(dim=1) == ys[1000:]).float().mean().item()
print(acc > 0.9)
```

```text
True
```

- `self.tok(x) + self.pos(positions)`: kelime gömmesi ile konum gömmesi
  toplanır; `(12, 32)`'lik konum tensörü gruba yayınlanır.
- Dikkat katmanından sonra her konumun vektörü komşularının bilgisini de
  taşır: "burada 3 var ve hemen sağımda 5 var" bir konumda bir araya
  gelebilir. `h.max(dim=1).values` her özelliğin bütün konumlardaki en
  büyüğünü alır: 1B evrişimdeki havuzlama gibi "herhangi bir yerde var mı?"
  sorusu. Aynı ayarlarla ortalama (`h.mean(dim=1)`) alan sürüm %85'in
  altında kaldı.
- Transformer bu görevde de %90'ı geçti.

## Özet

- `nn.MultiheadAttention(..., batch_first=True)`; öz dikkatte `attn(x, x,
  x)`. Ağırlıklar `(B, T, S)`, satır toplamları 1.
- `key_padding_mask` `(B, S)` ve `attn_mask` `(T, S)` mantıksal maskelerde
  **`True` yok say** demek. Dolgu için ilki, gelecek için `torch.triu(...,
  diagonal=1)`.
- Dikkat sıradan habersiz: konumları karıştırınca çıkış da yalnızca
  karışır. Sıra konum gömmesiyle verilir.
- `nn.TransformerEncoderLayer` + `nn.TransformerEncoder` hazır blok; küçük
  veride `dropout=0.0` ve `eval()` ile denetlemek kolaylaşır.
