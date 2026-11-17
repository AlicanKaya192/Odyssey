# RNN, LSTM ve GRU

Tekrarlayan sinir ağı (RNN) Gömmeler ve Dil Modelleri modülünün RNN
bölümünde NumPy ile sıfırdan kuruldu. Kısaca: ağ diziyi soldan sağa okur,
her adımda o anki girdiyi ve bir önceki **gizli durumu** (hidden state)
birleştirip yeni gizli durumu hesaplar; her adımda aynı ağırlıklar
kullanılır. Düz RNN'de türev uzun dizilerde kaybolur; LSTM ve GRU bunu
**kapılarla** (gates) çözer. Orada ileri hesabı, zamanda geri yayılımı ve
kapıları elle yazmıştık.

PyTorch'ta üçü de hazır katman: `nn.RNN`, `nn.LSTM`, `nn.GRU`. Geri
yayılımı autograd yapar. Bu bölümde katmanların **girdi ve çıktı
biçimlerini**, parametrelerinin nerede durduğunu ve dolgulu dizilerde nasıl
kullanılacaklarını öğreniyoruz; çoğu hata bu biçimlerin karıştırılmasından
çıkar.

## `nn.RNN`: iki çıkış

```python
import torch
from torch import nn

torch.manual_seed(0)
rnn = nn.RNN(input_size=4, hidden_size=3, batch_first=True)
x = torch.randn(2, 5, 4)
out, h = rnn(x)
print(out.shape, h.shape)
print(torch.allclose(out[:, -1], h[0]))
```

```text
torch.Size([2, 5, 3]) torch.Size([1, 2, 3])
True
```

- Girdi `(B, T, D)`: 2 dizi, 5 adım, her adımda 4 sayı. `batch_first=True`
  yazılmazsa katman `(T, B, D)` bekler ve yanlış eksende okur ama **hata
  vermez**; bu yüzden en sinsi hatalardan biridir.
- `out` **her adımın** gizli durumu: `(B, T, H)`. Her kelime için bir çıktı
  gereken işlerde (etiketleme, dil modeli) bu kullanılır.
- `h` yalnızca **son** adımın gizli durumu: `(katman sayısı, B, H)`. Bütün
  diziyi tek vektörle özetleyen işlerde (sınıflandırma) bu kullanılır.
  `batch_first=True` olsa da `h`'nin ilk boyutu katman; grup ikinci.
- Son satır: son adımın `out`'u ile `h` aynı şey.

## Katmanın içi: aynı formül

`nn.RNN`'in hesapladığı, NumPy'de yazdığımız formülün aynısı. Ağırlıklar
`weight_ih_l0` (girdiden gizliye) ve `weight_hh_l0` (gizliden gizliye)
adlarıyla duruyor; PyTorch iki ayrı yanlılık (bias) tutuyor.

```python
W_ih, W_hh = rnn.weight_ih_l0, rnn.weight_hh_l0
b = rnn.bias_ih_l0 + rnn.bias_hh_l0
h_t = torch.zeros(2, 3)
for t in range(5):
    h_t = torch.tanh(x[:, t] @ W_ih.T + h_t @ W_hh.T + b)
print(W_ih.shape, W_hh.shape)
print(torch.allclose(h_t, h[0], atol=1e-6))
```

```text
torch.Size([3, 4]) torch.Size([3, 3])
True
```

Ağırlıklar `(çıkış, girdi)` biçiminde saklandığı için `.T` ile çarpılıyor;
`nn.Linear`'daki düzenin aynısı. Beş adımlık döngümüz katmanın son gizli
durumunu verdi.

## Üç katman, üç parametre sayısı

```python
def count(m):
    return sum(p.numel() for p in m.parameters())


for cls in (nn.RNN, nn.GRU, nn.LSTM):
    print(cls.__name__, count(cls(4, 3, batch_first=True)))
```

```text
RNN 27
GRU 81
LSTM 108
```

Düz RNN'in bir "kapısı" var: `3×4 + 3×3 + 3 + 3 = 27`. GRU üç parça
hesaplar (sıfırlama kapısı, güncelleme kapısı, aday durum), LSTM dört
(unutma, giriş, çıkış kapıları ve aday hücre): parametre sayısı tam 3 ve 4
katı. Aynı gizli boyutta LSTM daha güçlü ama daha pahalıdır; GRU arada.

## `nn.LSTM`: hücre durumu da döner

LSTM'in gizli durumunun yanında bir de **hücre durumu** (cell state) var:
uzun süreli bellek. Bu yüzden ikinci çıkış bir **demet**.

