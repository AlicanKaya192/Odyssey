## SSRF bir bakışta

| Soru | Cevap |
|---|---|
| Ne olur? | Sunucu, kullanıcının verdiği adrese kendi adına istek atar |
| Neden tehlikeli? | Sunucu içeride; dışarıdan erişilemeyen adreslere ulaşır |
| Hangi özellikler? | Resim getirme, bağlantı önizleme, web kancası, dosya içe aktarma |
| Bulutta özel risk | Bağlantı yerel aralıktaki (`169.254.0.0/16`) meta veri hizmeti |

## Reddedilecek adresler

| Tür | `ipaddress` özelliği | Örnek |
|---|---|---|
| Geri döngü | `is_loopback` | `127.0.0.1` |
| Özel | `is_private` | `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` |
| Bağlantı yerel | `is_link_local` | `169.254.0.0/16` |
| Belirtilmemiş | `is_unspecified` | `0.0.0.0` |
| Ayrılmış | `is_reserved` | `240.0.0.0/4` |

## Python kalıpları

- Ayrıştır: `parts = urlsplit(url)`; `parts.scheme`, `parts.hostname`,
  `parts.port`.
- Şema: `parts.scheme in ("http", "https")`.
- İzin listesi: `parts.hostname in ALLOWED_HOSTS` (birebir eşitlik).
- IP denetimi: adı çöz, `ipaddress.ip_address(...)`, iç adres özellikleri.
- Çözülemeyen ya da geçersiz adres: reddet.

## Kurallar

- Metin araması (`startswith`, `in`) ile adres denetlenmez.
- Denetim **çözümlemeden sonra** IP üzerinde yapılır; bağlantı
  **denetlenen IP'ye** kurulur.
- Yönlendirme izlenmez ya da her adım yeniden denetlenir.
- Getirme bileşenine çıkış süzmesi; iç ağa ve meta veri adresine yolu yok.
- Cevap türü, boyutu ve zaman aşımı sınırlı; hata ayrıntısı gösterilmez.
