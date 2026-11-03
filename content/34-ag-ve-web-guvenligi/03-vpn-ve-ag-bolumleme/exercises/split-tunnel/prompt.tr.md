Bölünmüş tünelde yalnızca belirli ağlara giden trafik VPN'den geçer.
`route(dst, tunnel_networks)` hedef adres listedeki ağlardan birindeyse
`"vpn"`, değilse `"direct"` döndürsün.

**Beklenen çıktı:**

```
10.20.0.15 vpn
172.20.1.1 vpn
203.0.113.7 direct
```
