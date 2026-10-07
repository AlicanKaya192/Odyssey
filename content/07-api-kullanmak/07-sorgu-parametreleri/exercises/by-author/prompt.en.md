Ask for Orwell's books; let the server do the filtering.

**What to do:**

1. Send a request to `/books` with `params={"author": "Orwell"}`.
2. Print the address that went out (`r.url`).
3. Collect the books' titles into a `titles` list and print each on its own
   line.

**Expected output:**

```
http://api.odyssey.test/books?author=Orwell
Nineteen Eighty-Four
Animal Farm
Homage to Catalonia
```
