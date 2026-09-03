Önceki alıştırmada test sütununun zıpladığını gördün. Şimdi o zıplamanın
nereden geldiğini ölçeceksin.

Model sabit, veri sabit. **Değişen tek şey ayrımın rastgeleliği.**

**Yapman gerekenler:**

1. Veriyi hazırla (oku, eksikleri at, kodla) ama **ayırma**.
2. `random_state` değerini **0'dan 4'e** kadar değiştirerek beş kez ayır.
3. Her turda doğrusal regresyon eğit ve test MAE'sini ölç. İki ondalığa
   yuvarlayıp bir listede birikt.
4. Listeyi olduğu gibi yazdır.
5. **En düşük, en yüksek ve aradaki farkı** yan yana yazdır.

**Beklenen çıktı:**

```
[16.16, 16.95, 17.07, 19.68, 21.56]
16.16 21.56 5.4
```

**Aynı model, aynı veri, beş farklı cevap.**

En düşük 16.16, en yüksek 21.56. Aradaki fark **5.40** — yani sayının
kendisinin yaklaşık üçte biri.

Bunu bir raporda düşün: `random_state=0` yazan biri "modelimin hatası
16.16" diyor, `random_state=4` yazan biri "21.56" diyor. İkisi de dürüst,
ikisi de aynı modeli anlatıyor.

**Bu, önceki bölümlerde ölçtüğün her sayının üstünde duran bir uyarı.**
Tek bir ayrımdan gelen sonuç bir **tahmin**, kesin bir ölçüm değil.
`random_state=42` yazmak sonucu tekrarlanabilir yapıyor ama daha doğru
yapmıyor.

İki modeli karşılaştırırken bu daha da tehlikeli: aralarındaki 2 birimlik
fark modelden mi geliyor, ayrımdan mı? Bu haliyle söylenemiyor.

Çözüm bir sonraki alıştırmada.
