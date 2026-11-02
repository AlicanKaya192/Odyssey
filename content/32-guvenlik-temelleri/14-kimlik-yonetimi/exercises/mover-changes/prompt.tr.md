`roles` rol adından yetki listesine giden bir sözlük. Bir çalışanın
rolü `old_role`'dan `new_role`'a değişiyor.

`mover_changes(old_role, new_role, roles)` bir sözlük döndürsün:
`"add"` yeni rolde olup eskisinde olmayan yetkiler, `"remove"` eskisinde
olup yenisinde olmayanlar; ikisi de abece sırasında liste. İki rolde de
olan yetkiye dokunulmaz.

**Beklenen çıktı:**

```
add: ['approve-leave', 'read-reports']
remove: ['push-code', 'read-logs']
```
