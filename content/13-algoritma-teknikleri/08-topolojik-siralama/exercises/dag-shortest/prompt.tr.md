`dag_shortest(n, edges, start)` fonksiyonunu yaz: düğümler `0`..`n − 1`,
kenarlar `[a, b, ağırlık]` yönlü ve **döngüsüz**; ağırlık negatif olabilir.
Her düğüme `start`'tan en kısa uzaklığı liste olarak döndürsün; ulaşılamayana
`None`.

Önce topolojik sıra (Kahn), sonra o sırayla her düğümün çıkan kenarlarını
gevşet: `O(n + m)`, negatif kenar sorun değil.

**Beklenen çıktı:**

```
[0, 2, -1, 0, -2]
```
