Different APIs put records in different envelopes. The most common forms and
how to reach the list of records.

## 1. `data` + `meta`

```json
{"data": [{"id": 1}, {"id": 2}], "meta": {"page": 1, "total": 42}}
```

```python
items = response["data"]
```

## 2. `results` + page links

```json
{"count": 42, "next": "https://api.example.com/books?page=2",
 "previous": null, "results": [{"id": 1}, {"id": 2}]}
```

```python
items = response["results"]
```

`next` is the address of the next page; if it is `null` you are on the last
page (Section 10).

## 3. A bare list

```json
[{"id": 1}, {"id": 2}]
```

```python
items = response
```

The response itself is the list. If there is total or page information, it
comes in the headers.

## 4. A key named after the records

```json
{"books": [{"id": 1}], "total": 1}
```

```python
items = response["books"]
```

## 5. A single record

When you ask for a single resource such as `/books/42`, the response is often
not a list but the record itself:

```json
{"id": 42, "title": "Emma"}
```

To turn it into a table you can make a one-item list: `items = [response]`.

## How do you know?

- Look at the sample response in the documentation.
- If there is none, print the first response with
  `json.dumps(response, indent=2)` and read it with your own eyes.
- To be sure inside a program, check its type:
  `isinstance(response, list)`.
