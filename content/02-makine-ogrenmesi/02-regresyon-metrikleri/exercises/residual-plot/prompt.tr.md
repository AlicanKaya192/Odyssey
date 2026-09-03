Önceki alıştırmada modelin en çok 26 yaşındaki evde yanıldığını gördün.
Tek kayıttı; şimdi bunun bir **desen** olup olmadığına bakacaksın.

Bu kez kalıntıları **eğitim** verisinde hesaplıyorsun. Kural değişmedi:
orada **ölçüm** yapmıyorsun, **teşhis** koyuyorsun. Otuz kayıt, on kayıttan
daha net bir resim veriyor ve test kümesi ölçüm için el değmemiş kalıyor.

**Yapman gerekenler:**

1. Oku, `area` ile `price`'ı al, ayır (`random_state=42`), modeli eğit.
2. **Eğitim** kalıntılarını hesapla: `y_train - model.predict(X_train)`.
3. Eğitim satırlarının **yaşlarını** al.
4. Kalıntıları yaşa karşı **saçılım** olarak çiz.
5. Sıfır çizgisini kırmızıyla ekle — desen ancak ona göre okunuyor.
6. Eksenleri `age` ve `residual` diye adlandır, başlık koy, `chart.png`
   olarak kaydet.
7. Kalıntı ile yaş arasındaki **korelasyonu** üç ondalıkla yazdır.

**Beklenen çıktı:**

```
-0.937
```

Grafiğin çalıştırma sonrası **sonuç panelinde** görünecek.

**Bu sayı çok şey söylüyor.** -0.937 neredeyse mükemmel bir ters ilişki:
yaş büyüdükçe kalıntı düşüyor, yani model **sistematik olarak yüksek**
tahmin ediyor. Rastgele bir dağılım olsaydı korelasyon sıfıra yakın
çıkardı.

**Grafikte göreceğin şey** noktaların soldan sağa aşağı inen bir bulut
oluşturması. Bu bir bulut değil, bir çizgi eğilimi — ve bir modelin
kalıntısında görülmesi gereken son şey.

**Kalıntıda desen görmek kötü haber değil, yol haritası.** Desen, hâlâ
öğrenilebilecek bir şeyin orada durduğu anlamına geliyor. Buradaki şey
belli: `age` sütunu. Bölüm 01'de eklediğimizde hata 18.5'ten 7.13'e
inmişti — bu grafik onu **eklemeden önce** söylüyordu.

Bir modeli iyileştirmenin yolu genelde daha karmaşık bir model denemekten
değil, kalıntının ne söylediğini dinlemekten geçiyor.
