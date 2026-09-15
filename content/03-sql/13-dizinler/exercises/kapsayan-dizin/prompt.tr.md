Bu sorgu `created_at` ile süzüyor ve `amount`'u da istiyor:

```sql
SELECT created_at, amount FROM events
WHERE created_at >= '2025-06-01' AND created_at < '2025-06-02';
```

Yalnızca `created_at` üzerinde bir dizin varken sunucu o dizini **hiç
kullanmadı** ve tabloyu baştan sona okudu (150 okuma): dizinde `amount`
yok, her satır için tabloya dönmek taramadan pahalı sayıldı.

`created_at` üzerine, `amount`'u da **yanında taşıyan** tek bir dizin kur.
`amount` anahtarın parçası olmasın — sıralamaya girmesin, yalnızca dizinde
dursun. Ölçüldü: böyle bir dizinle aynı sorgu **3 okuma**.

Denetim anahtar sütununa ve eklenen sütuna ayrı ayrı bakıyor.
