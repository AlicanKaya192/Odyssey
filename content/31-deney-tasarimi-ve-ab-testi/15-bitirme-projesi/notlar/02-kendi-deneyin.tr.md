Bitirme projesindeki çözümleme bir şablondur. Kendi verinle denemek için
aşağıdaki planı doldur, sonra adımları sırayla uygula.

## Plan şablonu

| Alan | Senin cevabın |
|---|---|
| Değişiklik | ... |
| Hipotez | "... yüzünden ... artacak" |
| Birincil metrik ve birimi | ... (kullanıcı başına mı, gösterim başına mı?) |
| Pratik eşik | ... puan |
| Koruma metrikleri | ... (sınırlarıyla) |
| Ortak değişken (CUPED) | ... (testten önce ölçülmüş) |
| Segmentler | en fazla bir ya da iki |
| Örneklem ve süre | ... kullanıcı, ... gün |
| Bakma kuralı | yalnızca son gün / ardışık eşikler |
| Karar kuralı | dört sonuç ve her birinde ne yapılacağı |

## Veri yoksa

`ab_data.py` içindeki fonksiyonlarla kendi senaryonu kur: `make_capstone`
fonksiyonuna farklı bir `lift` (ör. 0 ya da −0,05) vererek aynı çözümlemenin
başka sonuçlara nasıl vardığını gör. Gerçek etkiyi bilen biri olarak
çözümlemenin onu bulup bulmadığına bak: bu, yöntemi sınamanın en iyi
yoludur.

## Sık yapılan hatalar

- Planı testten sonra yazmak.
- Birincil metriği sonuca göre değiştirmek.
- Belirsiz sonucu "etki yok" diye raporlamak.
- Segmentlerde en çarpıcı olanı öne çıkarmak.
