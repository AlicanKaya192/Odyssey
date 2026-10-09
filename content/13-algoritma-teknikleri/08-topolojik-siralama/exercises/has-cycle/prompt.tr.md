`has_cycle(deps)` fonksiyonunu yaz: bağımlılıklarda **yönlü döngü** varsa
`True` döndürsün.

Kahn'ın sayaç yöntemi kolay bir yol: sırayla alınabilen iş sayısı bütün iş
sayısından azsa döngü var. Son satırdaki 50 000 işlik zincirde özyineli DFS
derinlik sınırına takılır.

**Beklenen çıktı:**

```
False
True
False True
```
