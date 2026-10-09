## Karşılaştırma

| | Merge sort | Quick sort | Timsort (`sorted`) |
|---|---|---|---|
| Fikir | böl, iki yarıyı sırala, birleştir | pivotun etrafında ayır, iki yanı sırala | koşuları bul, küçükleri eklemeliyle düzelt, birleştir |
| En iyi | `O(n log n)` | `O(n log n)` | `O(n)` (sıralı veri) |
| Ortalama | `O(n log n)` | `O(n log n)` | `O(n log n)` |
| En kötü | `O(n log n)` | `O(n²)` (kötü pivot) | `O(n log n)` |
| Ek bellek | `O(n)` | yerinde sürümde `O(log n)` (yığın) | `O(n)` |
| Kararlı mı? | evet | genelde hayır | evet |

## Birleştirme (merge) tek başına da işe yarar

İki sıralı listeyi birleştirmek `O(n + m)`; bu işlem sıralamanın dışında da
sık çıkar:

- İki sıralı dosyayı (log kayıtları, işlemler) tek sıraya dizmek
- Belleğe sığmayan veriyi sıralamak (**dış sıralama**): parçaları ayrı ayrı
  sırala, diske yaz, sonra parçaları birleştir
- `heapq.merge(*listeler)`: Python'un hazır çoklu birleştirmesi

## Pivot seçimi

| Seçim | Sıralı girdide | Not |
|---|---|---|
| İlk ya da son eleman | `O(n²)`, derin özyineleme | kullanma |
| Rastgele eleman | beklenen `O(n log n)` | basit ve güvenli |
| Üçün ortancası (ilk, orta, son) | `O(n log n)` | kötü girdi üretmek zorlaşır |

## Ne zaman hangisi?

- Python'da: **her zaman `sorted` / `list.sort`.**
- Kararlılık şart ve bellek sorun değilse: merge sort.
- Bellek az, ortalama hız önemli: yerinde quick sort (C kütüphanelerinin
  çoğu bunun bir türünü kullanır).
- Veri belleğe sığmıyor: parça parça sırala + birleştir (Büyük Veri
  patikasındaki parça parça okuma ile aynı fikir).
