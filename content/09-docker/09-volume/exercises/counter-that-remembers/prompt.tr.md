`counter.py` her çalıştığında sayacı bir artırıyor. Ama sayacı çalışma
klasörüne (`/app/count.txt`) yazıyor: her yeni konteyner sıfırdan başlıyor.

**Yapman gereken:** sayacın dosyasını volume'a bağlanan klasöre taşı:
`/data/count.txt`.

Odyssey iki ayrı konteyner çalıştıracak, ikisine de `-v counter:/data`
bağlayarak.

**Beklenen çıktılar:**

```
count: 1
count: 2
```
