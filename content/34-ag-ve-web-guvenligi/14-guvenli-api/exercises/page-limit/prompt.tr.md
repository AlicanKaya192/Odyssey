`page_limit(value)` adresteki `limit` değerini (metin ya da `None`)
alsın. `None` ise ya da `re.fullmatch(r"[0-9]{1,6}", value)` tutmuyorsa
`20`; değilse sayıyı **1 ile 100 arasına** sıkıştırıp döndürsün.

**Beklenen çıktı:**

```
None 20
'50' 50
'0' 1
'500' 100
'ten' 20
'-5' 20
```
