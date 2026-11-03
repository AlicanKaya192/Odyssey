`date_status(cert, today)` sertifikanın `today` günü geçerli olup
olmadığını söylesin: `today` `not_before`'dan önceyse `"not yet valid"`,
`not_after`'dan sonraysa `"expired"`, arasındaysa `"ok"`. Tarihler
`YYYY-MM-DD` metni. Başlangıç kodu yalnızca bitiş tarihine bakıyor.

**Beklenen çıktı:**

```
ok
not yet valid
expired
```
