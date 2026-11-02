`zones` parça adından bölgeye bir sözlük, `flows` `[kaynak, hedef]`
listeleri.

`boundary_crossings(flows, zones)` güven sınırını geçen akışları
`"kaynak->hedef"` metinleri olarak, listedeki sırayla döndürsün. Bir ucun
bölgesi **bilinmiyorsa** (sözlükte yoksa) o akış da sınırı geçiyor sayılsın:
bölgesini bilmediğin bir şeye güvenme.

**Beklenen çıktı:**

```
student->web
web->db
db->backup
```
