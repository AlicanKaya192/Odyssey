The headers you will see most often in requests, with typical values.

| Header | Example value | Meaning |
|---|---|---|
| `Host` | `api.example.com` | The host the request goes to |
| `Accept` | `application/json` | "I want the response as JSON" |
| `Content-Type` | `application/json` | "The body I am sending is JSON" |
| `Content-Length` | `37` | The body is 37 bytes |
| `Authorization` | `Bearer abc123` | An identity token (Section 08) |
| `User-Agent` | `python-requests/2.32` | The program that sent the request |
| `Accept-Language` | `tr-TR` | The preferred language of the response |

## Content types (Content-Type / Accept)

| Value | What |
|---|---|
| `application/json` | JSON data |
| `text/html` | A web page |
| `text/plain` | Plain text |
| `text/csv` | A CSV table |
| `application/x-www-form-urlencoded` | Form data (`name=value&...`) |
| `multipart/form-data` | File uploads |

## Two rules when reading

1. **Names are not case-sensitive.** In a program, store names lower-cased:
   `headers[name.lower()] = value`.
2. **Split only at the first colon.** In `Host: localhost:8000` the value is
   `localhost:8000`. `line.split(": ", 1)`.

## The byte count of the body

```python
body = '{"city": "Izmir"}'
print(len(body))                  # 17 letters
print(len(body.encode("utf-8")))  # 17 bytes

body = '{"city": "Kadıköy"}'
print(len(body))                  # 19 letters
print(len(body.encode("utf-8")))  # 21 bytes: ı and ö take two bytes each
```

`Content-Length` is always a number of **bytes**.
