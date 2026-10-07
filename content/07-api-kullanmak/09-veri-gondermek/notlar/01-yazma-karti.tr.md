Yazan isteklerin hepsi, beklenen kodlarıyla.

| İş | İstek | Gövde | Başarı kodu | Yanıt gövdesi |
|---|---|---|---|---|
| Oluştur | `POST /books` | Yeni kayıt | `201` | Kaydın son hâli + `Location` |
| Kısmen değiştir | `PATCH /books/<id>` | Yalnızca değişen alanlar | `200` | Kaydın son hâli |
| Tamamen değiştir | `PUT /books/<id>` | Kaydın tamamı | `200` | Kaydın son hâli |
| Sil | `DELETE /books/<id>` | Yok | `204` | Boş |

## requests

```python
r = requests.post(url, json=veri, headers=AUTH)
r = requests.patch(url, json={"price": 8.99}, headers=AUTH)
r = requests.put(url, json=tam_kayit, headers=AUTH)
r = requests.delete(url, headers=AUTH)
```

## `json=` mi `data=` mı?

| | `json=` | `data=` |
|---|---|---|
| Gövde | JSON metni | `ad=değer&...` |
| `Content-Type` | `application/json` | `application/x-www-form-urlencoded` |
| Ne zaman | API JSON istiyorsa (çoğu) | Web formu bekleyen eski API'ler |

## Hata kodları

| Kod | Anlam | Bakılacak |
|---|---|---|
| `400` | Gövde okunamıyor | JSON bozuk mu, `json=` mi kullandın? |
| `401` | Jeton yok / geçersiz | `Authorization` başlığı |
| `403` | Bu işlem için yetki yok | Jetonun yetkisi |
| `404` | Kayıt yok | Adresteki kimlik |
| `405` | Bu adreste bu yöntem yok | `Allow` başlığı; liste mi tek kayıt mı? |
| `409` | Çakışma (aynı kayıt zaten var) | Önce var mı diye bak |
| `422` | Değerler kurallara uymuyor | Gövdedeki `detail` |

## Dikkat

- `204` yanıtında `r.json()` çağırma; gövde boş.
- `POST`'u otomatik tekrarlama: kopya kayıt oluşur.
- `PUT` ile yalnızca bir alan gönderme: diğer alanlar kaybolabilir.
