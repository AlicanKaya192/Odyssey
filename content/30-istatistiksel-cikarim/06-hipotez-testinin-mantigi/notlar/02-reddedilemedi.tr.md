Bir testin en sık yanlış okunan sonucu "$H_0$ reddedilemedi"dir. Çoğu kişi
bunu "fark yok" diye okur. Değildir.

## Kanıt yokluğu, yokluğun kanıtı değil

Bu bölümdeki sunucu testinde gerçek bir 40 ms yavaşlama vardı ve test onu
göstermedi (p = 0,0968). Benzetim, 40 ölçümlük bu tasarımın gerçek
yavaşlamayı yalnızca %52,5 oranında yakaladığını söyledi. Test
"yavaşlama yok" demedi; "bu kadar veriyle ayırt edemiyorum" dedi.

## Ne yazmalı?

- "Fark yok" değil: "Fark istatistiksel olarak anlamlı bulunmadı."
- Yanına farkın güven aralığını koy. Aralık geniş ve hem sıfırı hem önemli
  bir yavaşlamayı içeriyorsa sonuç **kararsızdır**: daha çok veri gerekir.
- Aralık dar ve yalnızca önemsiz değerleri içeriyorsa ("en fazla 5 ms"),
  ancak o zaman "pratikte fark yok" denebilir.

## Güç düşükse test bilgi vermez

Gücü %20 olan bir test, gerçek farkların beşte dördünü kaçırır. Böyle bir
testin "anlamlı değil" demesi neredeyse hiçbir şey anlatmaz. Bu yüzden
deneyden **önce** kaç ölçüm gerektiğini hesaplamak (güç analizi) testin
kendisi kadar önemlidir.

## İki yanlış tepki

- "Anlamlı değil, demek ki değişiklik zararsız, yayına alalım." Kaçırılan
  bir yavaşlama kullanıcıya yine ulaşır.
- "Anlamlı çıkana kadar biraz daha ölçelim." Sonuca bakarak veri eklemek
  yanlış alarm oranını büyütür (ikinci modülde: sıralı bakma tuzağı).
  Ölçüm sayısı önceden belirlenir.
