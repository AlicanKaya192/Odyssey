`check_values(template, values)` şablondaki `{{ad}}` yer tutucularının
adlarını hazır `SLOT` ile bulsun ve `[eksik adlar, kullanılmayan adlar]`
döndürsün: eksik, şablonda olup `values`'ta olmayanlar; kullanılmayan,
`values`'ta olup şablonda olmayanlar. İki liste de abece sırasıyla.

**Beklenen çıktı:**

```
[['message', 'order_id'], ['order']]
[[], []]
```
