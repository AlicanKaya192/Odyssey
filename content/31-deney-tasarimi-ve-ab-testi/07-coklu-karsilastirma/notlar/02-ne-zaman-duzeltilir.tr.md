Her p değerini düzeltmek gerekmez. Soru şudur: bu testlerden **hangisi
karar veriyor?**

## Düzeltme gerekmeyenler

- **Önceden yazılmış tek birincil metrik.** Karar ona bağlıysa test ailesi
  tek testtir.
- **Koruma metrikleri**, yalnızca "bozuldu mu" diye bakılıyorsa ve
  bozulma testi durduruyorsa. Burada yanlış alarmın bedeli gereksiz bir
  durma, yanlış bir lansman değil.

## Düzeltme gerekenler

- Kararı birden çok metriğin **herhangi birine** bağlamak ("satın alma ya
  da gelir artarsa yayınlarız").
- Birden çok varyantı kontrolle karşılaştırıp en iyisini seçmek.
- Test bittikten sonra metrik, segment ya da zaman aralığı aramak. Bu
  durumda düzeltme bile yetmez: m'yi bilmek mümkün değildir. Bulunan şey
  yeni bir testin **sorusu** olur, sonucu değil.

## Raporda

- Kaç metriğe bakıldığını yazın.
- Birincil metriği ayrı, ikincilleri ayrı bir tabloda verin.
- İkincil bir metrik düzeltmeden sonra da anlamlıysa "ilginç, ayrı bir
  testle doğrulanmalı" diye yazın; karar ona dayandırılmaz.
