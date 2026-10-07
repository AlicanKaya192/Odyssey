In this API the endpoint that logs out is written with `GET`. While a
browser preloads a page (some browsers open links in advance), the person
could be logged out by themselves.

**What to do:** logging out changes state; move the endpoint to the right
method.

```text
GET  /logout   405
POST /logout   {"logged_in": false}
```
