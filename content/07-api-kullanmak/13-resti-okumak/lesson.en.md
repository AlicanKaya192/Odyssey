# Reading REST

Since the start of the path you have been using an API designed according to
REST's rules, and learnt most of them without noticing. In this section we
put the pieces together and read REST by name. The aim is two-way:

- When you open a new API's documentation, being able to **predict**:
  "deleting books is most likely `DELETE /books/<id>`".
- Being able to **tell good design from bad**: making the right decisions
  when you write your own API in API 2.

## What is REST?

REST (Representational State Transfer) is a **design style** described in a
doctoral thesis in 2000. It is not a library or a protocol; it is a set of
principles about how to use HTTP. An API that follows these principles is
called a "REST API" or "RESTful".

In everyday practice the principles come down to five ideas.

## 1. Everything is a resource, and every resource has an address

A **resource** is what the API talks about: a book, an author, an order.
Resources come in two forms:

<figure class="fig">
  <div class="flow">
    <span class="node">/books<br><small>collection</small></span><span class="arrow">→</span>
    <span class="node acc">/books/42<br><small>item</small></span>
    <span class="arrow">·</span>
    <span class="node">/authors/6<br><small>item</small></span><span class="arrow">→</span>
    <span class="node">/authors/6/books<br><small>related collection</small></span>
  </div>
  <figcaption>A collection's name is plural; an item is the collection's address plus an identifier; relationships are nested.</figcaption>
</figure>

- **Collection:** a list of resources of the same kind. Its name is plural:
  `/books`, `/authors`.
- **Item:** a single resource. The collection's address + an identifier:
  `/books/42`.

Related resources can be written **nested**: `/authors/6/books` means "the
books of author 6".

```python
r = requests.get(BASE + "/authors/6/books")
print([b["title"] for b in r.json()["data"]])
# ['The Dispossessed', 'The Left Hand of Darkness',
#  'A Wizard of Earthsea', 'The Lathe of Heaven']
```

## 2. The address is a noun; the action is in the method

REST's most recognisable rule: **no verbs in the address.** The HTTP method
says what to do.

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>Action in the address</h4><pre><code class="language-text">GET  /getBooks
POST /createBook
POST /books/42/delete
POST /updateBookPrice</code></pre></div>
    <div class="ok"><h4>Action in the method</h4><pre><code class="language-text">GET    /books
POST   /books
DELETE /books/42
PATCH  /books/42</code></pre></div>
  </div>
  <figcaption>The four requests on the right use two addresses; the method decides the job.</figcaption>
</figure>

Addresses such as `/getBooks`, `/createBook` and `/books/42/delete` do not
follow REST: the action has leaked into the address. In REST the same address
(`/books/42`) does different jobs depending on the method.

## 3. Methods and codes are a contract

In a REST API each method has a set meaning and success code; the table you
have seen along the path is really REST's contract:

| Request | Meaning | Success |
|---|---|---|
| `GET /books` | List | `200` + the list |
| `GET /books/42` | Fetch | `200` + the record; `404` if missing |
| `POST /books` | Create | `201` + `Location` |
| `PUT /books/42` | Replace | `200` (or `204`) |
| `PATCH /books/42` | Change part | `200` |
| `DELETE /books/42` | Delete | `204` |

A method that is not supported gets `405`, and the `Allow` header lists the
valid ones:

```python
r = requests.put(BASE + "/books")
print(r.status_code, r.headers["Allow"])   # 405 GET, POST
```

The collection accepts `GET` and `POST`; `PUT` is for items.

## 4. Every request stands on its own (stateless)

In REST the server **does not remember you** between requests. Every request
carries everything needed to understand it: identity (the token), parameters,
the body. That is why you send the token on **every** request; there is no
"I logged in once, now it knows me". This is called **statelessness**.

The benefit: any request can go to any copy of the server. As the API grows,
adding more servers becomes easy.

## 5. Responses can show the way (links)

A good REST API gives **links** in its responses: the next page, a related
resource, what can be done next. The practice server's root address:

```python
print(requests.get(BASE + "/").json())
# {'links': {'books': '/books', 'authors': '/authors', 'stats': '/stats'}}
```

Instead of memorising addresses, a client can follow links. The `links.next`
of pagination (Section 10) is the most common example. The idea has a long
name: HATEOAS ("hypermedia as the engine of application state"). Knowing the
name is enough; in practice it means "follow the links".

## Query parameters and versions

The two remaining habits are familiar from earlier sections:

- **Filtering, sorting and paging go in the query string:**
  `/books?author=Austen&sort=-year&page=2` (Sections 07, 10). You do not open
  a new address (not `/books/by-author/Austen`).
- **The version goes in the address or a header:** `/v1/books`, `/v2/books`.
  Changes are made in a new version so old clients do not break (Section 01).

## Good design, bad design

| Bad | Why | The REST way |
|---|---|---|
| `GET /getAllBooks` | A verb in the address | `GET /books` |
| `POST /books/42/delete` | The action in the address, the wrong method | `DELETE /books/42` |
| `GET /book?id=42` | Singular name, identifier in the query | `GET /books/42` |
| `POST /updatePrice` | A verb, and the resource is unclear | `PATCH /books/42` |
| `GET /books/delete/42` | A `GET` that deletes something! | `DELETE /books/42` |
| `200` + `{"error": ...}` for an error | The code gives false information | `404`, `422`... |

The last one is the sneakiest: an API that returns `200` on an error misleads
every client that checks the status code. Deleting with `GET` is even more
dangerous: browsers and tools treat `GET` as safe and may repeat it on their
own.

## REST is not everything

REST is the most common style but not the only one. A few you will hear of:

- **GraphQL:** a single address; the client writes which fields it wants in a
  query language.
- **gRPC:** for fast communication between programs; a binary format instead
  of JSON.
- **Webhook:** works the other way round: when something happens, the server
  sends a request to **your** address.

On this path and in API 2 we work with REST; knowing the others exist is
enough.

## Summary

- REST is a design style for using HTTP. Five ideas: **resources and their
  addresses**, **nouns in the address / actions in the method**, **the
  method and code contract**, **statelessness**, **links**.
- A collection is plural (`/books`), an item is collection + identifier
  (`/books/42`), a relationship is nested (`/authors/6/books`).
- No verbs in addresses; the same address does different jobs by method. An
  unsupported method gets `405` + `Allow`.
- Every request stands on its own: the token goes with every request.
- Filtering and paging go in the query; the version in the address.
- Returning `200` for an error and changing things with `GET` are REST's most
  dangerous violations.
