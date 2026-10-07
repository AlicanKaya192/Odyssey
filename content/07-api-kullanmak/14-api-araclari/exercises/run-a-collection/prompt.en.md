You have a small collection the team exported from Postman (simplified) and
an environment. The requests contain placeholders such as `{{base_url}}` and
`{{token}}`.

**What to do:**

1. Write the function `fill(text, variables)`: it replaces every `{{name}}`
   placeholder in the text with the value from the `variables` dictionary.
2. Run each request of the collection in order: fill the address and the
   header values with `fill`, send it with `requests.request` (with `json=`
   if there is a `body`).
3. Print each request's name and status code.

**Expected output:**

```
List books: 200
Who am I: 200
Add a book: 201
Missing book: 404
```
