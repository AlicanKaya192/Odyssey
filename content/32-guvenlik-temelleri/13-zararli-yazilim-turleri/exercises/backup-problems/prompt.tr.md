`copies` verinin bütün kopyaları (asıl veri dahil): her biri `media`,
`offsite`, `offline` alanlı sözlük.

`backup_problems(copies)` eksikleri bu sırayla bir liste olarak
döndürsün; eksik yoksa boş liste:

1. `"need-3-copies"`: 3'ten az kopya,
2. `"need-2-media"`: 2'den az **farklı** ortam (`media`),
3. `"need-offsite"`: başka yerde (`offsite`) kopya yok,
4. `"need-offline"`: bağlantısız (`offline`) kopya yok.

**Beklenen çıktı:**

```
need-3-copies
need-2-media
need-offsite
need-offline
good: 0 problems
```
