`km` sütunu 10.000 ile 300.000 arasında, `engine` 1.0 ile 2.0 arasında.
İkisi de sayı ama aynı dünyada değiller. Bu alıştırmada farkın **hangi
modeli ne kadar** etkilediğini ölçeceksin.

**Yapman gerekenler:**

1. Dosyayı oku ve eksik satırları at (`dropna`). Bu bölümün konusu
   ölçekleme; eksikleri önceki alıştırmada çözdün.
2. `X`'e üç sayısal sütunu, `y`'ye `price`'ı al. Ayır (`random_state=42`).
3. `StandardScaler`'ı **eğitimde** öğret, **ikisine de** uygula.
4. **KNN**'i (`n_neighbors=5`) iki kez eğit: ham veriyle ve ölçekli veriyle.
   İki MAE'yi yan yana yazdır (iki ondalık).
5. **Doğrusal regresyonu** da iki kez eğit: ham ve ölçekli. İki MAE'yi yan
   yana yazdır.
6. Doğrusal regresyonun iki sonucu aynıysa `same`, farklıysa `different`
   yazdır.

**Beklenen çıktı:**

```
171.49 51.48
34.63 34.63
same
```

**Birinci satır: üç kat fark.** Ölçeklemesiz KNN aslında yalnızca `km`'ye
bakıyor. `engine` sütunundaki 1.0 ile 2.0 arasındaki fark, `km`'deki
250.000'lik farkın yanında hiç. Mesafe hesabında küçük sütun sanki yokmuş
gibi davranıyor.

**İkinci satır: hiç fark yok.** Doğrusal regresyon her sütun için ayrı bir
katsayı öğreniyor ve o katsayıyı sütunun ölçeğine göre ayarlıyor. `km`
büyük sayılarsa katsayısı küçük çıkıyor; sonuç değişmiyor.

**Alınacak ders "her zaman ölçekle" değil, "hangi modelin neye baktığını
bil":**

| Etkileniyor | Etkilenmiyor |
|---|---|
| KNN, SVM, kümeleme, sinir ağları | Karar ağacı, rastgele orman |
| **Mesafe kullananlar** | **Eşik kullananlar** |

Bir ağaç "km 150.000'den büyük mü" diye soruyor; sütunun ölçeği bu soruyu
değiştirmiyor.

**`fit` ve `transform` ayrımına dikkat et.** Ölçekleyici eğitimin
ortalamasını ve standart sapmasını öğreniyor; teste `fit_transform`
çağırmak hem sızıntı olurdu hem de iki kümeyi farklı ölçeklere taşırdı.
