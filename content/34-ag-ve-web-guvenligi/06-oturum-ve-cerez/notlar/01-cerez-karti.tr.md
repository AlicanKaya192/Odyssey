## Doğru kurulmuş bir oturum çerezi

```text
Set-Cookie: session=<43 karakter>; Path=/; Max-Age=3600;
            Secure; HttpOnly; SameSite=Lax
```

## Öznitelikler

| Öznitelik | Neye karşı? | Oturum çerezinde |
|---|---|---|
| `Secure` | Yolda okunma (düz HTTP) | Açık |
| `HttpOnly` | Sayfadaki betiğin okuması (XSS) | Açık |
| `SameSite=Lax` | Başka siteden başlatılan istek (CSRF) | Açık (`Strict` daha sıkı) |
| `Max-Age` | Çerezin sonsuz yaşaması | Kısa |
| `Domain` | Fazla alt alana gitmesi | Yazılmaz (yalnızca kendi ana bilgisayarı) |

`SameSite=None` yalnızca `Secure` ile birlikte kabul edilir ve gerçekten
başka sitelerden kullanılması gereken çerezler içindir.

## Oturum kimliği

- `secrets.token_urlsafe(32)`: 256 bit, 43 karakter.
- Sayaç, zaman, kullanıcı adı ya da `random` ile **üretilmez**.
- URL'de taşınmaz (geçmişe, kayıtlara, `Referer`'a yazılır).
- Kayıtlara (log) yazılmaz.

## Yaşam döngüsü

| An | Yapılacak |
|---|---|
| Giriş | Yeni kimlik üret, eskisini sil (sabitlemeye karşı) |
| Yetki değişimi | Kimliği yenile |
| Her istek | Boşta kalma ve mutlak süreyi denetle |
| Çıkış | Sunucudaki kaydı sil, çerezi sil |
| Parola değişimi | Diğer bütün oturumları kapat |

## İmzalı çerez

- Durum çerezde tutuluyorsa HMAC ile imzalanır, `compare_digest` ile
  doğrulanır.
- İmza **gizlemez**; gizli bilgi çereze yazılmaz.
- İçine son geçerlilik zamanı konur; sunucu tek başına geri çağıramaz.
