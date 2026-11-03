Ağ Katmanları ve Güvenlik Duvarı bölümlerini birleştir. Her kuralda
`action`, `src` (CIDR) ve `port` (sayı ya da `"*"`) var.

`decide(rules, packet)` kuralları **yukarıdan aşağıya** denesin; paketin
kaynağı (`ipaddress`) kuralın ağındaysa ve port tutuyorsa **ilk** tutan
kuralın kararını döndürsün. Hiçbiri tutmazsa `"deny"`.

**Beklenen çıktı:**

```
10.0.5.7 22 deny
10.1.2.3 22 allow
192.168.1.5 443 allow
192.168.1.5 22 deny
```
