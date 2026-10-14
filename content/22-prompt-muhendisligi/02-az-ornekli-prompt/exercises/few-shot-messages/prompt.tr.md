`build_messages(system, examples, text)` şu listeyi döndürsün: önce
`system` mesajı; sonra `examples` içindeki her `[metin, etiket]` çifti için
bir `user` mesajı (metin) ve bir `assistant` mesajı (etiket); en sonda
`text` içerikli `user` mesajı.

**Beklenen çıktı:**

```
6
['user', 'assistant', 'user']
warranty
```
