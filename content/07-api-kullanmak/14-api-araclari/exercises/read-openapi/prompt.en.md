The practice server describes itself with `GET /openapi.json`. Do Swagger UI's
first job yourself: read the document and list the endpoints.

**What to do:**

1. Ask for the document; print the API's title and version (`info`).
2. For each path and each method in `paths`, build the line
   `METHOD path - summary`; add ` (auth)` at the end of those that need
   authentication (those with a `security` field). Collect the lines in an
   `endpoints` list and print them.
3. Print how many operations need authentication.

**Expected output:**

```
Odyssey Library API 1.0
GET /books - List books
POST /books - Add a book (auth)
GET /books/{id} - Get one book
PUT /books/{id} - Replace a book (auth)
PATCH /books/{id} - Change a book (auth)
DELETE /books/{id} - Delete a book (auth)
GET /authors - List authors
GET /authors/{id}/books - Books of one author
GET /stats - Library statistics (auth)
need auth: 5
```
