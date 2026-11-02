## Terimler

| Terim | Tek satır |
|---|---|
| Düz metin (plaintext) | Korunacak mesaj |
| Şifreli metin (ciphertext) | Şifrelemenin çıktısı |
| Anahtar (key) | Tek gizli parça |
| Kodlama (encoding) | Anahtarsız, herkes geri çevirir (Base64, hex) |
| Özet (hash) | Sabit uzunlukta parmak izi, geri dönmez |
| Simetrik | Aynı anahtarla şifrele ve çöz |
| Asimetrik | Açık anahtarla şifrele, özel anahtarla çöz |
| Kaba kuvvet (brute force) | Bütün anahtarları tek tek denemek |

## Kerckhoffs ilkesi

Algoritma açık olabilir; güvenlik yalnızca anahtarın gizliliğine dayanır.

## Anahtar uzunluğu

- `n` bit = `2ⁿ` anahtar; her ek bit kaba kuvveti iki katına çıkarır.
- Saniyede 10¹² denemede 40 bit yaklaşık 1 saniye, 56 bit yaklaşık 20
  saat, 128 bit 10¹⁹ yıldan fazla.
- Simetrik anahtar için bugünkü alt sınır 128 bit.

## Akılda tutulacak

- Base64 şifreleme değildir.
- Kriptografi erişilebilirlik sağlamaz; anahtar kaybolursa veri de gider.
- Gerçek uygulamada kendi algoritmanı ya da protokolünü yazma.
