| | PCA | Sinir ağı otomatik kodlayıcı |
|---|---|---|
| Kodlama | Doğrusal izdüşüm | Doğrusal olmayan katmanlar |
| Eğitim | Tek SVD, saniyenin altında | Binlerce adım, ayar ister (öğrenme oranı, momentum) |
| Sonuç | Her çalıştırmada aynı | Başlangıç ağırlıklarına ve hesap farklarına göre biraz oynar |
| Aynı kod boyunda hata | Daha yüksek (2 boyutta 0,0539) | Daha düşük (2 boyutta 0,0393) |
| Ne zaman | Hızlı bir taban çizgisi, az veri | Eğri yapılı, çok veri |

**Önce PCA'yı dene.** Sinir ağının hatası PCA'nınkinden belirgin biçimde
düşük değilse ek karmaşıklığa değmez. Bu bölümde fark belirgindi, ama her
veri için öyle olmayabilir.

**Sık hatalar:**

- **Test verisini eğitimde kullanmak.** Otomatik kodlayıcı da ezberleyebilir;
  geri kurma hatası her zaman görmediği resimlerde ölçülür.
- **Ortalamayı çıkarmadan PCA.** SVD'den önce `X - mean` yapılmazsa ilk yön
  verinin yayılımını değil ortalamasını anlatır.
- **Çıkış etkinleştirmesini veriye uydurmamak.** Pikseller 0–1 arasındaysa
  çıkışta `sigmoid` mantıklı; `tanh` (−1, 1) aralığı verir.
- **Kodu fazla geniş seçmek.** 64 piksele 64 sayılık kod hiçbir şeyi
  sıkıştırmaz; hata sıfıra yakın çıkar ama model bir şey öğrenmemiştir.
