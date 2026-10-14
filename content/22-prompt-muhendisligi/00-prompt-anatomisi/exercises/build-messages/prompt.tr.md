`build_messages(role, task, fmt, text)` iki mesajlık bir liste döndürsün:
önce `system` rolünde, içeriği `role`, `task` ve `fmt`'nin aralarında birer
boşlukla birleşimi olan mesaj; sonra `user` rolünde, içeriği `text` olan
mesaj. Her mesaj `{"role": ..., "content": ...}` biçiminde bir sözlük.

**Beklenen çıktı:**

```
2
Be a shop assistant. Classify. One word.
user Where is my parcel?
```
