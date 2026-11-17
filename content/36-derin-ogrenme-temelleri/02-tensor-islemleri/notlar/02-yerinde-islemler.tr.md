Adı alt çizgiyle biten metotlar (`add_`, `mul_`, `zero_`) tensörü
**yerinde** (in-place) değiştirir: yeni tensör kurmaz, eskisinin içini
yazar.

```python
a = torch.tensor([1.0, 2.0])
b = a
a.add_(10)
print(a.tolist(), b.tolist())
c = a
a = a + 1
print(a.tolist(), c.tolist())
```

```text
[11.0, 12.0] [11.0, 12.0]
[12.0, 13.0] [11.0, 12.0]
```

- `b = a` kopya değil, aynı tensöre ikinci ad. `a.add_(10)` ikisini de
  değiştiriyor.
- `a = a + 1` ise yeni bir tensör kuruyor ve `a` adını ona veriyor; `c`
  eski tensörde kalıyor.
- Yerinde işlem bellek kazandırır ama dikkat ister. Otomatik türev, geri
  yayılım için sakladığı bir değerin yerinde değiştirildiğini fark edince
  hata verir. Kendi kodunda emin değilsen `a = a + 1` biçimini kullan;
  `optimizer.zero_grad()` gibi kütüphane içi yerinde işlemler güvenli.
