Modülün ilk bölümlerinde dört üretken model gördük. Sayılar bölümlerdeki
ölçümlerden; veri ve ayarlar küçük, sonuçlar bu deneylere aittir.

| | Otomatik kodlayıcı | VAE | GAN | Difüzyon |
|---|---|---|---|---|
| Ne öğrenir | Sıkıştırıp geri kurmayı | Kodu bir dağılım olarak | Ayırt ediciyi kandırmayı | Eklenen gürültüyü tahmin etmeyi |
| Eğitim | Tek ağ, geri kurma hatası | Tek ağ, geri kurma + KL | İki ağın oyunu | Tek ağ, sıradan regresyon |
| Yeni örnek nereden | Belli değil | Standart normalden | Gürültüden, tek geçişte | Gürültüden, 100 adımda |
| Bölümdeki sonuç | Rastgele koddan net rakam %32 | 10 rakamın hepsi | 8 küme; 0,01'de 8, 6, 6 | 8 küme; 0,01'de de 8, 8, 8 |
| Güçlü yanı | Sıkıştırma, aykırı değer | Düzenli kod uzayı | Keskin örnek, hızlı üretim | Kararlı eğitim, bütün türler |
| Zayıf yanı | Üretici değil | Bulanık | Kırılgan eğitim, mod çöküşü | Yavaş üretim |

**Hangisini ne zaman?**

- Veriyi **sıkıştırmak** ya da **aykırı değer** bulmak: otomatik kodlayıcı.
- Düzenli bir **kod uzayı** gerekiyorsa (ara değerleme, başka bir modelin
  içinde küçük kod): VAE. Modern resim üreticilerinde VAE tam bu iş için
  var.
- **Hızlı** üretim önemliyse ve eğitimi dikkatle ayarlayabiliyorsan: GAN.
- **Kalite ve çeşitlilik** önemliyse ve üretim süresi sorun değilse:
  difüzyon. Bugünkü resim üreticilerinin çoğu, VAE'nin kod uzayında
  çalışan difüzyon modelleridir.

**Sık hatalar:**

- **Geri adımda taze gürültüyü atmak.** Örnekler kümelerin ortasına
  toplanır ve çeşitlilik kaybolur (bölümde merkeze ortalama uzaklık 0,064,
  gerçek veride 0,125).
- **Adım numarasını ağa vermemek.** Aynı ağ bütün adımlarda çalışıyor;
  hangi adımda olduğunu bilmezse ne kadar gürültü çıkaracağını bilemez.
- **`alpha_bar` yerine `alphas` kullanmak.** Tek adımda gürültü formülü
  birikimli çarpımı (`alpha_bar`) ister; geri adım ikisini de kullanır.
- **Tek bir ölçüye bakmak.** Bölümde GAN kümeye yakınlıkta, difüzyon
  kararlılıkta öndeydi; bir modeli değerlendirirken hem kaliteye hem
  çeşitliliğe bak.
