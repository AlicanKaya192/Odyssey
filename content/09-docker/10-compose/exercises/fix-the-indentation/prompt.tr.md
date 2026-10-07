Bu compose.yaml okunamıyor: `docker compose up` şunu diyor:

```text
did not find expected key
```

**Yapman gereken:** girintisi kayık satırı bul ve düzelt. `web`'in bütün
ayarları (`build`, `ports`, `environment`) aynı sütunda başlamalı.
