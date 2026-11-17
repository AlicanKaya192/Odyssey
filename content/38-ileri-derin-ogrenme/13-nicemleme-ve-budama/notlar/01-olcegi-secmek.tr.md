Derste bütün tensör için **tek bir ölçek** seçtik. Satırları çok farklı
büyüklükte olan bir ağırlıkta bu kötüdür: ölçeği en büyük satır belirler,
küçük değerli satırların hepsi birkaç basamağa sıkışır. Çare her satıra
(her çıkış kanalına) **kendi ölçeğini** vermek.

```python
import torch

gen = torch.Generator().manual_seed(0)
w = torch.randn(4, 8, generator=gen) * torch.tensor([[0.1], [1.0], [5.0], [0.5]])


def quantize(w, scale):
    return torch.round(w / scale).clamp(-127, 127) * scale


per_tensor = quantize(w, w.abs().max() / 127)
per_row = quantize(w, w.abs().amax(dim=1, keepdim=True) / 127)
print(bool((w - per_row).abs()[0].max() < (w - per_tensor).abs()[0].max() / 10))
```

```text
True
```

- `w`'nin satırları 0,1 ile 5 arasında farklı ölçeklerde.
- Tek ölçekle ilk satırın (en küçük değerli) hatası, satır başına ölçekle
  olanın on katından büyük.
- Satır başına ölçek her satır için bir sayı daha demek; 64 satırlık bir
  katmanda 64 sayı, ağırlığın yanında önemsiz. Evrişim ve doğrusal
  katmanlarda **kanal başına** nicemleme bu yüzden varsayılandır.

## Sıfır noktası

ReLU'dan sonra etkinlikler hep pozitiftir. Simetrik nicemleme (-127 ile
127) aralığın yarısını, hiç gelmeyecek eksi değerlere ayırır. **Asimetrik**
nicemleme `uint8`'in 0–255 aralığını değerlerin gerçek aralığına yayar ve
gerçek 0'ın hangi tam sayıya düştüğünü bir **sıfır noktası** (zero point)
ile kaydeder: `gerçek = ölçek · (q − sıfır_noktası)`.

```python
a = torch.rand(1000, generator=gen) * 6
symmetric = a.abs().max() / 127
asymmetric = (a.max() - a.min()) / 255
print(bool(asymmetric < symmetric))
```

```text
True
```

Asimetrik ölçek daha küçük, yani basamaklar daha sık: aynı 8 bitle daha az
yuvarlama hatası. Ağırlıklar sıfırın iki yanına dağıldığı için çoğu zaman
simetrik, etkinlikler asimetrik nicemlenir.
