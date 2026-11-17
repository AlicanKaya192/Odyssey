Eğitim ve test için **iki ayrı** dönüşüm zinciri kurulur. Ortak olan yalnızca
resmi ağa hazırlayan adımlardır (tür, normalleştirme); rastgele artırma
yalnızca eğitimde.

```python
import torch
from torchvision.transforms import v2

mean, std = 0.2, 0.3
train_tf = v2.Compose([
    v2.RandomHorizontalFlip(),
    v2.RandomCrop(16, padding=3),
    v2.Normalize([mean], [std]),
])
test_tf = v2.Normalize([mean], [std])

img = torch.full((1, 16, 16), 0.5)
torch.manual_seed(0)
print(torch.equal(test_tf(img), test_tf(img)))
print(round(test_tf(img).min().item(), 3), round(train_tf(img).min().item(), 3))
```

```text
True
1.0 -0.667
```

- Test dönüşümü her seferinde aynı sonucu veriyor: ölçüm tekrarlanabilir.
- Eğitim dönüşümündeki kırpma, dolgunun sıfırlarını da resme katıyor
  (normalleştirilince −0,667). Ağ eğitimde bu kenarları görüyor; testte
  görmüyor. Sorun değil: artırma eğitimi zorlaştırıp genellemeyi artırmak için.
- `mean` ve `std` eğitim verisinden bir kez hesaplanır, **iki zincirde de
  aynı sayılar** kullanılır.

| | Eğitim | Doğrulama / test |
|---|---|---|
| Rastgele çevirme, kırpma, döndürme | Evet | Hayır |
| `ToDtype`, `Normalize` | Evet | Evet (aynı sayılarla) |
| `DataLoader(shuffle=...)` | `True` | `False` |
