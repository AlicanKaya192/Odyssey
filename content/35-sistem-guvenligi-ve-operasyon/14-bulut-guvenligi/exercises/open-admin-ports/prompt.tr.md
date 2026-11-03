Her ağ kuralı `port` ve `source` alanlı. `open_admin_ports(rules, admin_ports)`
kaynağı bütün internet olan (`"0.0.0.0/0"` ya da `"::/0"`) ve portu
`admin_ports` içinde olan kuralların portlarını **bir kez** ve küçükten
büyüğe döndürsün.

**Beklenen çıktı:**

```
[22, 3389]
```
