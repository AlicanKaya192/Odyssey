## Bu teknikler nerede karşına çıkacak?

- **Makine öğrenmesinde:** karar ağacının en iyi bölmeyi seçmesi açgözlüdür;
  gradyan inişi yerel aramadır; k-ortalamalar bir yerel en iyiye iner; DTW ve
  dizi hizalama dinamik programlamadır; öneri sistemleri benzer kullanıcıları
  MinHash ve LSH ile bulur.
- **Veri mühendisliğinde:** iş hatları DAG'dir ve topolojik sırayla çalışır;
  büyük tablolarda farklı değer sayısı HyperLogLog ile, sık değerler
  Count-Min ile tahmin edilir; kopya kayıtlar birleşim-bulma ile gruplanır.
- **Mülakatlarda:** orta ve zor seviye soruların çoğu bu bölümlerin
  kalıpları: "graph", "dynamic programming", "backtracking", "greedy",
  "union find", "monotonic stack", "binary search" etiketleri.

## Nasıl pratik yapmalı?

1. Kod yazmadan önce bütçeyi kestir: `n` en fazla kaç, hangi karmaşıklık sığar?
2. Önce kaba kuvveti yaz; hızlı çözümü ona karşı rastgele girdilerle sına.
3. Takıldığında "Hangi soruya hangi teknik?" tablosuna dön.
4. DP'de önce durumu bir cümleyle tanımla; tablo ondan sonra gelir.
5. Bir hafta sonra aynı problemi kâğıda bakmadan yeniden çöz.

## Sırada ne var?

**Veri Bilimi ve Makine Öğrenmesi Algoritmaları**

Doğrusal ve lojistik regresyon, gradyan inişi, karar ağaçları, rastgele orman
ve gradyan artırma, k-en yakın komşu, k-ortalamalar ve DBSCAN, PCA, Naive
Bayes, SVM, EM, Apriori, PageRank, sinir ağı ve öneri sistemleri: hepsi
NumPy ile sıfırdan yazılıp scikit-learn ile karşılaştırılacak.
