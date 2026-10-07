**Yapman gerekenler:**

1. `Note` modeli: `text` (zorunlu metin), `pinned` (`bool`, varsayılan
   `False`).
2. `POST /notes`: notu listeye ekle, `201` ile `{"id": sıra, "text": ...,
   "pinned": ...}` döndür. `id` listedeki sırası (1'den başlar).
3. `GET /notes`: eklenen notları döndür.

- `POST /notes`, gövde `{"text": "buy milk"}` → `201`, `{"id": 1, "text": "buy milk", "pinned": false}`
- `POST /notes`, gövde `{"text": "call mom", "pinned": true}` → `201`, `{"id": 2, ...}`
- `POST /notes`, gövde `{"pinned": true}` → `422`
- `GET /notes` → iki not
