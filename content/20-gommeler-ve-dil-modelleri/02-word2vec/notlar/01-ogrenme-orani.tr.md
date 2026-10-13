Dersteki `train` fonksiyonunu üç öğrenme oranıyla, üçer turla çalıştıralım:

```python
for lr in [0.01, 0.05, 0.1]:
    with np.errstate(all="ignore"):
        _, _, losses = train(lr=lr, epochs=3)
    print(lr, losses)
```

```text
0.01 [2.138, 1.5, 1.45]
0.05 [2.351, 1.835, 1.506]
0.1 [nan, nan, nan]
```

- 0,1'de kayıp ilk turdan `nan` (not a number, "sayı değil"). Adımlar o kadar
  büyük ki vektörlerin nokta çarpımları büyüyüp `exp` taşıyor (sonsuz),
  sonsuzdan sonsuz çıkınca `nan` oluyor ve `nan` bütün tabloya yayılıyor.
  Bir kez `nan` olan model bir daha düzelmez.
- `np.errstate(all="ignore")` NumPy'nin taşma uyarılarını susturuyor;
  burada çıktıyı kısa tutmak için kullandık. Gerçek işte uyarıyı
  susturmak yerine okumak gerekir: "overflow encountered in exp" bir
  öğrenme oranı sorunu işaretidir.
- 0,01 bu küçük veride üç turda 0,05'ten bile düşük kayba indi. Daha büyük
  oran her zaman daha hızlı öğrenmek demek değil.

## Pratikte

- Öğrenme oranı bir ayar; birkaç değer deneyip kaybın eğrisine bak.
- İlk turdaki kayıp, başlangıçtaki kayıptan (her olasılık 0,5:
  `6 · log 2 ≈ 4,16`) düşük olmalı. Değilse ya oran çok büyük ya da kodda
  bir türev hatası var.
- Word2Vec'in kendi kodu da öğrenme oranını eğitim boyunca doğrusal
  azaltır; başta hızlı ilerlemek, sonda ince ayar yapmak için.
