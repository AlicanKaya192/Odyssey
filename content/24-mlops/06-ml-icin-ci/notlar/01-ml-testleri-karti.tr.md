ML hattında sınanan şeyler ve ne zaman düştükleri:

| Sınama | Neyi yakalar | Örnek |
|---|---|---|
| Birim testi | Özellik kodundaki hata | Sütun sırası değişti |
| Veri doğrulama | Bozuk veri | Ücret kuruşla geldi |
| Tekrarlanabilirlik | Tohumsuz yeni adım | İki eğitimin tahminleri farklı |
| Alt sınır | Genel kötüleşme | Doğruluk 0,78'in altında |
| Temel çizgiye göre pay | Hiçbir şey öğrenmeyen model | Doğruluk temel çizgiyle aynı |
| Dilim çıtası | Bir grupta çöküş | `pro` müşterilerde 0,654 |
| Yön testi | Ters mantık | Arama artınca iptal olasılığı düşüyor |
| Açık örnek | Büyük yanlış | Belli bir iptali "kalır" sanıyor |

## Dersteki ölçüm

| Model | Doğruluk | Kapı |
|---|---|---|
| Lojistik regresyon | 0,813 | Geçti |
| Aynısı, `C=0.0001` | 0,703 (temel çizgi) | Dört sorun |

| Model | Yön testinin tuttuğu müşteriler |
|---|---|
| Lojistik regresyon | %100 |
| Rastgele orman | %95,7 |

## Davranış testi türleri

- **Yön testi** (directional): bir değer belli yönde değişince tahmin
  beklenen yönde gitmeli.
- **Değişmezlik testi** (invariance): sonucu etkilememesi gereken bir
  şey değişince tahmin değişmemeli. Örneğin müşterinin kimliği ya da
  adının yazımı.
- **Açık örnek** (minimum functionality): cevabı herkesçe belli birkaç
  örnekte model doğru demeli.

## Terimler

- **Kalite kapısı** (quality gate): modeli çıtayla karşılaştıran ve
  geçemezse hattı durduran adım.
- **Dilim** (slice): verinin bir kesimi; bir paket, bir şehir, yeni
  müşteriler gibi.
- **Davranış testi** (behavioral test): modelin doğruluğuna değil
  tepkisinin mantığına bakan sınama.
