`fixed_share(system, inputs)` her girdi için `[system, user]` mesaj
listesinin token sayısını `count_message_tokens` ile bulsun. Döndür:
`[bütün çağrıların toplam token'ı, sistem mesajı içeriğinin bütün
çağrılardaki toplam token'ı, ikincinin birinciye oranı]`; oran 2 basamağa
yuvarlanmış (`inputs` boşsa oran `0.0`).

**Beklenen çıktı:**

```
[40, 12, 0.3]
[62, 34, 0.55]
```
