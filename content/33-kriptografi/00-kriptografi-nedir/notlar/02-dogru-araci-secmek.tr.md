Bir işe başlamadan önce sorulacak soru "hangi algoritma?" değil, **"neyi
korumak istiyorum?"**. Aynı kelimeleri karıştırmak en sık yapılan hatadır.

## Neye ihtiyacın var?

| İhtiyaç | Doğru araç | Yanlış seçim |
|---|---|---|
| Kimse okumasın | Şifreleme | Base64 ("okunmuyor nasılsa") |
| Değiştirilirse anlayayım | HMAC (ortak anahtar) ya da imza | Yalnızca düz özet: saldırgan veriyi değiştirip özeti de yeniden hesaplar |
| Parolayı sakla | Tuzlu, yavaş parola özeti | Şifreleme (anahtarı alan hepsini açar) ya da düz özet |
| Kimin gönderdiğini üçüncü kişiye kanıtla | Dijital imza | HMAC (anahtarı iki taraf da bildiği için ikisi de üretebilir) |
| Rastgele jeton ya da anahtar | `secrets`, `os.urandom` | `random` (tahmin edilebilir) |

## Üç soru

1. **Geri çevrilmesi gerekiyor mu?** Hayırsa özet; evetse şifreleme.
2. **Kim geri çevirecek?** Yalnızca anahtarı bilenler ise şifreleme; herkes
   ise kodlama (güvenlik değil).
3. **Kime kanıt gerekiyor?** Yalnızca iki taraf ise HMAC; üçüncü kişiye
   ise imza.

## Kurallar

- Yüksek düzeyli, denenmiş bir kütüphane kullan; düşük düzeyli parçaları
  kendin birleştirme.
- Anahtarları koda yazma; yapılandırmadan ya da bir sır kasasından oku.
- Algoritmanın adını değil, gizli tuttuğun şeyin **anahtar** olduğunu
  unutma.
