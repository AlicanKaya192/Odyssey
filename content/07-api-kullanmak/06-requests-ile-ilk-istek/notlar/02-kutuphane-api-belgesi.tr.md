Bu patikanın alıştırma sunucusunun belgesi. Her API'de olduğu gibi, bir
alıştırmaya başlamadan önce buraya bakabilirsin. Taban adres:

```text
http://api.odyssey.test
```

## Kitaplar

| İstek | Ne yapar |
|---|---|
| `GET /books` | Kitap listesi (sayfalı, 5'er) |
| `GET /books/<id>` | Tek kitap; yoksa `404` |
| `POST /books` | Yeni kitap (jeton gerekir) → `201` |
| `PUT /books/<id>` | Kitabı tamamen değiştir (jeton) |
| `PATCH /books/<id>` | Kitabın bazı alanlarını değiştir (jeton) |
| `DELETE /books/<id>` | Kitabı sil (jeton) → `204` |

`GET /books` sorgu parametreleri: `author`, `tag`, `year_min`, `year_max`,
`q` (başlıkta geçen kelime), `sort` (`title`, `year`, `price`; önüne `-`
konursa büyükten küçüğe), `page`, `per_page` (en fazla 20).

Liste yanıtı:

```json
{"data": [...], "meta": {"page": 1, "per_page": 5, "total": 23, "pages": 5},
 "links": {"next": "/books?page=2", "prev": null}}
```

Bir kitap:

```json
{"id": 1, "title": "Emma", "author_id": 1, "year": 1815, "price": 12.5,
 "tags": ["classic", "novel"], "updated": "2024-01-10",
 "author": {"id": 1, "name": "Austen", "country": "UK"}}
```

## Yazarlar

| İstek | Ne yapar |
|---|---|
| `GET /authors` | Bütün yazarlar |
| `GET /authors/<id>` | Tek yazar |
| `GET /authors/<id>/books` | O yazarın kitapları |

## Kimlik

| Nerede | Değer | Nerede gerekiyor |
|---|---|---|
| `Authorization: Bearer letmein` | Jeton | Kitap ekleme, değiştirme, silme; `/me` |
| `X-API-Key: demo-key-123` | Okuyucu anahtarı | `/stats` |
| `X-API-Key: admin-key-999` | Yönetici anahtarı | `/admin/report` |
| Basic: `reader` / `pass123` | Kullanıcı adı ve şifre | `/basic` |

Bu değerler yalnızca alıştırma sunucusu için; gerçek bir API'nin
anahtarını koda yazmamayı Bölüm 08'de göreceğiz.

## Diğer uç noktalar

| İstek | Ne yapar |
|---|---|
| `GET /status` | Düz metin `ok` |
| `GET /offset/books` | `offset` + `limit` ile sayfalama |
| `GET /cursor/books` | İmleçle (`cursor`) sayfalama |
| `GET /flaky` | İlk iki istekte `503`, sonra `200` |
| `GET /broken` | Her zaman `500` |
| `GET /slow` | Yanıtı 3 saniye sonra veriyor |
| `GET /limited` | Saniyede 3 istek; fazlasına `429` |
| `GET /changes?since=2024-03-01` | O tarihten sonra değişen kitaplar |
| `GET /openapi.json` | Bu API'nin makine okunur belgesi |

Sunucu her çalıştırmada baştan başlıyor: eklediğin ya da sildiğin kitaplar
bir sonraki çalıştırmada eski hâline dönüyor.
