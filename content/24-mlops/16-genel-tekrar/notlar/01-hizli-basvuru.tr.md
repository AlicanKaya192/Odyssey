Modülün kurallarını, ölçülerini ve eşiklerini tek sayfada topladık.

## Eşikler ve ölçüler

| Ne | Kural | Bölüm |
|---|---|---|
| PSI | 0,1'in altı kararlı, 0,25'in üstü büyük kayma | 10 |
| Gürültü | Aynı dönemden başka bir örneklemin değeri | 10, 12 |
| Kapı | Aday canlı modeli aynı güncel kümede `min_gain` kadar geçmeli | 5, 11 |
| Kalibrasyon | Ortalama olasılık ile gerçekleşen oran yakın olmalı | 11 |
| Gecikme | p95 ile yazılır, ortalama kuyruğu gizler | 7, 13 |
| Doluluk | %100'e göre değil, boşlukla planlanır (ör. %70) | 13 |
| A/A gürültüsü | Grup dört kat büyüyünce yaklaşık yarıya iner | 12 |

## Kayıtta ne olmalı?

| Kayıt | İçinde |
|---|---|
| Eğitim kaydı | Tohum, ayarlar, verinin özeti, kütüphane sürümleri |
| Deney kaydı | Her deney, kötüleri de: ayarlar, doğrulama skoru |
| Model kaydı | Sürüm, dosya özeti, ölçümler, eşik, canlı etiketi, model kartı |
| Tahmin kaydı | Kimlik, model sürümü, tahmin, girdiler; sonra gerçek sonuç |

## Sık hatalar

| Hata | Sonucu | Bölüm |
|---|---|---|
| Tohumu sonuca göre seçmek | İyimser ölçüm | 1, 4 |
| Veriyi denetlemeden eğitmek | Kod çalışır, model bozulur | 2 |
| Testte seçip testte raporlamak | Kazananın laneti | 4 |
| Eğitimde ve sunmada ayrı özellik kodu | Eğitim-sunma farkı | 8 |
| p-değerine uyarı bağlamak | Büyük örneklemde her şey "anlamlı" | 10 |
| Kapıyı eski kümeyle çalıştırmak | Yeni model haksızca reddedilir | 11 |
| Küçük kanaryada karar vermek | Şans karar verir | 12 |
| Eşiği 0,5'te bırakmak | İş ölçüsünde kayıp | 14 |
