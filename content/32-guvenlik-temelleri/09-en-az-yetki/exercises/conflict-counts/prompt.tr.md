`conflicts` çakışan görev çiftlerinin listesi (her çift iki elemanlı bir
liste). `user_perms` kullanıcıdan yetki listesine bir sözlük.

`conflict_counts(user_perms, conflicts)` her kullanıcının kaç çiftin
**iki yarısına birden** sahip olduğunu saysın ve yalnızca en az bir
çakışması olan kullanıcıları içeren bir sözlük döndürsün.

**Beklenen çıktı:**

```
{'ada': 2, 'grace': 1}
```
