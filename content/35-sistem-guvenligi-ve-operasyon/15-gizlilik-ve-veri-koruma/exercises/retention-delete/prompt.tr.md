Her kayıt `[kimlik, amac, olusturma]` (tarih ISO metni); `retention` amaç →
gün. `to_delete(records, retention, today)` silinecek kayıtların
kimliklerini abece sırasıyla döndürsün: yaşı amacın süresini **aşan** ve
amacı `retention`'da **olmayan** kayıtlar (saklamak için bir dayanak yok).

**Beklenen çıktı:**

```
['r1', 'r5']
```
