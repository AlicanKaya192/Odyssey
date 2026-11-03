## Hata ve savunma

| Hata | Savunma |
|---|---|
| Farklı hata mesajları (kullanıcı adı numaralandırma) | Tek mesaj; bilinmeyen kullanıcı için de özet hesapla |
| Sınırsız deneme (kaba kuvvet) | Hesap ve kaynak başına sınır, artan bekleme |
| Kimlik bilgisi doldurma | MFA, kaynak başına izleme, sızmış parola listesi |
| Hesabı tamamen kilitlemek | Artan bekleme (kilit hizmet engellemeye kapı açar) |
| Tahmin edilebilir sıfırlama jetonu | `secrets`, kısa ömür, tek kullanım, sunucuda özet |
| Zayıf parola kuralı | En az uzunluk, bilinen kötü parolaların reddi |
| Varsayılan parola | Kurulumda değiştirmeyi zorunlu kıl |
| Atlanabilen MFA | İkinci adım sunucuda denetlenir |

## Artan bekleme

| Hata sayısı | 1 | 2 | 3 | 4 | 5 | 10 | 11 |
|---|---|---|---|---|---|---|---|
| Bekleme (sn) | 0 | 0 | 1 | 2 | 4 | 128 | 256 |

Kural: 3 hatadan sonra `2 ** (hata - 3)` saniye, en çok 300.

## Sıfırlama jetonu

- `secrets.token_urlsafe(32)`
- Sunucuda `hashlib.sha256(token.encode()).hexdigest()`
- Ömür kısa (ör. 900 saniye), tek kullanım (`used`)
- `hmac.compare_digest` ile karşılaştırma
- Başarılı sıfırlamadan sonra öteki oturumlar kapanır

## Mesajlar

| Durum | Kullanıcının gördüğü |
|---|---|
| Yanlış ad ya da parola | "Kullanıcı adı ya da parola yanlış" |
| Sıfırlama isteği | "Bu adres kayıtlıysa bağlantı gönderdik" |
| Çok fazla deneme | "Bir süre sonra yeniden deneyin" |
