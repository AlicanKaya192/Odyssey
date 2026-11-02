| Tür | Örnek | Kullanıcı başına değer | Test |
|---|---|---|---|
| Oran | satın alma oranı | 0 ya da 1 | iki oran z-testi |
| Ortalama | kullanıcı başına gelir | sürekli sayı | Welch t-testi |
| Sayım | kullanıcı başına ziyaret | 0, 1, 2, ... | Welch t-testi |
| Oran metriği | sipariş başına tutar | iki toplamın oranı | delta yöntemi ya da bootstrap |

## Göreli ve mutlak değişim

- **Mutlak:** B − A. Satın alma %11,7'den %12,2'ye çıktıysa +0,5 puan.
- **Göreli:** (B − A) / A. Aynı değişiklik yaklaşık +%4.

İkisi de yazılır; yalnızca göreli değişim yazmak küçük bir farkı büyük
gösterir (Etki Büyüklüğü bölümü).

## Duyarlılık için kaba kural

Değişim katsayısı (sapma / ortalama) ne kadar büyükse aynı göreli farkı
görmek için o kadar çok kişi gerekir: kabaca karesiyle. Gelir gibi uzun
kuyruklu metrikler bu yüzden pahalıdır. Seçenekler:

- daha duyarlı bir ara metrik (satın alma oranı) birincil, gelir ikincil;
- uç değerleri kırpmak (capping), ör. en büyük %1'i sabit bir üst sınıra
  çekmek; kural önceden yazılır;
- varyans azaltma (CUPED bölümü).

## Kısa ve uzun vade

Bazı metrikler hemen değişir (tıklama), bazıları geç (elde tutma). Kısa
vadeli bir metrik uzun vadeli amaca bağlı değilse yanıltabilir; bu konu
Yenilik Etkisi ve Uzun Vadeli Etki bölümünde.
