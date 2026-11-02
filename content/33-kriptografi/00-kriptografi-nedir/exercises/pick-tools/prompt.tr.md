`needs` bir sözlük; olmayan anahtar `False` sayılır.
`pick_tools(needs)` gereken araçların abece sıralı listesini döndürsün:

- `secret` → `"encryption"`
- `password` → `"password-hash"`
- `third_party` (üçüncü kişiye kanıt) → `"signature"`
- `tamper` ve `third_party` değilse → `"mac"`

**Beklenen çıktı:**

```
['encryption']
['mac']
['signature']
['encryption', 'password-hash']
[]
```
