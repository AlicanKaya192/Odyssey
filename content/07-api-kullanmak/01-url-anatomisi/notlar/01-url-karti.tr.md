URL'nin parçaları ve `urllib.parse` komutları tek sayfada.

## Parçalar

```text
https://api.example.com:8443/v1/books/42?author=Austen&sort=year#notes
└─┬─┘   └──────┬──────┘ └─┬┘└─────┬────┘└───────────┬──────────┘└──┬─┘
şema      ana makine    port     yol          sorgu dizesi       parça
```

| Parça | Görevi | Not |
|---|---|---|
| Şema | Konuşma kuralı | API'de `https` |
| Ana makine | Hangi bilgisayar | `localhost` = kendi bilgisayarın |
| Port | Hangi program | Yazılmazsa 443 (`https`) / 80 (`http`) |
| Yol | Hangi uç nokta, hangi kaynak | `/v1/` sürüm, `/42` kimlik |
| Sorgu dizesi | Ek bilgiler | `?` bir kez, `ad=değer`, `&` ile ayrılır |
| Parça | Sayfanın bir yeri | Sunucuya gitmez |

## `urllib.parse`

```python
from urllib.parse import urlparse, parse_qs, urlencode, quote, unquote

p = urlparse(url)
p.scheme, p.hostname, p.port, p.path, p.query, p.fragment

parse_qs("a=1&b=2&b=3")          # {'a': ['1'], 'b': ['2', '3']}
urlencode({"q": "New York"})     # q=New+York
urlencode({"t": ["x", "y"]}, doseq=True)   # t=x&t=y
quote("a b&c")                   # a%20b%26c
unquote("a%20b")                 # a b
```

## Taban adres + uç nokta

```python
def endpoint_url(base, path):
    return base.rstrip("/") + "/" + path.lstrip("/")
```

## Unutma

- `parse_qs` her değeri **liste** olarak verir: `params["city"][0]`.
- `parts.port` yazılmamışsa `None`.
- Sorgu dizesini elle yapıştırma; `urlencode` boşluğu ve `&` işaretini
  doğru kodlar.
