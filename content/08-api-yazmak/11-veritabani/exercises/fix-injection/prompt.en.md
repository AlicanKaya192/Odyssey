Two search endpoints work, but both build the query with an f-string: open
to SQL injection.

**What to do:** turn both into parameterised queries (`?`). Normal searches
must give the same results, while the attack text must find nothing.

- `GET /search?text=call mom` → `[{"id": 2, "text": "call mom"}]`
- `GET /search?text=x' OR '1'='1` → `[]`
- `GET /find?word=ea` → `read Dune`
- `GET /find?word=x' OR 1=1 --` → `[]`
