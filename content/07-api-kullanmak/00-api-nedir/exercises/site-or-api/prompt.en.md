Every response says what kind of data it carries with a label: the
**content type**. `text/html` is a web page, that is for people;
`application/json` is orderly data, that is for programs.

**What to do:**

1. From the responses in `responses`, collect the addresses whose content
   type is `application/json` into a list called `api_urls` (keep the order).
2. Print `For programs:`, then each of those addresses on its own line.
3. On the last line, print the number of `text/html` responses as
   `For people: N`.

**Expected output:**

```
For programs:
/api/weather
/api/cities
/api/forecast
For people: 2
```

You will meet the content type again inside the headers in Sections 02 and
03; the client looks at it to decide how to read the response.
