Her görev bir sözlük: `name`, `runs_as`, betiğin sahibi `owner` ve
izni `mode`. `risky_tasks(tasks)` `root` olarak çalışan ve betiği ya
`root`'a ait olmayan ya da grup veya diğerlerince yazılabilen
(`mode & 0o022`) görevlerin adlarını abece sırasıyla döndürsün.

**Beklenen çıktı:**

```
['audit', 'cleanup', 'report']
```
