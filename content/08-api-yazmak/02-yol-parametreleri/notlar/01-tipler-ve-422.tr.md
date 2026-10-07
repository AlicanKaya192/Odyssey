Yol parametresinde yazdığın tipin ne kabul ettiği ve neyi `422` ile
reddettiği (ölçüldü).

| Tip | Kabul ettiği | Reddettiği | `type` |
|---|---|---|---|
| `int` | `/books/2` → `2` | `abc`, `2.5` | `int_parsing` |
| `float` | `/price/3` → `3.0`, `/price/1.5` → `1.5` | `abc` | `float_parsing` |
| `str` | Her şey (`%20` boşluğa çevrilir) | — | — |
| `bool` | `1`, `true`, `yes`, `on` → `true`; `0`, `false`, `no`, `off` → `false` | `maybe` | `bool_parsing` |

## 422 gövdesinin parçaları

```json
{"detail": [{
  "type": "float_parsing",
  "loc": ["path", "p"],
  "msg": "Input should be a valid number, unable to parse string as a number",
  "input": "abc"}]}
```

- `detail` bir **liste**: birden çok hata varsa her biri ayrı öğe.
- `loc` ilk öğesi nereden geldiğini söyler: `path` (adres), `query` (sorgu,
  Sorgu Parametreleri bölümü), `body` (gövde, İstek Gövdesi bölümü).
- `msg` İngilizce açıklama; `type` makinenin okuyacağı kısa ad.

## Eğik çizgi içeren değer

Normalde bir yol parametresi `/` içeremez. Dosya yolu gibi bir değer için
`:path` eki:

```python
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file_path": file_path}
```

`GET /files/docs/2024/report.txt` → `{"file_path": "docs/2024/report.txt"}`.

## Sık hatalar

| Belirti | Sebep |
|---|---|
| Her istek `422` ve `loc: ["query", "book_id"]` | Adreste `{book_id}` yok; FastAPI parametreyi sorgu sandı (adı iki yerde de aynı yaz) |
| `/books/latest` → `422` | Değişkenli yol önce yazılmış; sabit yolu üste al |
| `/books/2` bulunmuyor | Tip yazılmamış, `"2"` metin olarak aranıyor |
| `500` olmayan kayıtta | `HTTPException(404)` yerine `KeyError` |
