Örneklem sayıyı küçültüyor ama soruyu değiştirmemeli. Bu yanılgıların her
biri örneklemin bütünü temsil etmemesine yol açıyor.

## 1. İlk N satır

`head(10_000)` zaman sıralı siparişlerde yılın ilk dört günü. Dosyalar çoğu
zaman bir sıraya göre yazılır (zaman, müşteri, bölge); ilk satırlar o sıranın
yalnızca başı. Her zaman rastgele seç.

## 2. Büyük örneklem yanlılığı düzeltir sanmak

Yanlı bir yöntemle alınan örneklem büyüdükçe yanlılık kalıyor, yalnızca
daha emin görünüyor. "İlk bir milyon satır" da yalnızca ilk satırlar.

## 3. Nadir olayı örneklemle aramak

Binde bir görülen bir olay, bir milyon satırın yüzde birlik örnekleminde
ortalama on kez görülür; bazen hiç görülmez. Dolandırıcılık, arıza, şikâyet gibi nadir olaylarda
verinin tamamına bak ya da o olayları ayrıca örnekle.

## 4. Küçük grubu basit örneklemle karşılaştırmak

1 600 satırlık rastgele örneklemde Trabzon'a 75 sipariş düştü; tahmini
İstanbul'unkinden yaklaşık üç kat fazla oynadı. Grupları karşılaştıracaksan
katmanlı örneklem.

## 5. Tohumu unutmak

`random_state` vermezsen her çalıştırma başka satırlar seçer; sonuç tekrar
edilemez, hata ayıklamak zorlaşır. Tohum ver, raporuna yaz.

## 6. Önce süzüp sonra örneklemek, ya da tersi

"İzmir siparişlerinden yüzde bir" ile "yüzde birlik örneklemin İzmir
siparişleri" aynı soru değil. İkincisinde İzmir için yalnızca yaklaşık
1 300 satır kalır. Ne istediğini önce cümleyle yaz.

## 7. Yaklaşık sonucu kesin sanmak

`approx_count_distinct` bu patikada 245 461 müşteriyi 219 479 saydı (yüzde
10,6 eksik). Yaklaşık sayıyı raporlarken "yaklaşık" de; fatura, muhasebe gibi
işlerde kullanma.

## 8. Standart hatayı yanlış n ile hesaplamak

Standart hatada n, **örneklemin** büyüklüğü; verinin tamamınınki değil.
Bir milyonluk veriden 10 000'lik örneklem: n = 10 000.
