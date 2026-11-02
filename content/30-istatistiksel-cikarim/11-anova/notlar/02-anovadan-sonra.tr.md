ANOVA'nın "anlamlı" demesi yolun sonu değil, başı. Tek başına yalnızca
"grupların hepsi aynı değil" der. Karar için üç soru daha cevaplanmalı.

## 1. Hangi gruplar farklı?

Tukey HSD gibi bir post-hoc test kullan. Altı çifti düzeltmesiz t-testleriyle
sınamak, ANOVA'dan önce yapınca olduğu gibi yanlış alarmları katlar.

Yalnızca **önceden belirlenmiş** birkaç karşılaştırma ilgini çekiyorsa
(örneğin her yeni düzeni yalnızca eski düzen A ile karşılaştırmak) bütün
çiftlere bakmak gerekmez; o birkaç karşılaştırma için daha güçlü
yöntemler var (ikinci modülde: çoklu karşılaştırma).

## 2. Fark ne kadar büyük?

Bu bölümde F büyük ve p çok küçüktü, ama $\eta^2$ = 0,037: sürenin
yalnızca küçük bir kısmı düzenden geliyor. C düzeninin A'dan farkı
yaklaşık 1,4 dakika; bu fark iş için önemli mi, sayfanın amacına göre
karar verilir.

## 3. Sonuç gerçek hayata taşınır mı?

- Gruplar rastgele mi atandı? Atanmadıysa (kullanıcı düzeni kendisi
  seçtiyse) fark düzenden değil seçenlerin farklılığından gelebilir.
- Ölçüm süresi yeterli miydi? Yeni bir düzen ilk günlerde merak
  uyandırıp sonra etkisini yitirebilir (yenilik etkisi, ikinci modülde).

## ANOVA "anlamlı değil" derse

Bütün düzenler aynı demek değildir. Gruplar küçükse gerçek farklar kolayca
kaçırılır. Bu bölümde Tukey bile C ile D arasındaki gerçek 0,6 dakikayı
150'şer kişiyle ayırt edemedi. Güç analizi bölümünde kaç kişinin yeteceğini
önceden hesaplamayı öğreneceğiz.
