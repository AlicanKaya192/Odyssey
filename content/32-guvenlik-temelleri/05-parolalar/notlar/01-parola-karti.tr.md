## Formüller

- Rastgele parola: **entropi = uzunluk × log2(alfabe)** bit.
- Rastgele kelimeler: **entropi = kelime sayısı × log2(liste uzunluğu)**;
  7776 kelimelik listede kelime başına 12,92 bit.
- Ortalama deneme sayısı: **2^(bit − 1)**; süre = deneme / hız.

## Alfabeler

| Alfabe | Karakter sayısı | Karakter başına bit |
|---|---|---|
| Rakamlar | 10 | 3,32 |
| Küçük harfler | 26 | 4,70 |
| Harf ve rakam | 62 | 5,95 |
| Yazdırılabilir ASCII | 94 | 6,55 |

## Saldırı türleri

| Saldırı | Ne yapar | Savunma |
|---|---|---|
| Çevrimiçi tahmin | Giriş sayfasında dener | Deneme sınırı, bekleme, MFA |
| Çevrimdışı tahmin | Çalınan özetleri kendi makinesinde dener | Yavaş özet fonksiyonu, tuz (Parolaları Saklamak) |
| Sözlük saldırısı | Gerçek parolaları ve kalıpları dener | Sızmış parola listesiyle denetim |
| Kimlik bilgisi doldurma | Başka siteden sızanı dener | Her yerde ayrı parola, MFA |

## Python

```python
import secrets
import string

alphabet = string.ascii_letters + string.digits
password = "".join(secrets.choice(alphabet) for _ in range(16))
token = secrets.token_urlsafe(16)
```

- `secrets.choice`, `secrets.token_urlsafe`, `secrets.token_hex`: güvenli.
- `random.choice`, `random.randint`: tahmin edilebilir; parola, jeton,
  doğrulama kodu için **kullanılmaz**.

## Kural (bugünkü kılavuzlar)

- Uzunluk esas; en az 8, tercihen 12 ve üstü; en az 64 karaktere izin.
- Sızmış ve yaygın parolaları reddet.
- Zorunlu karakter türü ve düzenli değiştirme yok; yalnızca sızıntıda
  değiştir.
- Yapıştırmaya ve parola yöneticisine izin ver.
