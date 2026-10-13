Zamanda geri yayılımda türev her adımda bir kez daha `W_h` ve `tanh`'ın
türeviyle çarpılır. 40 adım geriye gitmek, 40 çarpan demek. Bu çarpanlar
ortalamada birden küçükse türev **kaybolur** (vanishing gradient), büyükse
**patlar** (exploding gradient). Rastgele ağırlıklı bir RNN'de ölçelim:

```python
import numpy as np

H = 32
for scale in [0.1, 0.25, 0.5]:
    rng = np.random.default_rng(0)
    Wh = rng.normal(0, scale, (H, H))
    hs = [np.zeros(H)]
    for t in range(40):
        hs.append(np.tanh(rng.normal(0, 1, H) + hs[-1] @ Wh))
    dh = np.ones(H)
    norms = []
    for t in reversed(range(1, 41)):
        norms.append(np.linalg.norm(dh))
        dh = Wh @ ((1 - hs[t] ** 2) * dh)
    print(scale, " ".join(f"{norms[k]:.0e}" for k in [0, 10, 20, 30, 39]))
```

```text
0.1 6e+00 1e-04 2e-09 7e-14 4e-18
0.25 6e+00 5e-01 2e-02 3e-03 8e-04
0.5 6e+00 4e+01 3e+02 1e+03 6e+02
```

Sütunlar sondan 0, 10, 20, 30 ve 39 adım gerideki türevin büyüklüğü.

- Küçük ağırlıklarla (0,1) türev 6'dan 10 adımda 0,0001'e, 39 adımda
  10⁻¹⁸'e iniyor: 40 kelime önceki bir kelimeden hiçbir şey öğrenilemez.
- Büyük ağırlıklarla (0,5) türev yüz kattan fazla büyüyor; tek bir
  güncelleme ağırlıkları bozabilir.
- Patlamanın çaresi derste kullandığımız **türev kırpma**. Kaybolmanın
  çaresi o kadar basit değil: ağın yapısını değiştirmek gerekiyor. LSTM ve
  GRU bunun için tasarlandı (ikinci not).
- Derste cümleler en fazla 11 kelime olduğu için kaybolma sorun olmadı.
  Gerçek metinlerde bir paragrafın başındaki özne, sonundaki zamirden onlarca
  kelime uzakta olabilir.
