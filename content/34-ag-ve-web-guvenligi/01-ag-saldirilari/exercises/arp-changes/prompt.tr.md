`replies` her biri `[ip, mac]` olan ARP cevaplarının listesi (geliş
sırasıyla). `arp_changes(replies)` bir tablo tutsun; bir adres için daha
önce **farklı** bir MAC görüldüyse `[ip, eski, yeni]` listesini sonuca
eklesin. Aynı MAC'in tekrar gelmesi değişiklik değildir.

**Beklenen çıktı:**

```
192.168.1.1
  old 02:00:00:00:00:fe
  new 02:00:00:00:00:66
```
