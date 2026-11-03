`graph` paket → doğrudan bağımlılıklar listesi. `all_dependencies(graph,
root)` `root`'un doğrudan ve dolaylı bütün bağımlılıklarını **bir kez** ve
abece sırasıyla döndürsün; `root`'un kendisi listede olmasın. Grafikte
döngü olabilir: başlangıç kodunun özyinelemesi orada sonsuza gider.

**Beklenen çıktı:**

```
db, escape, http, pool, templates, web
http, pool
```
