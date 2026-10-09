`count_sum_k(values, k)` fonksiyonunu **önek toplamı + sözlükle** yaz:
toplamı tam `k` olan ardışık parça sayısını döndürsün. Sayılar negatif
olabilir.

1. Sözlüğü `{0: 1}` ile başlat.
2. Her elemanda önek toplamını güncelle; `seen.get(total - k, 0)` kadar
   parça ekle; sonra `total`'ın sayacını artır.

**Hız şartı:** kodun sonunda 100 000 sayılık bir liste sayılıyor; her parçayı
denemek 5 milyar adım.

**Beklenen çıktı:**

```
4
6
11656430
```
