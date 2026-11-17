Açgözlü seçim hep aynı metni üretir. Çeşitlilik için olasılıklara göre
**örnekleme** yapılır; **sıcaklık** (temperature) bu olasılıkların ne kadar
sivri olacağını ayarlar: logitler sıcaklığa bölünüp softmax alınır. Gömmeler
ve Dil Modelleri modülündeki metin üretimi bölümünde NumPy ile yazılmıştı;
PyTorch'ta aynısı:

```python
import torch

logits = torch.tensor([2.0, 1.0, 0.1])
for temp in (0.5, 1.0, 2.0):
    probs = torch.softmax(logits / temp, dim=0)
    print(temp, [round(p, 2) for p in probs.tolist()])

gen = torch.Generator().manual_seed(0)
probs = torch.softmax(logits, dim=0)
sample = torch.multinomial(probs, num_samples=5, replacement=True, generator=gen)
print(sample.shape, sample.dtype)
```

```text
0.5 [0.86, 0.12, 0.02]
1.0 [0.66, 0.24, 0.1]
2.0 [0.5, 0.3, 0.19]
torch.Size([5]) torch.int64
```

- Düşük sıcaklık (0,5) en olası seçeneği büyütür: davranış açgözlü seçime
  yaklaşır. Yüksek sıcaklık (2) olasılıkları eşitler: metin daha çeşitli
  ama daha hatalı olur.
- `torch.multinomial` olasılıklara göre kimlik çeker; tekrarlanabilir olsun
  diye kendi `Generator`'ünü verdik. Dönen kimlikler `int64`, yani doğrudan
  `nn.Embedding`'e girdi olabilir.

| Yöntem | Üretim | Ne zaman |
|---|---|---|
| Açgözlü (`argmax`) | Hep aynı, tekrara düşebilir | Kısa, tek doğru cevaplı işler |
| Örnekleme, sıcaklık < 1 | Biraz çeşitli, çoğunlukla doğru | Genel metin üretimi |
| Örnekleme, sıcaklık > 1 | Çok çeşitli, sık hatalı | Fikir üretmek, deneme |
