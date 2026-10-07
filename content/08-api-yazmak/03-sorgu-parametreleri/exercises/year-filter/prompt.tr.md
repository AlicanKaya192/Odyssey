`books` listesi hazır.

**Yapman gereken:** `GET /books` isteğe bağlı bir `year_from` süzgeci alsın:

- Verilirse yılı `year_from` ve sonrası olan kitaplar.
- Verilmezse altı kitabın hepsi.

- `GET /books?year_from=1950` → Dune, Kindred, Beloved
- `GET /books` → altı kitap
