`rules` her biri `{"action", "proto", "port"}` sözlüğü olan bir liste;
`proto` ya da `port` `"any"` olabilir. `decide(rules, packet)` kuralları
sırayla denesin ve ilk tutan kuralın `action` değerini döndürsün. Hiçbiri
tutmazsa `"deny"` döndürsün (varsayılan reddet).

**Beklenen çıktı:**

```
tcp 443 allow
tcp 22 deny
udp 53 allow
udp 123 deny
```
