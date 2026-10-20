Dersteki kayıt defterini, dosya yolunu parametre alacak biçimde yaz:

- `load_runs(path)`: dosya yoksa boş liste; varsa her satırı `json.loads` ile açıp liste döndür.
- `log_run(path, params, metrics)`: numara, dosyadaki deney sayısı + 1. `{"run": ..., "params": ..., "metrics": ...}` sözlüğünü `json.dumps` ile tek satır yap, dosyayı **ekleme** kipinde (`"a"`) açıp sonuna satır sonuyla birlikte yaz. Numarayı döndür.

**Beklenen çıktı:**

```
1
2
2 2 1
[]
```
