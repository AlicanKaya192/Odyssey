Dersteki döngü her turun iki kaybını `history`'de tuttu. Birkaç tura
bakalım:

```python
for epoch in [1, 5, 10, 20, 30]:
    train_loss, val_loss = history[epoch - 1]
    print(epoch, round(train_loss, 3), round(val_loss, 3))
```

```text
1 0.696 0.431
5 0.228 0.353
10 0.212 0.359
20 0.206 0.409
30 0.178 0.432
```

İlk turlarda iki kayıp birlikte düşüyor. Sonra eğitim kaybı düşmeye devam
ederken doğrulama kaybı yükseliyor: aradaki açıklık büyüyor. İki eğrinin
birlikte okunuşu:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>İkisi de düşüyor</span><span>Model öğreniyor; eğitime devam.</span></div>
    <div class="anat-row"><span>Eğitim düşüyor, doğrulama yükseliyor</span><span>Aşırı öğrenme (overfitting): model eğitim verisini ezberliyor. En iyi turda dur, düzenlileştirme ekle.</span></div>
    <div class="anat-row"><span>İkisi de yüksek ve yatay</span><span>Yetersiz öğrenme (underfitting): model çok küçük, öğrenme oranı uygunsuz ya da tur az.</span></div>
    <div class="anat-row"><span>Kayıp zıplıyor, <code>nan</code> oluyor</span><span>Öğrenme oranı fazla yüksek.</span></div>
  </div>
  <figcaption>Eğitim ve doğrulama kaybını birlikte okumak.</figcaption>
</figure>

Tek bir kayıp sayısı bunların hiçbirini söylemez; iki eğriyi yan yana
görmek gerekir. Kayıpları bir listede tutup sonradan çizmek (ya da
birkaç turunu yazdırmak) bu yüzden alışkanlık olmalı.
