Bir API alan adlarını `camelCase` istiyor, ama Rust'ta `snake_case` yazıyoruz. `rename_all` kullan. `nick_name` `None` ise JSON'a hiç yazılmasın.

**Beklenen çıktı:**

```text
{"userId":1}
{"userId":2,"nickName":"gh"}
```
