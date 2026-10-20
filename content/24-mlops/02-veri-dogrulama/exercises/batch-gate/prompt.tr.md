`rules.py` dosyasında dersteki `SCHEMA` ve `check_row` hazır. `gate(rows, schema, max_bad_share)` fonksiyonunu yaz. Bu kez hata fırlatmak yerine bir **sözlük** döndür:

- Her satırı `check_row(row, schema)` ile denetle; sorunu olan satır karantinaya (`quarantined`), olmayan sağlam (`good`) sayılır.
- Bozuk satırların payı (`quarantined / len(rows)`) `max_bad_share`'den **büyükse** `"status"` değeri `"rejected"`, değilse `"accepted"`.
- Satır yoksa boş parti reddedilir: `{"status": "rejected", "good": 0, "quarantined": 0}`.
- Döndürülen sözlüğün anahtarları: `"status"`, `"good"`, `"quarantined"`.

**Beklenen çıktı:**

```
accepted 200 0
rejected 188 12
rejected 0 0
```
