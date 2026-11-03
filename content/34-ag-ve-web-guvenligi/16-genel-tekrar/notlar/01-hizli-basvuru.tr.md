## Ağ

| Konu | Hatırla |
|---|---|
| Özel aralıklar | `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`; geri döngü `127.0.0.0/8` |
| CIDR | `/24` → 256 adres; her ek bit yarıya indirir |
| TCP / UDP | Güvenilir, el sıkışmalı / hızlı, garantisiz |
| Güvenlik duvarı | İlk tutan kural; sonda varsayılan ret; çıkış süzmesi |
| Bölümleme | Bölgeler arası izin listesi; DMZ; sıfır güven |
| DNS | TTL kadar önbellek; DNSSEC bütünlük, DoT/DoH gizlilik |
| HTTPS | Gizlilik + bütünlük + sunucu kimliği; HSTS `max-age=31536000` |

## Web: saldırı → savunma

| Saldırı | Birinci savunma | Ek katman |
|---|---|---|
| SQL enjeksiyonu | Parametreli sorgu (`?`) | Ad için izin listesi, en az yetkili veritabanı kullanıcısı |
| XSS | Bağlama göre çıktı kodlama (`html.escape`) | CSP, `HttpOnly` |
| CSRF | Oturuma bağlı jeton + `compare_digest` | `SameSite=Lax`, `Origin` denetimi |
| SSRF | Ayrıştırılmış adresle izin listesi | İç adresleri IP üzerinde reddetmek, çıkış süzmesi |
| Bozuk erişim denetimi | Her nesnede sahiplik denetimi | `404` ile varlığı gizlemek |
| Kimlik bilgisi doldurma | Artan bekleme, MFA | Kaynak başına izleme |
| Yol geçişi | `normpath` + `startswith(BASE + "/")` | Rastgele dosya adı |
| Komut enjeksiyonu | Argüman listesi | `shlex.quote` |
| Toplu atama | Alan izin listesi | Reddedileni `422` ile bildirmek |
| Tıklama kaçırma | `frame-ancestors 'none'` | `X-Frame-Options: DENY` |

## Çerez ve başlık

| Ad | Değer |
|---|---|
| Oturum çerezi | `Secure; HttpOnly; SameSite=Lax` |
| CORS | İzin listesindeki köken + `Vary: Origin` |
| Tür | `X-Content-Type-Options: nosniff` |
| Yönlendiren | `Referrer-Policy: strict-origin-when-cross-origin` |

## Python araçları

| İş | Araç |
|---|---|
| Adres ve ağ | `ipaddress.ip_address`, `ip_network`, `in` |
| Adresi ayrıştırmak | `urllib.parse.urlsplit` (`.scheme`, `.hostname`, `.port`) |
| Biçim | `re.fullmatch` |
| Rastgele değer | `secrets.token_urlsafe(32)` |
| Karşılaştırma | `hmac.compare_digest` |
| İmza | `hmac.new(sır, ileti, hashlib.sha256)` |
| Kodlama | `html.escape`, `urllib.parse.quote(s, safe="")`, `json.dumps` |
