Bu patikanın alıştırmaları ek paket kurmadan, Python'un kendi
kütüphanesiyle yazılmış küçük sunucular kullanıyor. Nasıl çalıştıklarını
bilmek konteynerde neyin dinlendiğini anlamayı kolaylaştırıyor.

## Dosya sunucusu

```text
python -m http.server 8000
```

Bulunduğu klasördeki dosyaları sunuyor. `index.html` varsa ana sayfa o.
Varsayılan olarak bütün adresleri (`0.0.0.0`) dinliyor; `--bind 127.0.0.1`
yalnızca içeriden ulaşılır yapıyor.

## JSON döndüren küçük bir API

```python
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = json.dumps({"status": "ok"}).encode()
            self.send_response(200)
        else:
            body = json.dumps({"error": "not found"}).encode()
            self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
```

- `("0.0.0.0", 8000)`: hangi adres ve port. Konteynerde hep `0.0.0.0`.
- `do_GET`: her GET isteğinde çalışan metot; `self.path` istenen yol.
- `send_response`, `send_header`, `end_headers`, `wfile.write`: durum kodu,
  başlıklar ve gövde (API patikasında gördüğün yanıtın parçaları).

## Gerçek projelerde

Bu küçük sunucular öğrenmek için yeterli ama gerçek uygulamalarda çatılar
kullanılıyor:

| Çatı | Çalıştırma | Konteynerde dikkat |
|---|---|---|
| FastAPI + uvicorn | `uvicorn main:app --host 0.0.0.0 --port 8000` | `--host 0.0.0.0` şart |
| Flask | `flask run --host 0.0.0.0` | Varsayılan 127.0.0.1 |
| Django | `python manage.py runserver 0.0.0.0:8000` | Varsayılan 127.0.0.1 |
| Streamlit | `streamlit run app.py --server.address 0.0.0.0` | |

API 2 patikasında FastAPI ile kendi API'ni yazıp bu patikanın
yöntemleriyle konteynere koyacaksın.
