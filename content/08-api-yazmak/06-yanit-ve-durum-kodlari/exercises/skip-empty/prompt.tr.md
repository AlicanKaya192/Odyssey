`profiles` sözlüğü hazır; kayıtlarda `secret_note` adlı gizli bir alan da var.

**Yapman gereken:** `Profile` modeli (`name`; `bio` ve `website` isteğe
bağlı, varsayılan `None`) ve `GET /profiles/{profile_id}`. Cevapta:

- `secret_note` olmasın,
- değeri `None` olan alanlar hiç yazılmasın.

- `GET /profiles/1` → `{"name": "Ada", "bio": "Mathematician"}`
- `GET /profiles/2` → `{"name": "Alan", "website": "https://example.com"}`
