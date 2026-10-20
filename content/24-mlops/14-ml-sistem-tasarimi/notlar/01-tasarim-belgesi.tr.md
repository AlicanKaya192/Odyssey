Kısa bir tasarım belgesi kod yazmadan önce yazılır. Bu örnek, modülün
iptal modeli için doldurulmuş hâli.

## Hedef

- İş hedefi: iptal edecek müşteriye indirim teklif ederek iptali azaltmak.
- İş ölçüsü: kâr = kurtarılan müşterilerin beklenen değeri − tekliflerin
  maliyeti.
- Varsayımlar: teklif 5 birim; iptal edecek müşterinin kabulü %30, kalan
  müşteri 60 birim.

## Veri

- Kaynak: müşteri tablosu, her gece tarih itibarıyla çekilir.
- Etiket: `churned`, bir ay sonra belli olur (etiket gecikmesi).
- Doğrulama: şema ve aralık denetimi, karantina eşiği %5.

## Model

- Temel çizgi: `support_calls >= 2` kuralı.
- Model: ölçeklenmiş lojistik regresyon; eşik kâra göre seçilir.
- Kapı: güncel, etiketli bir kümede temel çizgiden ve canlıdaki modelden
  iyi olmalı.

## Sunma

- Toplu tahmin, her gece; sonuç bir tabloya yazılır.
- Yedek plan: model ya da tablo yoksa kural çalışır.

## İzleme ve yeniden eğitim

- İzleme: PSI, kalibrasyon farkı, aylık kâr.
- Yeniden eğitim: ayda bir + kalite uyarısında; son pencere ölçülerek
  seçilir.

## Yapma

- "Doğruluk %80'in üstünde olsun" diye hedef yazma; iş ölçüsünü yaz.
- Varsayımları belgeye yazmadan eşik seçme.
