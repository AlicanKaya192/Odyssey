API 1'in tamamı tek sayfada.

## requests

| İş | Kod |
|---|---|
| Getir | `requests.get(url, params=..., headers=..., timeout=10)` |
| Oluştur | `requests.post(url, json=..., headers=AUTH)` → `201` |
| Kısmen değiştir | `requests.patch(url, json=..., headers=AUTH)` → `200` |
| Tamamen değiştir | `requests.put(url, json=..., headers=AUTH)` → `200` |
| Sil | `requests.delete(url, headers=AUTH)` → `204` |
| Oturum | `s = requests.Session(); s.headers.update({...})` |
| Kod | `r.status_code`, `r.ok`, `r.raise_for_status()` |
| Gövde | `r.json()`, `r.text` |
| Gidilen adres | `r.url`, `r.request.headers` |

## Kimlik

| Yöntem | Başlık |
|---|---|
| API anahtarı | `X-API-Key: ...` (ada API karar verir) |
| Bearer | `Authorization: Bearer <jeton>` |
| Basic | `auth=(ad, şifre)` |

Anahtar: `os.environ.get("AD")`; `.env` git'e girmez.

## Kodlar

`200` tamam · `201` oluşturuldu · `204` gövdesiz tamam · `400` bozuk istek ·
`401` tanınmıyorsun · `403` izin yok · `404` yok · `405` bu yöntem yok ·
`422` değerler geçersiz · `429` yavaşla · `500` sunucu hatası ·
`503` şu an hizmet yok

## Sayfalama

| Biçim | Durma koşulu |
|---|---|
| `page` | `page >= meta.pages` ya da boş sayfa |
| `next` | `links.next` `None` |
| `offset` + `limit` | `offset >= total` |
| `cursor` | `next_cursor` `None` |

## Dayanıklılık

- Her istekte `timeout`.
- Yeniden dene: `Timeout`, `ConnectionError`, `5xx`, `429` (`Retry-After`).
- Yeniden deneme: `4xx`; otomatik `POST`.
- Bekleme: 1, 2, 4... saniye; üst sınır.
- Hız: istekler arasında en az `pencere / izin` saniye.

## Veri hattı

Çek → sakla (önbellek) → düzleştir → denetle (`assert`) → yaz (`"w"`).
Güncelleme artımlı: `since` + kimliğe göre birleştir.
