# Sending Data: POST, PUT, PATCH, DELETE

So far you have only **read** (`GET`). Working with an API often means
writing too: adding a new record, correcting a field, deleting an outdated
record. In this section you really use the methods you met in Section 02.

On the practice server, adding, changing and deleting books needs a
**token** (Section 08). In the examples we define the header once:

```python
import requests

BASE = "http://api.odyssey.test"
AUTH = {"Authorization": "Bearer letmein"}
```

The server starts from scratch on every run; the books you add and delete are
back to how they were on the next run. Try things freely.

## POST: creating a new record

A new book is sent to the **list** of books (`/books`) with `POST`. The book's
details travel in the body, as JSON:

```python
new = {"title": "Kindred", "author_id": 6, "year": 1979, "price": 11.5}
r = requests.post(BASE + "/books", json=new, headers=AUTH)

print(r.status_code, r.headers["Location"])   # 201 /books/24
book = r.json()
print(book["id"], book["title"], book["author"]["name"])   # 24 Kindred Le Guin
```

Notice three things:

- **The `json=` parameter.** requests turns the dictionary into JSON text
  (`json.dumps`), puts it in the body and adds the
  `Content-Type: application/json` header itself.
- **`201 Created`.** It means "created"; not `200`.
- **The `Location` header and the response body.** You did not choose the
  book's number; the server did (`24`) and gave the new record's address in
  `Location`. The body carries the record's final state too, with the fields
  the server added (`author`).

<figure class="fig">
  <div class="flow">
    <span class="node">POST /books<br><small>body: the new book</small></span><span class="arrow">→</span>
    <span class="node acc">Server<br><small>validates, gives a number</small></span><span class="arrow">→</span>
    <span class="node">201 Created<br><small>Location: /books/24</small></span>
  </div>
  <figcaption>A new record goes to the list's address; the server gives it a number and states the new address in the <code>Location</code> header.</figcaption>
</figure>

## `json=` and `data=` are not the same

```python
r = requests.post(BASE + "/books", data={"title": "Kindred", "price": 11.5}, headers=AUTH)
print(r.request.headers["Content-Type"])   # application/x-www-form-urlencoded
print(r.request.body)                      # title=Kindred&price=11.5
print(r.status_code, r.json())
# 422 {'error': 'validation', 'detail': 'the body must be a JSON object'}
```

`data=` sends the dictionary as **form data**: the format of forms on web
pages (`name=value&...`), not JSON. An API that expects JSON cannot read it.
**If the API wants JSON, use `json=`.** The documentation says which it wants;
most of today's APIs want JSON.

## When the server refuses: 401 and 422

Send it without the token and the server does not know who you are:

```python
r = requests.post(BASE + "/books", json=new)
print(r.status_code, r.json())   # 401 {'error': 'missing or invalid token'}
```

If the body breaks the rules, `422`:

```python
r = requests.post(BASE + "/books", json={"title": "", "price": 5}, headers=AUTH)
print(r.status_code, r.json())
# 422 {'error': 'validation', 'detail': 'title must be a non-empty string'}
```

The server checking incoming data against its rules is called
**validation**: the title cannot be empty, the price must be positive. The
`detail` field says exactly what is wrong; it is the first place to read when
you get an error.

## PATCH: changing part of it

Let's change only Dune's price:

```python
r = requests.patch(BASE + "/books/2", json={"price": 8.99}, headers=AUTH)
book = r.json()
print(r.status_code, book["title"], book["price"], book["year"])   # 200 Dune 8.99 1965
```

We sent only the price; the title and year stayed as they were. This time the
address is the address of **a single record** (`/books/2`).

## PUT: replacing it completely

`PUT` **replaces** the record entirely with what you send:

```python
r = requests.put(BASE + "/books/4", json={"title": "Solaris", "price": 12.0}, headers=AUTH)
book = r.json()
print(r.status_code, book["title"], book["price"], book["year"], book["tags"])
# 200 Solaris 12.0 0 []
```

We sent only the title and price; the year became `0` and the tags empty. The
fields you did not send went back to their defaults. The warning from Section
02 came true: **`PATCH` for a partial change; `PUT` when you send the whole
record.**

## DELETE: deleting

```python
r = requests.delete(BASE + "/books/9", headers=AUTH)
print(r.status_code, repr(r.text))   # 204 ''
print(requests.get(BASE + "/books/9").status_code)   # 404
```

`204 No Content`: "deleted, nothing more to say". The body is empty;
`r.json()` would fail here. A `GET` afterwards returns `404`, confirming the
deletion.

Trying to delete the same book again:

```python
print(requests.delete(BASE + "/books/9", headers=AUTH).status_code)   # 404
```

The code is different (`404`) but **the result is the same**: the book is
gone. That is what `DELETE` being idempotent means; the second request does
not change the state.

## Write, then verify

Two good habits after a request that writes:

1. **Check the status code.** `201`, `200`, `204` are the codes you expect; if
   something else came, read the `detail` in the body.
2. **Verify the result from the response or with a new `GET`.** The server may
   have changed what you sent (a rounded price, an added field).

```python
r = requests.post(BASE + "/books", json=new, headers=AUTH)
if r.status_code == 201:
    location = r.headers["Location"]
    saved = requests.get(BASE + location).json()
    print("saved:", saved["title"], saved["price"])
else:
    print("failed:", r.status_code, r.json().get("detail"))
```

## Do not send a POST twice

The warning from Section 02 becomes concrete here: `POST` is not idempotent.
Run the code above twice and **two** Kindred records are created (24 and 25).
Code that automatically repeats a `POST` because the connection dropped
produces duplicate records. That is why we will keep `POST` separate when we
write retries in Section 11.

## Summary

- `POST /books` with `json=` creates a new record → `201`, a `Location`
  header and the record's final state in the body.
- `json=` sends a JSON body and `Content-Type: application/json`; `data=`
  sends form data. If the API wants JSON, use `json=`.
- `PATCH /books/2` changes only the fields you send; `PUT` replaces the whole
  record, and what you leave out may be lost.
- `DELETE` → `204`, empty body. A second delete may return `404`, but the
  result is the same.
- `401` the token is missing, `422` the body breaks the rules: read `detail`.
- After writing, check the code and verify the result; do not repeat a `POST`
  automatically.
