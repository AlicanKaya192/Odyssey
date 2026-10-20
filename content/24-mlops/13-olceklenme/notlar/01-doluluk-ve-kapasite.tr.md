Kapasite planı üç sayıyla başlar: gelen istek, işin süresi, çalışan sayısı.

## Hesap

- Doluluk = saniyedeki istek × işin süresi (saniye) ÷ çalışan sayısı.
- Örnek: saniyede 50 istek, 10 ms, 1 çalışan → 50 × 0,01 ÷ 1 = 0,5.
- Gereken çalışan: doluluk hedefin (örneğin 0,7) altına inene kadar
  çalışan ekle.

## Dersteki benzetim (iş ortalama 10 ms)

| Doluluk | Ortalama bekleme | p95 bekleme |
|---|---|---|
| 0,50 | 9,8 ms | 45,3 ms |
| 0,80 | 36,4 ms | 120,9 ms |
| 0,90 | 74,1 ms | 226,6 ms |
| 0,99 | 329,5 ms | 1131,2 ms |

## Aynı doluluk, daha çok çalışan (%90)

| Çalışan | Ortalama bekleme |
|---|---|
| 1 | 74,1 ms |
| 2 | 34,5 ms |
| 4 | 15,4 ms |

## Kontrol listesi

- Doluluk hedefi %100'ün altında, boşluklu mu?
- Sunucu durumsuz mu (her kopya aynı cevabı verir)?
- Gecikme sınırı p95 ile mi yazıldı (ortalama kuyruğu gizler)?

## Yapma

- Sunucuyu %100 doluluğa göre planlama; bekleme orada patlar.
- İstekler arasında sunucunun belleğinde müşteri bilgisi saklama;
  yatay ölçeklenme bozulur.
