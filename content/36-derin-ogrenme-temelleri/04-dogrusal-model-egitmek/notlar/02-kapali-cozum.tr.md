Doğrusal regresyonun gradyan inişi gerektirmeyen bir **kapalı çözümü**
var: en küçük kareler (least squares). Makine öğrenmesi patikasındaki
`LinearRegression` bunu kullanıyordu. PyTorch'ta `torch.linalg.lstsq`:

```python
A = torch.stack([x, torch.ones_like(x)], dim=1)
solution = torch.linalg.lstsq(A, y.unsqueeze(1)).solution
print(A.shape, [round(v, 2) for v in solution.flatten().tolist()])
```

```text
torch.Size([100, 2]) [2.99, 2.0]
```

- `A`'nın ilk sütunu `x`, ikincisi hep 1: ikinci sütunun katsayısı sabit
  `b` oluyor.
- Sonuç dersteki gradyan inişinin bulduğuyla aynı yerde: `w ≈ 3`, `b ≈ 2`.

Peki neden gradyan inişi? Kapalı çözüm yalnızca doğrusal modelde ve
kayıp ortalama kare hatayken var. Araya bir ReLU girdiği anda formül
kalmıyor; derin öğrenmede tek yol adım adım aramak. Bu bölümde doğrusal
modeli seçtik, çünkü gradyan inişinin bulduğunu kesin cevapla
karşılaştırabiliyoruz.
