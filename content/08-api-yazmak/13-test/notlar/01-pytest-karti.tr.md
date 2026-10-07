pytest ile API testinde en sık kullanılanlar.

## Komutlar (terminalde)

| Komut | Ne yapar? |
|---|---|
| `pytest` | Klasördeki bütün `test_*.py` dosyalarını çalıştırır |
| `pytest -q` | Kısa çıktı |
| `pytest test_main.py` | Tek dosya |
| `pytest -k missing` | Adında `missing` geçen testler |
| `pytest -x` | İlk düşen testte dur |

Bilgisayarındaki ortamda `pip install pytest` gerekir; Odyssey'nin
alıştırma ortamında hazır.

## `assert` kalıpları

```python
assert r.status_code == 201
assert r.json() == {"id": 1, "title": "Dune", "year": 1965}   # tamamı
assert r.json()["title"] == "Dune"                            # tek alan
assert "id" in r.json()                                       # alan var mı
assert len(r.json()) == 3                                     # liste boyu
assert r.headers["location"] == "/books/1"                    # başlık
```

Bilinmeyen değerler (jeton, zaman) için tamamını değil, varlığını ya da
biçimini dene: `assert len(r.json()["access_token"]) == 32`.

## Fixture'lar

```python
@pytest.fixture
def client():
    return TestClient(app)


def test_home(client):          # parametre adı = fixture adı
    assert client.get("/").status_code == 200
```

`autouse=True` olmayan fixture yalnızca onu parametre olarak isteyen teste
verilir.

## Test adları

`test_` + ne denendiği: `test_missing_book_returns_404`,
`test_duplicate_email_is_409`. Düşünce adı okuyan neyin bozulduğunu anlar.

## Yaygın hatalar

| Hata | Sonuç |
|---|---|
| İşlev adı `test_` ile başlamıyor | pytest onu görmez; "no tests" |
| `assert` yerine `print` | Test hiçbir zaman düşmez |
| Testler paylaşılan durumu temizlemiyor | Sonuç sıraya bağlı |
| `dependency_overrides` temizlenmiyor | Sonraki testler sahteyle çalışır |
