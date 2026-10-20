Eğitim-sunma farkının biçimleri:

| Biçim | Örnek | Nasıl önlenir |
|---|---|---|
| Kod farkı | Sunma ekibi özellik kodunu yeniden yazdı, iki sütun yer değiştirdi | Özellik kodu tek yerde; ikisi de içe aktarır |
| Birim farkı | Eğitimde 29,90, canlıda 2990 (kuruş) | Şema ve sunma anı profili |
| Eksik değer farkı | Eğitimde ortalamayla doldurulmuş, canlıda 0 | Doldurma da özellik kodunun parçası |
| Zaman sızıntısı | Eğitimde iptal sırasındaki aramalar da sayılmış | Özellikler tahmin anı itibarıyla (as of) |
| Veri kaynağı farkı | Eğitimde günlük toplu tablo, canlıda başka bir servis | Tek tanımlı özellik deposu |

## Dersteki ölçüm

| Durum | Doğruluk |
|---|---|
| Eğitimdeki özelliklerle | 0,813 |
| İki sütunu yer değiştirmiş sunma kodu | 0,297 |
| Herkese "kalır" (temel çizgi) | 0,703 |
| Sızıntılı model, testte | 0,939 |
| Sızıntılı model, canlıda | 0,787 |

Sızıntılı model testte en iyi, canlıda sızıntısızdan kötü.

## Yakalamak

- Sunma anında modele giren vektör kaydedilir (bir kısmı yeter).
- Kayıtlı vektörlerin sütun ortalamaları eğitimdekilerle karşılaştırılır.
- Büyük fark varsa önce kod farkından şüphelenilir: sütun sırası, birim,
  doldurma.

## Terimler

- **Eğitim-sunma farkı** (training-serving skew): modelin canlıda
  eğitimdekinden farklı hesaplanmış girdiler görmesi.
- **Zaman sızıntısı** (point-in-time leakage): eğitimde, tahmin anında
  bilinemeyecek bilgiyi kullanmak.
- **İtibarıyla sorgu** (as of): bir tarihte bilinen son değeri almak.
