`unique_path(path)` fonksiyonunu yaz: `path` (bir `Path`) yoksa onu
döndürsün; varsa adının sonuna `-1`, `-2`... ekleyerek **olmayan** ilk yolu
döndürsün (`with_stem`, `exists`). `report.txt` ve `report-1.txt` varken
sonuç `report-2.txt`.

**Beklenen çıktı:**

```
report-1.txt
report-2.txt
new.txt
```
