`PUT` ile `PATCH` ikisi de "değiştir" demek; fark neyin gönderildiğinde.

| | `PUT` | `PATCH` |
|---|---|---|
| Gövde | Kaydın **tamamı** | Yalnızca değişen alanlar |
| Model | Zorunlu alanlı (`BookIn`) | Hepsi isteğe bağlı (`BookPatch`) |
| Eksik alan | `422` | Dokunulmaz |
| Kodda | `books[id] = {...}` | `record.update(patch.model_dump(exclude_unset=True))` |

## Aynı isteği iki kez göndermek

`PUT /books/2 {"title": "Persuasion", "year": 1817}` iki kez gönderilse de
sonuç aynı: kayıt o hâle gelir. Buna **idempotent** (tekrara dayanıklı)
denir. `GET`, `PUT`, `DELETE` böyledir: ağ kopup istemci isteği yeniden
gönderirse zarar olmaz. (`DELETE` ikinci kez `404` döner ama kayıt yine
silinmiş durumdadır.)

`POST` değildir: iki kez gönderilen `POST /books` iki kitap oluşturur.
API Kullanmak modülündeki yeniden deneme kuralı buradan geliyor: `POST`'u körü körüne
tekrar etme.

## `exclude_unset`, `exclude_none`, `exclude_defaults`

| Gönderilen | `exclude_unset=True` | `exclude_none=True` |
|---|---|---|
| `{"year": 1966}` | `{"year": 1966}` | `{"year": 1966}` |
| `{"title": null}` | `{"title": None}` | `{}` |
| `{}` | `{}` | `{}` |

`exclude_unset` istemcinin bilerek gönderdiği `null`'u korur; `exclude_none`
atar. `PATCH`'te doğru olan `exclude_unset`. Bir alan `null` olamıyorsa
(`title` gibi) gönderilen `null`'u doğrulayıcıyla `422` yap (derste); kural
(`min_length=1`) `None`'a uygulanmaz, onu durdurmaz.

## `PATCH` ile boş gövde

`PATCH /books/1 {}` → hiçbir şey değişmez, kayıt olduğu gibi döner (`200`).
Hata vermek istersen: `if not changes: raise HTTPException(400, ...)`.
