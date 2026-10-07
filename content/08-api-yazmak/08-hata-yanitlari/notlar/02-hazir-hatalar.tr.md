FastAPI'nin senin yazmadığın hataları; hepsi ölçüldü.

| Durum | Kod | Gövde |
|---|---|---|
| Adres hiç yok (`GET /nothing`) | `404` | `{"detail": "Not Found"}` |
| Adres var, yöntem yok (`DELETE /items/pen`) | `405` | `{"detail": "Method Not Allowed"}` |
| Parametre/gövde kalıba uymuyor | `422` | `{"detail": [{"type", "loc", "msg", "input"}]}` |
| Kodunda yakalanmamış hata (`1 / 0`) | `500` | Düz metin `Internal Server Error` |

## Kendi `404`'ünle karıştırma

`GET /nothing` → `{"detail": "Not Found"}` (adres yok).
`GET /items/xyz` → `{"detail": "Item not found"}` (adres var, kayıt yok).

İkisi de `404`. İstemci farkı `detail`'den anlar; bu yüzden kendi
mesajında neyin bulunamadığını söyle (`"Item not found"`, `"User not
found"`).

## `422` gövdesini okumak

```json
{"detail": [{"type": "int_parsing", "loc": ["query", "x"],
             "msg": "Input should be a valid integer, ...", "input": "abc"}]}
```

| Alan | Anlamı |
|---|---|
| `type` | Hatanın türü (makine için) |
| `loc` | Nerede: `["query", "x"]`, `["body", "year"]` |
| `msg` | Açıklama (insan için) |
| `input` | Gelen değer |

## `500` olunca

İstemci yalnızca `Internal Server Error` görür. Asıl bilgi sunucunun
terminalinde (ya da günlüğünde): hangi dosya, hangi satır, hangi hata.
Odyssey'de alıştırmayı **Çalıştır**'la denediğinde terminal de hatanın
hangi dosyanın hangi satırında çıktığını yazıyor.
