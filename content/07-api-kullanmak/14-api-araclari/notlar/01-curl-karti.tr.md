curl'ün en çok kullanılan seçenekleri ve requests karşılıkları.

## Seçenekler

| curl | Ne yapar | requests |
|---|---|---|
| `curl URL` | GET isteği | `requests.get(URL)` |
| `-X POST` | Yöntemi seçer | `requests.post(...)` |
| `-H "Ad: değer"` | Başlık ekler | `headers={"Ad": "değer"}` |
| `-d 'metin'` | Gövde gönderir (yöntemi POST yapar) | `data=` / `json=` |
| `--json '{...}'` | JSON gövde + başlıklar (yeni curl) | `json={...}` |
| `-u ad:sifre` | Basic kimlik | `auth=("ad", "sifre")` |
| `-i` | Yanıt başlıklarını da gösterir | `r.headers` |
| `-s` | Sessiz (ilerleme göstermez) | |
| `-o dosya` | Yanıtı dosyaya yazar | `open(...).write(r.content)` |
| `-G --data-urlencode "q=a b"` | Sorgu parametresi kodlar | `params={"q": "a b"}` |
| `--max-time 5` | Zaman aşımı | `timeout=5` |

## Örnekler

```text
curl -i https://api.example.com/books?author=Austen
curl -H "X-API-Key: abc" https://api.example.com/stats
curl -X PATCH --json @price.json -H "Authorization: Bearer abc" \
  https://api.example.com/books/2
curl -X DELETE https://api.example.com/books/7 -H "Authorization: Bearer abc"
```

## Windows'ta dikkat

- PowerShell'de `curl` başka bir komuta yönlenebilir: `curl.exe` yaz.
- Komut satırında JSON içindeki çift tırnaklar ters bölüyle kaçırılır:
  `-d "{\"a\": 1}"`. Uzun gövdeler için dosyadan göndermek kolaydır:
  `-d @body.json`.
