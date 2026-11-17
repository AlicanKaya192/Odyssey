`fit(transform)` dersteki deneyi yapsın: `torch.manual_seed(0)` ile dersteki
CNN'i kursun, `Shapes(x_small, y_small, transform)` üzerinde yığın 16,
`generator=torch.Generator().manual_seed(0)` ile karıştırarak Adam
(`lr=0.005`) ile 25 tur eğitsin; sonra artırmasız eğitim resimlerindeki ve
test resimlerindeki doğruluğu döndürsün.

**Beklenen çıktı:**

```
True
True
True
```
