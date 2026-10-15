`mask_log(lines, secrets)` fonksiyonunu yaz. Kayıt satırlarının listesini alsın; her satırda geçen her gizli değeri `***` ile değiştirip yeni bir liste döndürsün.

İki kural:

- Boş gizli değer (`""`) atlanır.
- **Uzun** gizli değerler önce değiştirilir. Yoksa `abc123XYZ` önce değişince `abc123XYZ-backup` satırında `***-backup` kalır ve değerin bir parçası sızar.

**Beklenen çıktı:**

```
Login as admin
Using token ***
Retry with ***
Done
```
