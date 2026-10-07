**Yapman gereken:** adresteki iki tam sayıyı toplayan uç nokta.

```text
GET /add/2/3     {"result": 5}
GET /add/-4/10   {"result": 6}
GET /add/x/3     422
```

Tip yazmazsan `"2" + "3"` = `"23"` olur; dene ve gör.
