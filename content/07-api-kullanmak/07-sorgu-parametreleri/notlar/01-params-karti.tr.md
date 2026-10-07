`params=` ile sorgu kurmanın bütün durumları.

| Sözlük | Giden sorgu |
|---|---|
| `{"author": "Austen"}` | `?author=Austen` |
| `{"q": "the lighthouse"}` | `?q=the+lighthouse` |
| `{"q": "fish & chips"}` | `?q=fish+%26+chips` |
| `{"per_page": 3}` | `?per_page=3` |
| `{"tag": ["scifi", "humor"]}` | `?tag=scifi&tag=humor` |
| `{"author": "Orwell", "tag": None}` | `?author=Orwell` |
| `{}` | (sorgu yok) |

## Kalıplar

```python
r = requests.get(BASE + "/books", params={"author": "Austen", "sort": "-year"})
print(r.url)                     # giden adresi denetle
books = r.json()["data"]
if not books:
    print("nothing found")       # 200 + boş liste
```

İsteğe bağlı parametreler:

```python
def search(**filters):
    return requests.get(BASE + "/books", params=filters).json()["data"]

search(author="Austen")
search(tag="scifi", sort="-year")
```

`**filters` fonksiyona verilen bütün adlı değerleri bir sözlükte topluyor;
o sözlük doğrudan `params` oluyor.

## Adres zaten sorgu içeriyorsa

```python
r = requests.get(BASE + "/books?sort=year", params={"tag": "scifi"})
print(r.url)   # .../books?sort=year&tag=scifi
```

requests yeni parametreleri `&` ile ekliyor; ikinci bir `?` yazmıyor. Yine de
tek bir yerde (yalnızca `params`) tutmak okumayı kolaylaştırır.

## Unutma

- Parametre adları ve anlamları API'den API'ye değişir: `per_page`, `limit`,
  `size`, `pageSize`... Belgeye bak.
- Bilinmeyen bir parametreyi API çoğu zaman sessizce yok sayar. Sonuç
  beklediğin gibi değilse önce `r.url`'deki adı belgeyle karşılaştır.
