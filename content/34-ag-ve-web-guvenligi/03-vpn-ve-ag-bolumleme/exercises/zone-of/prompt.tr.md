`zones` her biri `[name, cidr]` olan bir liste ve ağlar iç içe
olabilir. `zone_of(ip_text, zones)` adresi içeren ağlardan **önek uzunluğu
en büyük** olanın (en özel) adını döndürsün; hiçbiri içermiyorsa
`"unknown"`. Ağın önek uzunluğu `net.prefixlen`. Başlangıç kodu ilk
tutanı döndürüyor.

**Beklenen çıktı:**

```
10.20.5.9 db
10.20.9.9 servers
10.1.1.1 corp
192.168.1.1 unknown
```
