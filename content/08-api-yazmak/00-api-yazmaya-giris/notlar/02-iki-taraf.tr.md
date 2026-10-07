API 1'de istemci tarafında öğrendiğin her şeyin sunucu tarafındaki
karşılığı. Bu modül boyunca bu tabloya dönebilirsin.

| Kavram | API 1: istemci (requests) | API 2: sunucu (FastAPI) | Bölüm |
|---|---|---|---|
| Yöntem ve adres | `requests.get(BASE + "/books")` | `@app.get("/books")` | 01 |
| Yol parametresi | `/books/42` adresini kurmak | `@app.get("/books/{book_id}")` + `book_id: int` | 02 |
| Sorgu parametresi | `params={"page": 2}` | `def list_books(page: int = 1)` | 03 |
| Gövde | `json={"title": "Dune"}` | `def add(book: Book)` (Pydantic modeli) | 04 |
| Doğrulama | 422 almak | Alan kuralları (`Field(min_length=1)`) | 05 |
| Durum kodu | `r.status_code` okumak | `status_code=201`, `HTTPException(404)` | 06, 08 |
| CRUD | GET / POST / PUT / DELETE göndermek | Dört uç nokta yazmak | 07 |
| Kimlik | `headers={"Authorization": ...}` | Başlığı okuyup denetlemek | 10 |
| Sayfalama | `page` ile sayfa sayfa çekmek | `page`, `per_page` ile dilimlemek | 03, 09 |
| Hız sınırı, yeniden deneme | 429 ve 5xx'te beklemek | Doğru kodu doğru zamanda vermek | 08 |
| Belge | Belgeyi okumak | `/docs` kendiliğinden | 15 |
| Test | Cevabı `print` ile görmek | `TestClient` ve pytest | 13 |

Akılda kalsın: istemci olarak "bu API ne yapar?" diye soruyordun; sunucu
olarak "bu API ne söz veriyor?" diye soracaksın. Her uç nokta bir söz:
şu adrese şu istek gelirse şu kodla şu cevap.
