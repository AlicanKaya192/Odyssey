RSA'nın matematiği kısa, ama doğru kullanımı birçok ayrıntıya bağlı. Bu
liste, kütüphane seçerken ve ayarlarını okurken bakılacak noktalar.

## Kontrol listesi

| Konu | Doğrusu | Yanlışı |
|---|---|---|
| Anahtar boyu | En az 2048 bit; uzun ömürlü anahtar için 3072 | 512 ya da 1024 bit |
| Açık üs | 65537 | Çok küçük üs (ör. 3) ile dolgusuz şifreleme |
| Şifreleme dolgusu | OAEP | Dolgusuz (ders kitabı) RSA |
| İmza dolgusu | PSS | Dolgusuz imza |
| Büyük veri | Karma şifreleme: RSA yalnızca simetrik anahtarı taşır | Veriyi parça parça RSA ile şifrelemek |
| Anahtar üretimi | Denenmiş kütüphane, güvenli rastgelelik | Kendi asal üretecini yazmak |
| Özel anahtar | Şifreli dosyada ya da anahtar kasasında | Kodun içinde, depoda |
| Aynı anahtar çifti | Şifreleme ve imza için ayrı çiftler | Tek çifti her işe kullanmak |

## Karma şifreleme adımları

1. Rastgele bir simetrik anahtar üret (`secrets.token_bytes(32)`).
2. Veriyi bu anahtarla AES-GCM gibi doğrulanmış şifrelemeyle şifrele.
3. Simetrik anahtarı alıcının **açık** RSA anahtarıyla, OAEP ile şifrele.
4. İkisini birlikte gönder. Alıcı özel anahtarıyla simetrik anahtarı,
   onunla da veriyi çözer.

## RSA'nın yerini alanlar

Yeni sistemlerde anahtar değişimi için çoğunlukla eliptik eğri
Diffie-Hellman (X25519), imza için Ed25519 ya da ECDSA tercih ediliyor:
anahtarlar çok daha kısa, işlemler daha hızlı. RSA yine de sertifikalarda
ve eski sistemlerde yaygın.
