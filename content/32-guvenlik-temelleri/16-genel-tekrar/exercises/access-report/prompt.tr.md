En Az Yetki bölümünü toparla. `grants` kullanıcı → verilen yetkiler,
`used` kullanıcı → son 90 günde kullanılanlar (kullanıcı yoksa hiçbiri),
`conflicts` birlikte bulunmaması gereken `[a, b]` çiftleri.

`access_report(grants, used, conflicts)` satırları bir liste olarak
döndürsün. Kullanıcılar abece sırasında; her kullanıcıda önce kullanılmayan
her yetki (abece sırasında) `"<kullanici>: unused <yetki>"`, sonra iki
yetkisini de taşıdığı her çatışma (verildiği sırada)
`"<kullanici>: conflict <a>+<b>"`.

**Beklenen çıktı:**

```
ada: unused read-reports
ada: conflict pay-create+pay-approve
bora: unused read-reports
ceren: unused read-logs
```
