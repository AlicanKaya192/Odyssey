Yanında bir `logs` klasörü var: `2025-11.txt`, `2025-12.txt`,
`2026-01.txt`, `2026-02.txt`, `README.txt`.

`archive_year(folder, year)` fonksiyonunu yaz: klasörde adı `{year}-` ile
başlayan `.txt` dosyalarını `folder/archive/{year}/` klasörüne taşısın
(`glob`, `shutil.move`) ve o arşiv klasöründeki dosya adlarını sıralı liste
olarak döndürsün. İkinci kez çağrılınca bir şey taşımadan aynı listeyi
vermeli.

**Beklenen çıktı:**

```
['2025-11.txt', '2025-12.txt']
['2026-01.txt', '2026-02.txt', 'README.txt']
```
