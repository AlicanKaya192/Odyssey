Test seçimi verinin **nasıl toplandığına** bağlıdır, sayıların görünüşüne
değil. İki sütun yan yana duruyor diye veri eşli olmaz; iki ayrı tabloda
durduğu için de bağımsız olmaz.

## Eşli örnekler

- Aynı sayfaların değişiklikten önce ve sonra açılış süresi.
- Aynı kullanıcıların eski ve yeni sürümle yaptığı görev süresi.
- Aynı mağazaların geçen ay ve bu ay satışı.
- Aynı öğrencinin ön test ve son test puanı.

Ortak nokta: her ölçümün öteki grupta **tam bir eşi** var ve eşler
birbirine benziyor.

## Bağımsız örnekler

- A/B testinde A ve B gruplarına rastgele atanmış farklı kullanıcılar.
- İki ayrı şehirden alınmış iki örneklem.
- Mobil ve masaüstü kullanıcıları.

## Yanlış seçimin bedeli

| Yanlış | Sonuç |
|---|---|
| Eşli veriye bağımsız test | Birimler arası fark gürültü sayılır; güç çöker. Bu bölümde gerçek kazancı yakalama oranı %78,2 iken %0,0 oldu |
| Bağımsız veriye eşli test | Rastgele sıraya dizilmiş satırlar eşleştirilir; sonuç anlamsızdır |

## Eşliyi tasarımla kazanmak

Eşli tasarım çoğu zaman bilinçli seçilebilir: aynı kullanıcıya iki sürümü
de göstermek (sırası rastgele), aynı sayfayı iki kez ölçmek. Birimler
birbirinden çok farklıysa bu, aynı güç için çok daha az ölçüm demektir.
İkinci modüldeki CUPED yöntemi de aynı fikrin A/B testlerine uyarlanmış
hâlidir: kullanıcının deneyden önceki davranışını "kendi eşi" gibi kullanır.
