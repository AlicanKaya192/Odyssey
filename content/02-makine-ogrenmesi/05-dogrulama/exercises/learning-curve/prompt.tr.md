Bir model yeterince iyi değilse iki yol var: **daha çok veri toplamak** ya
da **modeli değiştirmek**. Hangisinin işe yarayacağını tahmin etmek yerine
ölçeceksin.

Yöntem: modeli eğitim verisinin gitgide büyüyen parçalarıyla tekrar tekrar
eğitip iki hatayı da izlemek.

**Yapman gerekenler:**

1. Veriyi hazırla ve ayır (`random_state=42`).
2. Şu boyutları sırayla dene: **10, 20, 30, 45, 60, 79**.
3. Her boyut için modeli eğitim verisinin **ilk o kadar satırıyla** eğit ve
   iki hata ölç:
   - o parçadaki **eğitim** hatası
   - **her zaman aynı** test kümesindeki hata
4. Her boyut için tek satır yazdır: **boyut, eğitim hatası, test hatası**.
5. İki eğriyi aynı grafiğe çiz, etiketle, `legend` ekle. Eksenler
   `training size` ve `MAE`, başlık koy, `chart.png` olarak kaydet.
6. Son boyuttaki iki hata arasındaki fark **1'den küçükse** `no`, değilse
   `yes` yazdır. (Soru: daha çok veri işe yarar mı?)

**Beklenen çıktı:**

```
10 10.1 19.4
20 11.8 18.59
30 13.87 18.22
45 15.45 18.01
60 16.33 16.75
79 15.52 15.69
no
```

Grafiğin çalıştırma sonrası **sonuç panelinde** görünecek.

**İki eğri birbirine doğru gidiyor** ve bu şaşırtıcı olabilir:

- **Eğitim hatası yükseliyor** (10.10 → 15.52). On kaydı ezberlemek kolay,
  79 kaydı değil. Model büyüdükçe daha zor bir sınava giriyor.
- **Test hatası düşüyor** (19.40 → 15.69). Daha çok örnek gören model daha
  iyi genelliyor.
- **Sonunda buluşuyorlar:** 15.52 ve 15.69, aradaki fark 0.17.

**Yazdırdığın `no` bir karar.** Eğriler buluştuysa model artık ezberlemiyor;
eldeki veriden alınabilecek alınmış. Yüz araba daha toplamak bu sayıyı
değiştirmeyecek.

Eğer arada açıklık kalsaydı (eğitim 5, test 18 gibi) cevap `yes` olurdu:
model ezberliyor demektir ve daha çok veri onu bastırır.

**Bu grafik pahalı bir kararı ucuza aldırıyor.** "Veri toplayalım mı, model
mi değiştirelim" sorusu haftalar sürebilecek bir iş; öğrenme eğrisi
saniyeler içinde cevaplıyor.

Buradaki cevap "model ya da özellik" tarafında: daha iyi olmak istiyorsan
yeni bir sütun ya da farklı bir yöntem gerekiyor.
