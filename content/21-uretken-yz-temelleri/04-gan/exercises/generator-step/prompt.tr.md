`train(steps, seed)` dersteki GAN'ı eğitiyor ama üreticinin adımı eksik.
Ayırt edicinin adımından sonra yaz: yeni bir gürültüden sahte grup üret
(`acts_g = forward(rng.normal(size=(128, 2)), gen)`), onu ayırt ediciden
geçir, logite göre türev `(p_f - 1) / 128` ile `backward` çağırıp girdiye
giden türevi al, o türevle üreticinin `backward`'ını çağır ve `opt_g.step`
ile güncelle. Fonksiyon bulunan küme sayısını ve kümeye yakın örnek oranını
döndürüyor.

**Beklenen çıktı:**

```
[8, 0.892]
```
