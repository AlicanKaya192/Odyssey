`format_duration(seconds)` fonksiyonunu yaz: tam sayı saniyeyi
`"01:02:05"` biçiminde (saat:dakika:saniye, iki haneli) metne çevirsin.
`divmod` kullan: önce 3600'e, sonra 60'a böl. Saat 24'ü geçebilir
(`90061` → `"25:01:01"`).

**Beklenen çıktı:**

```
01:02:05
25:01:01
00:00:59
```
