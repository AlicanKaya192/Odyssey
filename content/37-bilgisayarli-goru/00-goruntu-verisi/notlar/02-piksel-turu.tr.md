`uint8` pikseller üç yerde sessiz ya da beklenmedik davranıyor:

```python
import torch

x = torch.tensor([10, 250], dtype=torch.uint8)
print((x - 20).tolist())
try:
    x.mean()
except RuntimeError as error:
    print(type(error).__name__)
print(x.float().mean().item())
print((x.to(torch.int16) - 20).tolist())
```

```text
[246, 230]
NotImplementedError
130.0
[-10, 230]
```

- **Çıkarma başa sarıyor:** `10 − 20` eksi olamadığı için 246 oluyor. Hata
  yok. Parlaklık farkı, kenar gibi hesaplardan önce türü değiştir.
- **Ortalama hata veriyor:** `mean` tam sayı türünde çalışmıyor
  (`NotImplementedError`; `RuntimeError`'ın bir alt türü olduğu için
  `except RuntimeError` onu da yakalıyor). Önce `float()`.
- **Daha geniş tür:** `int16` eksi değerleri de tutuyor; ama ağa vermeden
  önce yine `float32` gerekir.

Kural: dosyadan okuduğun resmi ilk iş `float32`'ye çevir ve [0, 1]'e ölçekle;
geri kalan bütün hesabı orada yap. Kaydederken `uint8`'e dönmeden önce
değerleri `clamp(0, 1)` ile sınırla, yoksa 1'i aşan değerler de başa sarar.
