The parts of a URL and the `urllib.parse` commands on one page.

## The parts

```text
https://api.example.com:8443/v1/books/42?author=Austen&sort=year#notes
└─┬─┘   └──────┬──────┘ └─┬┘└─────┬────┘└───────────┬──────────┘└──┬─┘
scheme       host       port    path          query string     fragment
```

| Part | Job | Note |
|---|---|---|
| Scheme | The rules of the talk | `https` for APIs |
| Host | Which computer | `localhost` = your own computer |
| Port | Which program | 443 (`https`) / 80 (`http`) when not written |
| Path | Which endpoint, which resource | `/v1/` version, `/42` identity |
| Query string | Extra details | `?` once, `name=value`, separated by `&` |
| Fragment | A place on the page | Never reaches the server |

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

## Base address + endpoint

```python
def endpoint_url(base, path):
    return base.rstrip("/") + "/" + path.lstrip("/")
```

## Remember

- `parse_qs` gives every value as a **list**: `params["city"][0]`.
- `parts.port` is `None` when it is not written.
- Do not glue the query string by hand; `urlencode` encodes spaces and `&`
  correctly.
