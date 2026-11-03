## Kim neyi korur?

| Katman | IaaS | PaaS | SaaS |
|---|---|---|---|
| Veri | Müşteri | Müşteri | Müşteri |
| Kimlikler ve erişim | Müşteri | Müşteri | Müşteri |
| Uygulama | Müşteri | Müşteri | Sağlayıcı |
| İşletim sistemi | Müşteri | Sağlayıcı | Sağlayıcı |
| Ağ ve sanallaştırma | Sağlayıcı | Sağlayıcı | Sağlayıcı |
| Fiziksel veri merkezi | Sağlayıcı | Sağlayıcı | Sağlayıcı |

## En sık yapılandırma hataları

| Hata | Denetim | Düzeltme |
|---|---|---|
| Herkese açık depolama alanı | `public` ve veri türü | Herkese açık erişimi hesap düzeyinde engelle |
| Şifresiz veri | `encrypted` | Varsayılan şifrelemeyi aç |
| Geniş joker izin (`*`) | Politika ifadeleri | İşlemleri tek tek yaz |
| Yönetim portu internete açık | `0.0.0.0/0` ve port | Kaynak adresi daralt, VPN |
| Yönetici hesabında çok faktörlü doğrulama yok | Hesap ayarı | Zorunlu yap |
| Eski erişim anahtarları | Anahtar yaşı | Yenile ya da kaldır |

## IAM değerlendirme sırası

1. İşleme uyan bütün ifadeler bulunur.
2. Bir tanesi bile `deny` ise **yasak**.
3. En az bir `allow` varsa **izin**.
4. Hiçbiri yoksa **yasak** (varsayılan olarak reddet).

## Python kalıpları

- Joker eşleşme: `fnmatch.fnmatchcase(islem, kalip)` (büyük-küçük harfe duyarlı).
- Yasak kazanır: `if "deny" in eslesenler: return False`.
- Bütün internet: `kaynak in ("0.0.0.0/0", "::/0")`.

## Akılda tutulacak

- Bulut sorumluluğu ortadan kaldırmaz, paylaştırır.
- Veri ve kimlikler her modelde müşterinindir.
- Yanlış yapılandırma en sık olay sebebidir; kod olarak altyapı onu
  kurulumdan önce yakalar.
