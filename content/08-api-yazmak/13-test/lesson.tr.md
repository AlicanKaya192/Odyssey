# API'yi Test Etmek

Bir uç noktayı değiştirdin; başka bir yeri bozmadığını nasıl bileceksin?
`/docs`'ta her isteği elle denemek her değişiklikte yorucu ve unutkan.
Bunun yerine istekleri ve beklenen cevapları **kod** olarak yazarsın; bir
komutla hepsi saniyeler içinde çalışır. Bu bölümde **pytest** ve FastAPI'nin
**TestClient**'ı ile API'nin testlerini yazıyorsun.

Odyssey'de alıştırmaları denetleyen de tam olarak budur: her alıştırmanın
arkasında senin koduna istek atan testler var. Şimdi masanın öbür
tarafındasın.

## İlk test

`main.py`'de bir kitap API'si olsun. Yanına `test_main.py`:

```python
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_add_book():
    r = client.post("/books", json={"title": "Dune", "year": 1965})
    assert r.status_code == 201
    assert r.json() == {"id": 1, "title": "Dune", "year": 1965}


def test_read_missing():
    r = client.get("/books/99")
    assert r.status_code == 404
    assert r.json()["detail"] == "Book not found"
```

- `TestClient(app)`: sunucu açmadan, uygulamayı **aynı süreçte**
  çağıran bir istemci. API 1'deki `requests` ile aynı yazım: `client.get`,
  `client.post(..., json=...)`, `r.status_code`, `r.json()`.
- Adı `test_` ile başlayan her işlev bir test. pytest onları kendisi
  buluyor.
- `assert koşul`: koşul yanlışsa test **düşer**.

Çalıştırmak için terminalde `pytest` (Odyssey'de alıştırmayı
**Çalıştır**'la). Hepsi geçince:

```text
......                                                    [100%]
6 passed in 0.39s
```

Her nokta geçen bir test.

## Düşen test neye benzer?

```text
..F...                                                    [100%]
_____________________ test_first_id_again _____________________
    def test_first_id_again():
        r = client.post("/books", json={"title": "Emma", "year": 1815})
>       assert r.json()["id"] == 1
E       assert 2 == 1
FAILED test_main.py::test_first_id_again - assert 2 == 1
1 failed, 5 passed in 0.59s
```

pytest hangi satırın düştüğünü (`>`) ve iki tarafın değerini (`2 == 1`)
gösteriyor. Bu çıktıyı ölçtük (sayfaya sığsın diye çizgileri kısalttık);
neden düştüğü bir sonraki başlıkta.

<figure class="fig">
  <div class="flow">
    <span class="node">test_main.py<br><small>client.post(...)</small></span><span class="arrow">→</span>
    <span class="node acc">TestClient<br><small>sunucu yok</small></span><span class="arrow">→</span>
    <span class="node">main.app</span><span class="arrow">→</span>
    <span class="node ok">assert<br><small>201? doğru gövde?</small></span>
  </div>
  <figcaption>Testler uygulamayı aynı süreçte çağırıyor; her <code>assert</code> bir beklentiyi denetliyor. Biri tutmazsa test düşüyor ve pytest hangi satır olduğunu gösteriyor.</figcaption>
</figure>

## Testler birbirini etkilememeli

Yukarıdaki test tek başına çalışsa geçerdi. Düştü, çünkü daha önceki
`test_add_book` `books` sözlüğüne Dune'u eklemişti ve sözlük testler
arasında **paylaşılıyor**. Testin sonucu sıraya bağlı oldu: kötü test.

Çözüm: her testten önce durumu temizleyen bir **fixture**:

```python
import pytest

from main import books


@pytest.fixture(autouse=True)
def clean():
    books.clear()
    yield
    books.clear()
```

- `@pytest.fixture`: testlerden önce/sonra çalışan hazırlık işlevi.
- `autouse=True`: her teste kendiliğinden uygulanıyor.
- `yield`: bağımlılıklardaki gibi; öncesi testten önce, sonrası testten
  sonra.

Fixture eklenince aynı altı test `6 passed` (ölçtük).

## Aynı testi birçok girdiyle: `parametrize`

```python
@pytest.mark.parametrize("body", [
    {"title": "X"},
    {"year": 1},
    {"title": "X", "year": "old"},
])
def test_bad_bodies(body):
    assert client.post("/books", json=body).status_code == 422
```

Bir işlev, üç test: pytest her girdi için ayrı çalıştırıyor ve ayrı
raporluyor. Sınır değerlerini (`0`, `1`, en büyük, en büyüğün bir fazlası)
böyle denemek kolay.

## Bağımlılığı testte değiştirmek

Bağımlılıklar bölümünde gördüğün `dependency_overrides` testte işe yarıyor:

```python
from main import app, require_key


def test_stats_without_real_key():
    app.dependency_overrides[require_key] = lambda: None
    try:
        assert client.get("/admin/stats").status_code == 200
    finally:
        app.dependency_overrides.clear()
```

Gerçek anahtar denetimi yerine "her zaman geçer" verdin. Aynı yolla gerçek
veritabanı yerine boş, geçici bir veritabanı verilir. `finally` içinde
temizlemek şart; yoksa sonraki testler de sahte bağımlılıkla çalışır.

## İyi bir test neyi dener?

| Dene | Örnek |
|---|---|
| Başarılı yol | `POST` → `201` ve doğru gövde |
| Bulunamayan | olmayan numara → `404` |
| Bozuk girdi | eksik alan, yanlış tip → `422` |
| Sınırlar | `limit=0`, `limit=50`, `limit=51` |
| Kimlik | anahtarsız → `401`, yanlış rol → `403` |
| Akış | ekle → oku → sil → oku (`404`) |

Bir test **bozuk kodu yakalayabilmeli**. Odyssey bunu da ölçüyor: testlerin
uygulamanın kasıtlı bozulmuş bir hâline karşı da çalıştırılıyor; hepsi
yine geçerse "testlerin bu hatayı görmüyor" diyor.

## Özet

- `TestClient(app)`: sunucusuz istemci; `requests` gibi yazılır.
- `def test_...():` + `assert`; pytest kendisi bulur ve çalıştırır.
- Paylaşılan durum testleri birbirine bağlar: `@pytest.fixture(autouse=True)`
  ile temizle.
- `@pytest.mark.parametrize`: aynı test, birçok girdi.
- `app.dependency_overrides` ile sahte bağımlılık; sonra `clear()`.
- İyi test başarılı yolu da hataları da dener ve bozuk kodda düşer.
