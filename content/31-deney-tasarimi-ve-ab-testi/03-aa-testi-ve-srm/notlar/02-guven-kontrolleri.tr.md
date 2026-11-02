Bir deneyin sonucuna bakmadan önce geçilen kontroller. Biri düşerse sonuç
okunmaz.

| Kontrol | Ne sınanıyor | Araç |
|---|---|---|
| SRM | grup büyüklükleri tasarıma uyuyor mu | ki-kare uyum iyiliği |
| Denge tablosu | değişiklikten etkilenmeyen özellikler eşit mi | gruplara göre ortalamalar |
| A/A geçmişi | sistemin yanlış alarm oranı %5 civarı mı | çok sayıda A/A testi |
| Süre | plan kadar mı, tam haftalar mı | plan |
| Koruma metrikleri | bozulma var mı | ikincil testler |
| Kayıt eksiksizliği | olay sayıları günden güne makul mü | günlük sayım grafiği |

## Neden bu kadar titizlik?

Bozuk bir deney "temiz" görünen sahte bir sonuç üretir: bu bölümdeki
örnekte B hiçbir şey yapmadığı hâlde satın alma oranı anlamlı biçimde
yüksek çıktı. Sahte bir kazanç uygulamaya alınırsa, sonraki deneyler
yanlış bir taban üzerine kurulur.

## Yapma

- SRM'yi "küçük fark, önemli değil" diye geçmek.
- Kaybolan kullanıcıları elle "doldurmak" ya da bir gruptan rastgele
  kişi silip eşitlemek: kaybın nedeni rastgele değilse içerik yine bozuk.
- Tek bir A/A testinin anlamlı çıkmasından sistemin bozuk olduğu
  sonucunu çıkarmak.
