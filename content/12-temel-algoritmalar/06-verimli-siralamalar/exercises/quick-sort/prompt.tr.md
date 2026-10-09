`quick_sort(items)` fonksiyonunu **özyinelemeyle** yaz: listenin sıralı
bir kopyasını döndürsün.

1. 0 ya da 1 elemanlı liste zaten sıralı.
2. Pivotu **rastgele** seç: `random.choice(items)`.
3. Listeyi üçe ayır: pivottan küçükler, **pivota eşitler**, büyükler.
4. Küçükleri ve büyükleri `quick_sort` ile sırala; sonucu
   `küçükler + eşitler + büyükler` diye birleştir.

Eşitleri ayrı tutmak, aynı değerden çok olan listelerde iki tarafın
dengesiz kalmasını önler.

**Hız şartı:** kodun sonunda zaten sıralı, 20 000 elemanlı bir liste
sıralanıyor. Son elemanı pivot alsaydın derinlik sınırına takılırdın;
rastgele pivotla sorun yok.

**Beklenen çıktı:**

```
[1, 2, 3, 6, 6, 6, 9]
[]
True
```
