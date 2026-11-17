`train_and_test(epochs)` veriyi, modeli, `DataLoader`'ı ve optimizer'ı kuruyor ve
sonunda test doğruluğunu ölçüyor; ama aradaki eğitim döngüsü yok. Döngüyü
yaz: her turda her küme için `zero_grad`, kayıp, `backward`, `step`. 10 turda
test doğruluğu %90'ı geçmeli.

**Beklenen çıktı:**

```
True
```
