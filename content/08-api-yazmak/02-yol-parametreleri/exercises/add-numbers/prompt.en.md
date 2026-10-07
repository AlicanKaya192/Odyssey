**What to do:** an endpoint that adds the two integers in the address.

```text
GET /add/2/3     {"result": 5}
GET /add/-4/10   {"result": 6}
GET /add/x/3     422
```

Without types, `"2" + "3"` = `"23"`; try it and see.
