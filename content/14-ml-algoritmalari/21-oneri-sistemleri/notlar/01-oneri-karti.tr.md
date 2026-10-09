## Yöntemler

| Yöntem | Tahmin | Güçlü yanı | Zayıf yanı |
|---|---|---|---|
| Genel ortalama | `μ` | basit | kişiselleştirme yok |
| Sapma taban çizgisi | `μ + b_u + b_i` | hızlı, sağlam | zevki görmez |
| Kullanıcı tabanlı CF | benzer kullanıcıların sapmaları | açıklanabilir ("sana benzeyenler") | çok kullanıcıda yavaş |
| Ürün tabanlı CF | benzer ürünlere verdiğin puanlar | ürünler az değişir, önceden hesaplanır | yeni ürün |
| Matris ayrıştırma | `μ + b_u + b_i + p_u · q_i` | en isabetli, ölçeklenir | gizli boyutlar yorumlanmaz |
| İçerik tabanlı | ürünün özellikleri (tür, yazar) | yeni ürün de önerilir | benzerinin benzerini önerir |

## Ölçüler

| Ölçü | Ne ölçer |
|---|---|
| RMSE | puan tahmininin hatası |
| precision@k | önerilen `k` üründen kaçı isabetli |
| recall@k | isabetli ürünlerin kaçı önerildi |
| Kapsama | kataloğun ne kadarı hiç önerildi |

## Matris ayrıştırma adımı (bir puan)

- `err = r − (μ + b_u + b_i + p_u · q_i)`
- `b_u += lr (err − λ b_u)`, `b_i += lr (err − λ b_i)`
- `p_u += lr (err q_i − λ p_u)`, `q_i += lr (err p_u − λ q_i)` (ikisi de eski
  değerlerle)

## Sık hatalar

- Boş hücreleri 0 puan sanmak: eksik veri "beğenmedi" değildir.
- Ölçmeden önce test puanlarını eğitime katmak (sızıntı).
- Yalnızca RMSE'ye bakmak: kullanıcı listeyi görür, hatayı değil.
- Her şeyi popüler ürünlere yığmak: kişiselleştirme ve çeşitlilik kaybolur.
