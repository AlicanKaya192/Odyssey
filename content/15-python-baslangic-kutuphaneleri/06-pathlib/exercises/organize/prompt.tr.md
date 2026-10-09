Yanında `inbox` klasörü var: `photo.jpg`, `report.pdf`, `data.csv`,
`notes.txt`, `scan.PDF`, `README`.

`organize(folder)` fonksiyonunu yaz: klasördeki her **dosyayı** uzantısının
küçük harfli, noktasız adını taşıyan alt klasöre taşısın (`scan.PDF` →
`pdf/`); uzantısı yoksa `other/`. Sonunda klasördeki bütün dosyaların
göreli, `/` ayıraçlı yollarını **sıralı** liste olarak döndürsün. İkinci
kez çağrılınca bir şey taşımadan aynı listeyi vermeli.

**Beklenen çıktı:**

```
csv/data.csv
jpg/photo.jpg
other/README
pdf/report.pdf
pdf/scan.PDF
txt/notes.txt
```
