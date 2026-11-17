`train_and_test(make_model)` verilen fonksiyonla bir model kursun
(`torch.manual_seed(0)` ile, önce), dersteki gibi eğitsin (yığın 32,
`generator=torch.Generator().manual_seed(0)` ile karıştırma, Adam
`lr=0.005`, 8 tur) ve test doğruluğunu döndürsün. Program aynı fonksiyonla
CNN'i ve MLP'yi karşılaştırır.

**Beklenen çıktı:**

```
True True
True
```
