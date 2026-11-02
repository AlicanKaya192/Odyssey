**p-hacking** (p avcılığı), aynı veriyi farklı biçimlerde inceleyip p < 0,05
çıkanı raporlamaktır. Çoğu zaman kötü niyet yoktur: her adım tek başına
makul görünür. Ama her yeni deneme yeni bir yanlış alarm şansı ekler; bu
bölümde 20 metriğe bakınca en az birinin "anlamlı" çıkma olasılığı
%62,6 kadardı.

## Sık görülen biçimleri

| Ne yapılıyor | Neden yanıltıyor |
|---|---|
| Birçok metriğe bakıp anlamlı olanı öne çıkarmak | Her metrik ayrı bir deneme |
| Veriyi segmentlere bölmek ("yalnızca mobilde anlamlı") | Her segment ayrı bir deneme |
| Anlamlı çıkana kadar veri toplamaya devam etmek | Her ara bakış ayrı bir deneme |
| Aykırıları sonuca göre atmak ya da tutmak | Analiz veriye göre seçiliyor |
| Sonucu görüp tek yönlü teste geçmek | Yanlış alarm oranı ikiye katlanıyor |
| Farklı testleri deneyip en küçük p'yi seçmek | Her test ayrı bir deneme |

## Önlemler

- **Önceden yaz:** soru, birincil metrik, örneklem büyüklüğü, test, yön ve
  $\alpha$ veri gelmeden belgelenir (ön kayıt, pre-registration).
- **Tek birincil metrik:** öteki metrikler "keşif" diye ayrıca ve ihtiyatla
  raporlanır.
- **Çoklu karşılaştırma düzeltmesi:** gerçekten çok şey sınanacaksa eşik
  buna göre sıkılaştırılır (Bonferroni, Holm; ikinci modülde).
- **Hepsini raporla:** kaç şeye bakıldığını, anlamlı çıkmayanlar dahil yaz.

## Kendine soracağın soru

"Veri başka türlü çıksaydı, analizi yine böyle mi yapacaktım?" Cevap
"hayır" ise p değeri sözünü tutmaz.
