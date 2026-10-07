# Query Parameters and Filtering

Asking an API for "all the books" is rarely useful. What you want is usually
narrower: books by **Austen**, the ones tagged **science fiction**, sorted
**newest first**, the **first 3**. You tell the server these details with
query parameters.

In Section 01 you met the query string (`?author=Austen&sort=year`) and built
it by hand with `urlencode`. requests does this for you; you just give it a
dictionary.

## `params=`: from a dictionary to a query string

```python
import requests

BASE = "http://api.odyssey.test"
r = requests.get(BASE + "/books", params={"author": "Austen"})
print(r.url)
# http://api.odyssey.test/books?author=Austen
print([b["title"] for b in r.json()["data"]])
# ['Emma', 'Persuasion', 'Pride and Prejudice', 'Sense and Sensibility']
```

requests turns the `params` dictionary into a query string and adds it to the
end of the address. `r.url` shows the address the request **really went to**;
it is the easiest way to check that the parameters went out right.

<figure class="fig">
  <div class="flow">
    <span class="node">params={"author": "Austen"}</span><span class="arrow">→ requests →</span>
    <span class="node acc">/books?author=Austen</span><span class="arrow">→</span>
    <span class="node">The server filters</span>
  </div>
  <figcaption>You give the dictionary; requests builds the address and encodes the values. <code>r.url</code> shows the result.</figcaption>
</figure>

Why not write the address by hand? Writing `BASE + "/books?q=" + text` breaks
the address when the text has a space or `&` (Section 01). `params=` encodes
every value itself:

```python
r = requests.get(BASE + "/books", params={"q": "the lighthouse"})
print(r.url)   # http://api.odyssey.test/books?q=the+lighthouse
```

## Several parameters

You can put as many keys as you like in the dictionary. They are all joined
with `&`:

```python
r = requests.get(BASE + "/books", params={"tag": "scifi", "sort": "-year", "per_page": 3})
print(r.url)
# http://api.odyssey.test/books?tag=scifi&sort=-year&per_page=3
print([(b["title"], b["year"]) for b in r.json()["data"]])
# [('Fiasco', 1986), ('The Dispossessed', 1974), ('The Lathe of Heaven', 1971)]
```

Numbers (`3`) are turned into text on their own. **The API's documentation**
says which parameters exist and what they mean; the practice server's
documentation is in the previous section's notes.

## The three jobs of parameters

Query parameters usually do one of three jobs:

**Filtering:** narrows the list.

```text
?author=Austen            by author
?tag=scifi                by tag
?year_min=1900&year_max=1930   by range
?q=dune                   by a word in the title
```

**Sorting:** sets the order. In this API `sort=year` is smallest first,
`sort=-year` largest first. Other APIs may use a separate parameter such as
`order=desc`; you check the documentation.

**Limiting and paging:** says how many records come back: `per_page=3`,
`page=2`. We will look at paging in detail in Section 10.

## The same name more than once: a list

To ask for two tags together, give a **list** as the value:

```python
r = requests.get(BASE + "/books", params={"tag": ["scifi", "humor"]})
print(r.url)
# http://api.odyssey.test/books?tag=scifi&tag=humor
print([b["title"] for b in r.json()["data"]])
# ['The Cyberiad']
```

requests writes the list as `tag=scifi&tag=humor`. This API reads the two
tags as "**both** of them". Another API might read them as "**either** of
them", or use a comma form such as `tags=scifi,humor`. Once again: the
documentation says.

## A parameter set to `None` is not sent

```python
r = requests.get(BASE + "/books", params={"author": "Orwell", "tag": None})
print(r.url)   # http://api.odyssey.test/books?author=Orwell
```

requests does not write a key whose value is `None` at all. That makes it easy
to gather optional parameters in one function:

```python
def search(author=None, tag=None, sort=None):
    params = {"author": author, "tag": tag, "sort": sort}
    return requests.get(BASE + "/books", params=params).json()["data"]
```

Only the values you give go into the address; the rest drop out quietly.

## No results: an empty list, not an error

When filtering finds nothing, most APIs **do not return an error**; they
return an empty list:

```python
r = requests.get(BASE + "/books", params={"author": "nobody"})
print(r.status_code, r.json()["data"])   # 200 []
```

`200` with an empty `data` means "the request is fine, no record matches".
`404` means "no such address or record". Do not mix them up: for an empty list
your code must not crash; it should say "nothing found".

## Filter on the server or in Python?

You could also fetch every book and filter in Python:

```python
books = requests.get(BASE + "/books", params={"per_page": 20}).json()["data"]
austen = [b for b in books if b["author"]["name"] == "Austen"]
```

But real APIs can hold thousands or millions of records. Downloading them all
is slow and puts load on the server. **If the API supports filtering, leave
the filtering to the server**; let only the records you need come back. Keep
filtering in Python for conditions the API does not support.

## Path or query? (a reminder)

The distinction from Section 01 applies here too:

- `/books/42` → **a single book** (a path parameter).
- `/books?author=Austen` → **filter the list** (a query parameter).

You may also see a form such as `/books?id=42`, but in REST style the address
of a single resource is a path. We will come back to this in Section 13.

## Summary

- `requests.get(url, params={...})` turns the dictionary into an encoded
  query string and adds it to the address. Do not glue the address by hand.
- `r.url` shows the address the request really went to; look at it to check
  the parameters.
- Parameters filter (`author`, `tag`, `q`), sort (`sort`) and limit
  (`per_page`, `page`). The documentation says which exist.
- A list value repeats the name (`tag=a&tag=b`); a `None` value is not sent.
- When nothing matches, most APIs return `200` and an empty list; that is not
  an error.
- If the API can filter, leave the filtering to the server.
