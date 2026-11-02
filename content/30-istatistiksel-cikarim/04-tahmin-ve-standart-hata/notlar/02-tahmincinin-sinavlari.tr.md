Bir tahmin kuralını değerlendirmenin yolu, onu binlerce örneklemde
çalıştırıp davranışına bakmak. Bu bölümde bunu üç kez yaptık.

## 1. Yansızlık: ortalamada doğru yerde mi?

Binlerce örneklemin tahminlerinin ortalaması gerçeğe eşitse tahminci
yansızdır.

- Örneklem ortalaması: yansız.
- $n-1$'e bölen varyans: yansız; $n$'e bölen: küçük tahmin eder.
- Örneklemin en büyüğü: yanlı; örneklemlerin %99,9 kadarı gerçeğin
  altında kaldı.

## 2. Tutarlılık: büyüdükçe gerçeğe yaklaşıyor mu?

Örneklem büyüdükçe tahminler gerçeğin etrafında toplanıyorsa tahminci
tutarlıdır. Örneklem ortalamasının oynaması $\sqrt{n}$ ile küçülür; ilk
bölümde 400 kişilik örneklemlerin 25 kişiliklere göre çok daha sıkı
toplandığını gördük.

Yanlı bir tahminci de tutarlı olabilir: $n$'e bölen varyansın yanlılığı
örneklem büyüdükçe kaybolur.

## 3. Etkinlik: aynı veriyle ne kadar az oynuyor?

İki yansız tahminciden daha az oynayanı daha etkindir. Çan biçimli açılış
sürelerinde medyanın varyansı ortalamanınkinin yaklaşık 1,53
katıydı: medyan aynı hassasiyet için daha çok veri ister.

## Değişen ölçü: ortalama kare hata

Bazen biraz yanlı ama çok az oynayan bir tahminci, yansız ama çok oynayan
birinden daha iyidir. İkisini birlikte ölçen sayı **ortalama kare hata**
(mean squared error):

$$MSE = \text{yanlılık}^2 + \text{varyans}$$

Makine öğrenmesindeki düzenlileştirme (regularization) tam bu takası yapar:
biraz yanlılık kabul edip oynamayı azaltır.

## Kontrol listesi

- Tahminciyi tek sayıyla değil, benzetimle değerlendir.
- Gerçeği bildiğin bir veride (bizim evrenimiz gibi) sına.
- Yanlılığı, oynamayı ve ikisinin toplamını ayrı ayrı yaz.
