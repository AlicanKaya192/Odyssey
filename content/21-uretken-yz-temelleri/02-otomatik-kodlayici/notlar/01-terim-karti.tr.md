| Terim | Anlamı |
|---|---|
| **Otomatik kodlayıcı** (autoencoder) | Girdiyi dar bir koda sıkıştırıp aynı girdiyi geri kurmayı öğrenen ağ |
| **Kodlayıcı** (encoder) | Girdiyi koda indiren yarı |
| **Kod çözücü** (decoder) | Koddan girdiyi geri kuran yarı |
| **Kod** / **gizli temsil** (latent code) | Dar boğazdaki birkaç sayı |
| **Kod uzayı** (latent space) | Bütün olası kodların uzayı; 2 boyutluysa düzlemde çizilebilir |
| **Geri kurma hatası** (reconstruction error) | Giren ile çıkan arasındaki fark, burada ortalama kare hata |
| **Denetimsiz öğrenme** (unsupervised) | Etiket kullanmadan veriden yapı öğrenmek |
| **PCA** | Veriyi en çok yayıldığı yönlere yansıtan doğrusal yöntem; doğrusal bir otomatik kodlayıcı gibi |
| **Momentum** | Her güncellemenin bir önceki güncellemenin bir kısmını taşıması; eğitimi hızlandırır |
| **Gürültü temizleme** (denoising) | Gürültülü girdiyi koddan geçirip ortak yapıyı geri almak |
| **Aykırı değer bulma** (anomaly detection) | Kötü geri kurulan örneği "farklı" diye işaretlemek |

**Akılda kalsın:**

- Kod dar olmalı; geniş kod her şeyi ezberler ve hiçbir şey öğrenmez.
- Otomatik kodlayıcı sıkıştırmada iyidir, **üretmede** zayıftır: kod
  uzayında boşluklar var ve rastgele bir kod çoğu zaman anlamsız resim
  verir (bölümde net rakam oranı %32, gerçeklerde %69).
- Doğrusal olmayan ağ PCA'yı geçti (2 boyutlu kodda 0,0539 → 0,0393), ama
  bedeli uzun eğitim.
