`validate(data)` hata kodlarının listesini döndürsün (sıra önemli):

- `data` sözlük değilse yalnızca `["object"]`.
- Eksik her alan için, `category`, `urgent`, `order_id` sırasıyla
  `"missing:<alan>"`.
- `category` varsa ve `LABELS`'ta değilse `"category"`.
- `urgent` varsa ve `bool` değilse `"urgent"`.
- `order_id` `None` değilse ve `ORD-` + beş rakama tam uymuyorsa
  `"order_id"`.

**Beklenen çıktı:**

```
[]
['missing:order_id', 'category', 'urgent']
['object']
```
