`sources` kaynak adı → `[zaman_damgasi, metin]` listesi; damgalar saat
dilimli ISO metni. `build_timeline(sources)` bütün olayları UTC'ye
çevirip zaman sırasıyla `"<SS:DD:ss> <kaynak> <metin>"` satırları olarak
döndürsün (saat biçimi `strftime("%H:%M:%S")`, UTC'de). Aynı anda olan
olaylar kaynak adına göre sıralansın.

**Beklenen çıktı:**

```
02:14:00 vpn login bob
02:15:10 db new db user
02:16:30 web admin page
02:20:05 db table exported
```
