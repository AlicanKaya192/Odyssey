REST API'lerde adresler belli bir düzene göre yazılır. Kural değil, gelenek;
ama uyulursa API'ni kullanan kişi belgeye bakmadan tahmin edebilir.

## Ad, fiil değil

Adres **neyin** üzerinde çalışıldığını, yöntem **ne yapıldığını** söyler.

| Kötü | İyi |
|---|---|
| `POST /createBook` | `POST /books` |
| `GET /getBook?id=3` | `GET /books/3` |
| `POST /deleteBook/3` | `DELETE /books/3` |
| `POST /books/3/update` | `PATCH /books/3` |

## Çoğul ad

Koleksiyon çoğul: `/books`, `/users`. Tek kayıt koleksiyonun altında:
`/books/3`. İkisinde de aynı kelime.

## İç içe kaynak

Bir yazarın kitapları: `GET /authors/7/books`. Yeni kitabı o yazara
eklemek: `POST /authors/7/books`. Bir seviyeden derine inme;
`/authors/7/books/3/reviews/2` yerine `/reviews/2`.

## Süzme, sıralama, sayfalama sorguda

`GET /books?year=1965&sort=title&limit=20&offset=40`. Yeni adres açma
(`/books/by-year/1965`).

## Kodun cevabı

| İstek | Cevap |
|---|---|
| `POST /books` | `201`, yeni kayıt, `Location: /books/4` |
| `GET /books` | `200`, liste (boşsa `[]`, `404` değil) |
| `GET /books/4` | `200` ya da `404` |
| `PUT` / `PATCH /books/4` | `200`, güncel kayıt |
| `DELETE /books/4` | `204` |

Boş liste bir hata değil: "hiç kitap yok" da geçerli bir cevap.
