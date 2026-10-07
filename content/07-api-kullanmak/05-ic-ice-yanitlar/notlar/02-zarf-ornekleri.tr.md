Farklı API'ler kayıtları farklı zarflara koyuyor. En sık görülen biçimler ve
kayıt listesine nasıl ulaşılacağı.

## 1. `data` + `meta`

```json
{"data": [{"id": 1}, {"id": 2}], "meta": {"page": 1, "total": 42}}
```

```python
items = response["data"]
```

## 2. `results` + sayfa bağlantıları

```json
{"count": 42, "next": "https://api.example.com/books?page=2",
 "previous": null, "results": [{"id": 1}, {"id": 2}]}
```

```python
items = response["results"]
```

`next` bir sonraki sayfanın adresi; `null` ise son sayfadasın (Bölüm 10).

## 3. Zarfsız liste

```json
[{"id": 1}, {"id": 2}]
```

```python
items = response
```

Yanıtın kendisi liste. Toplam ve sayfa bilgisi varsa başlıklarda gelir.

## 4. Kayıt adına göre anahtar

```json
{"books": [{"id": 1}], "total": 1}
```

```python
items = response["books"]
```

## 5. Tek kayıt

`/books/42` gibi tek bir kaynak istediğinde yanıt çoğu zaman liste değil,
kaydın kendisi:

```json
{"id": 42, "title": "Emma"}
```

Tabloya dökmek için tek elemanlı bir liste yapabilirsin: `items = [response]`.

## Nereden bileceksin?

- Belgedeki örnek yanıta bak.
- Yoksa ilk yanıtı `json.dumps(response, indent=2)` ile yazdır ve gözünle
  oku.
- Program içinde emin olmak için türüne bak: `isinstance(response, list)`.
