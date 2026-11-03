Politika `effect` (`"allow"` / `"deny"`) ve `action` (joker `*`
olabilir) alanlı ifadelerden oluşur. `is_allowed(policy, action)` uyan
ifadelerden biri `deny` ise `False`, en az biri `allow` ise `True`, hiçbiri
uymuyorsa `False` döndürsün. Eşleşme: `fnmatch.fnmatchcase(action, kalip)`.
Başlangıç kodu ilk uyan ifadeye göre karar veriyor.

**Beklenen çıktı:**

```
True
False
False
```
