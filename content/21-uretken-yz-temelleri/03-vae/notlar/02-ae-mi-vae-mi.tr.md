| | Otomatik kodlayıcı | VAE |
|---|---|---|
| Kod | Tek nokta | Dağılım ($\mu$, $\sigma$) |
| Kayıp | Yalnızca geri kurma | Geri kurma + β × KL |
| Kodların yeri | Ağın keyfine kalmış (derste ortalama −9,99; 1,69) | Standart normale yakın (ortalama ~0, yayılım ~1) |
| Yeni örnek | Nereden çekileceği belli değil | Standart normalden |
| Standart normalden 1000 kod | 4 rakam (öteki tohumlarda 3 ve 5) | 10 rakam (üç tohumda da) |
| Geri kurma, 8 sayılık kod | Daha iyi (0,0139) | Daha bulanık (0,025) |
| Ne zaman | Sıkıştırma, gürültü temizleme, aykırı değer | Üretim, düzenli kod uzayı, ara değerleme |

**Sık hatalar:**

- **KL'nin işaretini ya da sırasını karıştırmak.** Formül
  $\frac{1}{2}\sum(\mu^2 + \sigma^2 - \log\sigma^2 - 1)$; standart normalde
  (`mu = 0`, `logvar = 0`) sonuç 0 çıkmalı. Kendi kodunu önce bununla dene.
- **`logvar`'ı varyans sanmak.** `std = np.exp(0.5 * logvar)`; `np.sqrt(logvar)`
  negatif sayıda `nan` verir.
- **Ölçerken örnek çekmek.** Test hatası her çalıştırmada oynar;
  ölçümde $\mu$ kullan.
- **β'yı körlemesine büyütmek.** Kod uzayı düzenlenir ama bir noktadan sonra
  model çöker ve her şeyi aynı lekeye çevirir. KL'nin sıfıra indiğini
  görürsen β çok büyüktür.
- **Tek bir tohuma güvenmek.** Derste hakemin "emin" oranı tohumdan tohuma
  değişti; sonuç önemliyse eğitimi birkaç tohumla tekrarla.
