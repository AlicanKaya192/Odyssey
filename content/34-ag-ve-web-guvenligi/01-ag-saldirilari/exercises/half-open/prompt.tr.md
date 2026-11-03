`events` her biri `[kind, src]` olan bir liste; `kind` `"SYN"` ya da
`"ACK"`. `half_open(events)` SYN gönderip ardından ACK göndermemiş
kaynakları döndürsün. Sıra adres sırası olsun:
`sorted(..., key=ipaddress.ip_address)` (metin sırası `.10`'u `.9`'dan
önce koyar).

**Beklenen çıktı:**

```
198.51.100.9
198.51.100.10
198.51.100.11
```
