The most used parts of a request and a response with requests.

## Sending a request

```python
import requests

r = requests.get(url)                    # get
r = requests.post(url, json=data)        # create (Section 09)
r = requests.put(url, json=data)         # replace completely
r = requests.patch(url, json=data)       # change part of it
r = requests.delete(url)                 # delete
```

All of them accept the same extras: `params=` (query, Section 07),
`headers=` (Section 08), `timeout=` (Section 11).

## The parts of the response

| Expression | Gives | Example |
|---|---|---|
| `r.status_code` | The status code (int) | `200` |
| `r.ok` | Is the code below 400 | `True` |
| `r.headers["Content-Type"]` | A header (name not case-sensitive) | `application/json; charset=utf-8` |
| `r.text` | The body as text | `'{"id": 1, ...}'` |
| `r.json()` | The body as a Python object | `{'id': 1, ...}` |
| `r.url` | The final address of the request | `http://api.odyssey.test/books/1` |
| `r.request.method` | The method that was sent | `GET` |
| `r.raise_for_status()` | Raises `HTTPError` on 4xx/5xx | |

## A safe reading pattern

```python
r = requests.get(url)
if r.status_code == 200:
    data = r.json()
else:
    print("error", r.status_code, r.text)
```

or:

```python
r = requests.get(url)
r.raise_for_status()      # stops here if something is wrong
data = r.json()
```

## Errors

| Error | When |
|---|---|
| `requests.exceptions.MissingSchema` | The address does not start with `http://` |
| `requests.JSONDecodeError` | `json()` was called on a body that is not JSON |
| `requests.HTTPError` | `raise_for_status()` saw a 4xx/5xx |
| `requests.ConnectionError` | The server could not be reached at all (Section 11) |
| `requests.Timeout` | The response did not arrive in time (Section 11) |
