Hafta 4'te geçen her şey tek sayfada.

## İçe aktarmak

| Yazım | Kullanım |
|---|---|
| `import random` | `random.choice(...)` |
| `from random import choice` | `choice(...)` |
| `from random import choice, randint` | ikisi birden |
| `from sayings import goodbye` | kendi `sayings.py` dosyandan |

## random ve statistics

| Fonksiyon | Ne yapar |
|---|---|
| `random.choice(["a", "b"])` | listeden rastgele bir öğe |
| `random.randint(1, 10)` | 1–10 arası tam sayı, **iki uç dahil** |
| `random.shuffle(cards)` | listeyi yerinde karıştırır, `None` döndürür |
| `statistics.mean([100, 90])` | ortalama: `95` |
| `statistics.median([1, 3, 2])` | ortanca: `2` |
| `statistics.mode([1, 1, 2])` | en sık değer: `1` |

## Komut satırı

`python name.py David Malan` için:

| Yazım | Değer |
|---|---|
| `sys.argv` | `['name.py', 'David', 'Malan']` |
| `sys.argv[0]` | `'name.py'` (programın adı) |
| `sys.argv[1]` | `'David'` (ilk argüman, **metin**) |
| `sys.argv[1:]` | `['David', 'Malan']` |
| `len(sys.argv)` | `3` |
| `sys.exit("mesaj")` | mesajı yazar, programı bitirir |

## Dilim

| Yazım (`s = [1, 2, 3, 4]`) | Sonuç |
|---|---|
| `s[1:]` | `[2, 3, 4]` |
| `s[:2]` | `[1, 2]` |
| `s[1:3]` | `[2, 3]` (başlangıç dahil, bitiş hariç) |
| `s[-2:]` | `[3, 4]` (sondan iki) |
| `"hello"[1:3]` | `"el"` (dizelerde de çalışır) |

## Paketler ve API

| Yazım | Ne yapar |
|---|---|
| `pip install cowsay` | paketi PyPI'dan kurar (terminalde) |
| `requests.get(url)` | adrese istek atar |
| `response.json()` | JSON cevabını sözlüğe/listeye çevirir |
| `json.dumps(data, indent=2)` | veriyi okunur JSON metnine çevirir |
| `except requests.RequestException:` | bağlantı hatalarını yakalar |
