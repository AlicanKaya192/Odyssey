`contact_status(fields, now)` okunmuş alanları ve şimdiki zamanı (ISO,
`Z` ile) alıp sırayla şunu döndürsün: iletişim yoksa `"no contact"`,
`expires` yoksa `"no expiry"`, süre geçmişse ya da tam şimdi bitiyorsa
`"expired"`, yoksa `"ok"`. Başlangıç kodu süreyi hiç karşılaştırmıyor.

**Beklenen çıktı:**

```
ok
expired
no contact
```
