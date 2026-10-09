## Bu bölümlerdeki bilgi nerede işine yarayacak?

- **Veri işlerken:** pandas ve SQL'in arkasında bu bölümlerdeki fikirler
  çalışıyor. `merge` ve `JOIN` hash tablosu, `CREATE INDEX` B-ağacı,
  `sort_values` bir sıralama algoritması, `rolling` kayan pencere, `cumsum`
  önek toplamı.
- **Makine öğrenmesinde:** karar ağacında tahmin kökten yaprağa bir yürüyüş,
  KNN en yakın `k` komşuyu (heap, k-d ağacı) arıyor, öneri sistemleri en iyi
  `k`'yı seçiyor.
- **Kod incelemesinde ve mülakatlarda:** "bu döngünün içindeki `in` ne kadar
  tutar?" sorusunu artık soruyorsun. Teknik mülakatların çoğu bu bölümlerdeki
  kalıpların biraz değiştirilmiş hâli.

## Nasıl pratik yapmalı?

1. Bir problemi okuyunca kod yazmadan önce **kaba kuvvet** çözümü ve
   maliyetini söyle (`O(n²)` gibi).
2. "Hangi soruya hangi araç?" tablosuna bak: tekrar eden iş nerede? Bir
   sözlük, işaretçi ya da önek toplamı onu kaldırır mı?
3. Uç durumları önceden yaz: boş girdi, tek eleman, hepsi aynı, negatifler.
4. Yazdıktan sonra büyük bir girdiyle **süreyi ölç**; beklediğin büyüme
   sınıfı mı?
5. Bir hafta sonra aynı problemi kâğıda bakmadan yeniden çöz.

Kod problemi siteleri (kolay ve orta seviye) bu bölümlerin alıştırmalarına
çok benziyor; "array", "hash table", "two pointers", "sliding window",
"stack", "tree", "heap" etiketleri doğrudan bu bölümlere karşılık geliyor.

## Sırada ne var?

**ALG 2 — Algoritma Teknikleri ve Graflar**

- Böl ve fethet, geri izleme, açgözlü algoritmalar
- Dinamik programlama (iki bölüm): tekrar eden alt problemleri bir kez çözmek
- Graflar, graf gezinme, en kısa yol (Dijkstra), topolojik sıralama, kapsayan
  ağaç ve birleşim-bulma
- Metin ve sayı algoritmaları, rastgele algoritmalar
- Olasılıksal veri yapıları (Bloom filtresi, HyperLogLog), sezgisel
  optimizasyon

**ALG 3 — Veri Bilimi ve Makine Öğrenmesi Algoritmaları**

Regresyon, gradyan inişi, karar ağaçları, topluluk yöntemleri, SVM,
kümeleme, PCA, sinir ağı ve öneri sistemleri NumPy ile sıfırdan.
