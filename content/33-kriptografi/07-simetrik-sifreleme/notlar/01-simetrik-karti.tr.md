## İki tür

| | Akış şifresi | Blok şifresi |
|---|---|---|
| Nasıl | Anahtar dizisiyle XOR | Sabit bloklarda karıştırma |
| Dolgu | İstemez | İster (PKCS#7) |
| Örnek | ChaCha20 | AES |
| Kökeni | Tek kullanımlık şifre | Yer değiştirme + yer karıştırma |

## Nonce / IV

- Aynı anahtarın birçok mesajda kullanılmasını sağlar.
- **Benzersiz** olmalı; gizli olması gerekmez.
- **Asla** aynı anahtarla iki kez kullanılmaz (yoksa tekrar-anahtar hatası).
- Şifreli metnin yanında açıkça gönderilir.

## PKCS#7 dolgu

- Eksik bayt sayısı kadar, her biri o sayıya eşit bayt eklenir.
- Tam blok uzunluğundaki mesaja bile **yeni bir tam blok** eklenir.
- Çözerken son bayt dolgu uzunluğunu söyler: `data[:-data[-1]]`.

## AES

- Anahtar 128 / 192 / 256 bit; blok her zaman 128 bit (16 bayt).
- Standart kütüphanede **yok**; kütüphaneyle, doğrulanmış kipte (AES-GCM).
- İçi: yer değiştirme + yer karıştırma, birçok tur.

## Kurallar

- Kendi simetrik şifreni yazma.
- Tek başına şifreleme bütünlük sağlamaz; doğrulanmış şifreleme kullan.
- Anahtar en az 128 bit, rastgele.
