Hangisini raporlayacağın sorunun ne olduğuna bağlı. Tek kural yok, ama üç
soru çoğu zaman cevabı veriyor.

## 1. Toplamla mı ilgileniyorsun?

Sunucu maliyeti, toplam satış, toplam harcanan zaman gibi bir **toplam**
soruluyorsa ortalama gerekir: ortalama × kişi sayısı = toplam. Medyan bu
hesabı yapamaz.

## 2. Tipik kişiyi mi anlatıyorsun?

"Kullanıcılarımız genelde kaç dakika kalıyor?" sorusunda çarpık veride
medyan daha dürüst. Bu bölümde oturum süresinin ortalaması 9,04,
medyanı 7,49 dakikaydı: kullanıcıların yarısı 7,49
dakikadan kısa kalıyor.

## 3. Aykırı değerler gerçek mi?

- Ölçüm hatasıysa (açık unutulmuş uygulama, saat hatası) önce veri temizlenir.
- Gerçek davranışsa (gerçekten çok uzun oturumlar) silinmez; medyanı da
  ortalamayı da ver.

## İkisini birlikte ver

Raporda tek sayı yerine şu üçlü çoğu zaman en iyisi:

- medyan (tipik değer),
- ortalama (toplam için),
- bir yayılım ölçüsü: IQR ya da 95. yüzdelik.

Ortalama ile medyan arasındaki büyük fark kendi başına bir bilgidir:
"dağılım çarpık, birkaç büyük değer var" der.

## Sık yapılan hatalar

- Çarpık veride yalnızca ortalamayı vermek ve onu "tipik" diye sunmak.
- Ortalama ve standart sapmayı yan yana verip "değerlerin çoğu ortalama ± 2
  sapma içinde" demek: bu yalnızca çan biçimli veride geçerli.
- pandas ile NumPy'nin standart sapmasını karıştırmak (`ddof`).