```python
lstm = nn.LSTM(4, 3, batch_first=True)
out, (h, c) = lstm(x)
print(tuple(out.shape), tuple(h.shape), tuple(c.shape))
print(lstm.weight_ih_l0.shape)
```

```text
(2, 5, 3) (1, 2, 3) (1, 2, 3)
torch.Size([12, 4])
```

- `out, h = lstm(x)` yazarsan `h` bir demet olur ve sonraki satırda
  şaşırtıcı bir hata alırsın: `(h, c)` açılarak yazılır.
- Dört kapının ağırlıkları tek matriste üst üste: `(4 × 3, 4)` = `(12, 4)`.

## Derin ve çift yönlü

`num_layers=2` iki LSTM'i üst üste koyar: ikincisi birincinin `out`'unu
okur. `bidirectional=True` diziyi bir de sağdan sola okuyan ikinci bir LSTM
ekler; her adımın çıktısı iki yönün birleşimidir.

```python
deep = nn.LSTM(4, 3, num_layers=2, bidirectional=True, batch_first=True)
out, (h, c) = deep(x)
print(out.shape, h.shape)
```

```text
torch.Size([2, 5, 6]) torch.Size([4, 2, 3])
```

- `out` son katmanın iki yönü yan yana: `2 × 3 = 6` sayı.
- `h` her katman ve her yön için bir son durum: `2 katman × 2 yön = 4`.
  Sırası `[katman 0 ileri, katman 0 geri, katman 1 ileri, katman 1 geri]`;
  son katmanın iki yönü `h[-2]` ve `h[-1]`.
- Çift yönlü ağ diziyi önceden bütünüyle görmeyi gerektirir. Bütün metin
  elde olan sınıflandırmada işe yarar; bir sonraki kelimeyi tahmin eden dil
  modelinde ise geleceği görmek hile olur.

## Dolgulu dizilerde LSTM

Önceki bölümde kısa dizilere dolgu ekledik. LSTM dolguyu bilmez: dolgu
adımlarını da okur ve son gizli durumu bozar. Aşağıda ikinci dizinin
gerçek uzunluğu 2, sonrası sıfır dolgu.

```python
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

torch.manual_seed(1)
x = torch.randn(2, 5, 4)
x[1, 2:] = 0
lengths = torch.tensor([5, 2])
out, (h, c) = lstm(x)
print(torch.allclose(h[0, 1], out[1, 1]))

packed = pack_padded_sequence(x, lengths, batch_first=True, enforce_sorted=False)
out_p, (h_p, c_p) = lstm(packed)
print(torch.allclose(h_p[0, 1], out[1, 1]))

padded, lens = pad_packed_sequence(out_p, batch_first=True)
print(padded.shape, lens.tolist(), padded[1, 2:].abs().sum().item())
```

```text
False
True
torch.Size([2, 5, 3]) [5, 2] 0.0
```

- İlk satır `False`: dolgusuz çalıştırmada ikinci dizinin son gizli durumu,
  onun gerçek son adımındaki (`out[1, 1]`) durumla aynı değil. Üç sıfır
  adım durumu değiştirdi. Sıfır girdi "hiçbir şey" demek değil; ağ yine
  ağırlık ve yanlılıkla hesaplar.
- **Paketlemek** (`pack_padded_sequence`) her dizinin uzunluğunu katmana
  söyler; katman her diziyi kendi sonunda durdurur. İkinci satır `True`:
  paketli çalıştırmanın son durumu gerçek son adımın durumu.
- `enforce_sorted=False` dizilerin uzunluğa göre sıralı olmasını istemez
  (sıralamayı kendisi yapar ve geri alır).
- `pad_packed_sequence` paketli çıktıyı yeniden dolgulu tensöre çevirir;
  dolgu konumları sıfır.

## Özet

- `nn.RNN`, `nn.GRU`, `nn.LSTM`: girdi `(B, T, D)` için `batch_first=True`
  yaz; yazmazsan hata yok, yanlış sonuç var.
- `out` her adımın durumu `(B, T, H × yön)`; `h` son durum
  `(katman × yön, B, H)`. LSTM ikinci çıkışta `(h, c)` demeti döndürür.
- Parametre sayısı RNN'in 3 (GRU) ve 4 (LSTM) katı.
- Dolgulu dizide son durum için `pack_padded_sequence(...,
  enforce_sorted=False)`; ya da son gerçek adımın `out`'unu kendin seç
  (not).
