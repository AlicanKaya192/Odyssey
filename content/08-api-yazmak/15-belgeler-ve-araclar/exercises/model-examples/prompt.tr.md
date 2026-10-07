**Yapman gerekenler:**

1. `Book` modeli: `title` (örnek `"Dune"`, açıklama `The book's title`),
   `year` (örnek `1965`, açıklama `Year of first publication`).
2. `POST /books` → `201`, kitabı döndür (`tags=["books"]`).
3. `GET /old-books` → `[]`; belgede **eskimiş** görünsün.

Denetim `/openapi.json`'da `Book` şemasına ve `/old-books`'un
`deprecated` alanına bakacak.
