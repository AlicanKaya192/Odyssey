`split_path(path)` fonksiyonunu yaz: bir dosya yolunu
`(klasör, ad, uzantı)` demetine ayırsın. `os.path.split` klasörü ve dosya
adını, `os.path.splitext` adı ve uzantıyı verir.
Örnek: `"data/raw/sales.csv"` → `("data/raw", "sales", ".csv")`.

**Beklenen çıktı:**

```
('data/raw', 'sales', '.csv')
('', 'archive.tar', '.gz')
```
