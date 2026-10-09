Yanında bir `app` klasörü var: `main.py`, `utils.py`, `cache.tmp`,
`temp/output.txt`, `data/config.json`.

`clean_release(src, dst)` fonksiyonunu yaz: `src`'yi `dst`'ye kopyalasın,
ama `*.tmp` dosyalarını ve `temp` klasörünü atlasın; `dst` zaten varsa üstüne
kopyalasın. Sonunda `dst`'deki **dosyaların** göreli, `/` ayıraçlı yollarını
sıralı liste olarak döndürsün.

**Beklenen çıktı:**

```
data/config.json
main.py
utils.py
```
