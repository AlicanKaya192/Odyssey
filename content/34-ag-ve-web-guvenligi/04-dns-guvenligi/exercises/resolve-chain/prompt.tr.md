`records` her adı `[kind, value]` listesine eşleyen bir sözlük; `kind`
`"A"` ya da `"CNAME"`. `resolve(records, name)` CNAME'leri izleyip A
kaydının adresini döndürsün. Ad yoksa `"NXDOMAIN"`. CNAME'ler birbirini
gösterip döngü kurabilir: **8** CNAME izlendiği hâlde A'ya varılmadıysa
`"LOOP"` döndürsün. Başlangıç kodu yalnızca bir adım bakıyor.

**Beklenen çıktı:**

```
www.example.com 203.0.113.10
mail.example.com NXDOMAIN
a.example LOOP
```
