Bir ödeme sözlüğü: `amount`, `created_by`, `approvals` (onaylayanların
listesi). `approve(payment, approver)` bir onayı işleyip durumu döndürsün:

1. Onaylayan ödemeyi hazırlayan kişiyse → `"denied"`.
2. Onaylayan zaten listedeyse → `"duplicate"`.
3. Değilse onaylayanı `approvals` listesine **ekle**.
4. Gereken onay sayısı: tutar `10000` ya da üstüyse **2**, değilse **1**.
   Onay sayısı yetiyorsa → `"approved"`, yetmiyorsa → `"pending"`.

**Beklenen çıktı:**

```
ada denied
alan pending
alan duplicate
grace approved
small approved
```
