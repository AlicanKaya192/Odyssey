Dört sayfalama biçiminin hazır döngüleri. Alıştırma sunucusunda çalışıyorlar;
başka API'de alan adlarını belgeye göre değiştir.

## Sayfa numarası

```python
items, page = [], 1
while True:
    body = requests.get(BASE + "/books", params={"page": page, "per_page": 20}).json()
    items.extend(body["data"])
    if page >= body["meta"]["pages"]:
        break
    page += 1
```

`pages` yoksa: `if not body["data"]: break`.

## Sonraki bağlantısı

```python
items, url = [], BASE + "/books"
while url:
    body = requests.get(url).json()
    items.extend(body["data"])
    nxt = body["links"]["next"]
    url = BASE + nxt if nxt else None
```

## Ofset + sınır

```python
items, offset = [], 0
while True:
    params = {"offset": offset, "limit": 20}
    body = requests.get(BASE + "/offset/books", params=params).json()
    items.extend(body["items"])
    offset += body["limit"]
    if offset >= body["total"]:
        break
```

## İmleç

```python
items, cursor = [], None
while True:
    params = {"cursor": cursor} if cursor else {}
    body = requests.get(BASE + "/cursor/books", params=params).json()
    items.extend(body["results"])
    cursor = body["next_cursor"]
    if cursor is None:
        break
```

## Hangisi ne zaman

| Biçim | İyi yanı | Zayıf yanı |
|---|---|---|
| Sayfa numarası | Kolay; istediğin sayfaya atlarsın | Liste değişirken kayıt kayar |
| Sonraki bağlantısı | Hesap yok, sunucu söylüyor | Belli bir sayfaya doğrudan atlanmaz |
| Ofset + sınır | Veritabanına yakın, esnek | Çok büyük ofsetler yavaş olabilir |
| İmleç | Değişen listede tutarlı | Geri dönmek ve atlamak zor |

## Güvenlik sınırı

```python
for page in range(1, 500):      # en fazla 499 sayfa
    ...
    if son_sayfa:
        break
```

`while True` yerine üst sınırlı bir `for` kullanmak, durma koşulu bir gün
bozulursa sonsuz istek atmanı engeller.
