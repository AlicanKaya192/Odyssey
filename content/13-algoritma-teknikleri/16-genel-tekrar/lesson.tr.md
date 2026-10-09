# Genel Tekrar

ALG 2'nin sonuna geldin. ALG 1'de maliyeti ölçmeyi ve temel yapıları
öğrenmiştin; burada **problem çözme tekniklerini** öğrendin: problemi
parçalamak, akıllıca denemek, tekrar eden işi saklamak, ilişkileri graf olarak
görmek ve kesin cevap pahalıysa iyi bir tahminle yetinmek. Bu bölüm her
tekniğin özünü ve ölçtüğümüz en önemli sayıları bir arada topluyor.

<figure class="fig">
  <div class="flow">
    <span class="node">Teknikler<br><small>00–04</small></span><span class="arrow">→</span>
    <span class="node">Graflar<br><small>05–09</small></span><span class="arrow">→</span>
    <span class="node">Metin, sayı<br><small>10–11</small></span><span class="arrow">→</span>
    <span class="node">Rastgelelik<br><small>12–13</small></span><span class="arrow">→</span>
    <span class="node acc">Sezgisel, kalıp<br><small>14–15</small></span>
  </div>
  <figcaption>ALG 2'nin yolu: önce genel teknikler, sonra graflar, sonra özel alanlar ve yaklaşık yöntemler.</figcaption>
</figure>

## 1. Böl ve fethet (Bölüm 0)

Problemi aynı türden küçük parçalara böl, parçaları çöz, sonuçları birleştir.
Maliyeti **özyineleme ağacı** söyler: her seviyenin işi × seviye sayısı. Merge
sort'ta her seviye `n`, seviye sayısı `log n` → `O(n log n)`. Karatsuba dört
yarım çarpım yerine üç yaparak `n²`'yi `n^1,58`'e indirir. Parçalar örtüşüyorsa
böl ve fethet aynı işi tekrar eder; orada DP gerekir.

## 2. Geri izleme (Bölüm 1)

Seç, keşfet, geri al. Bütün alt kümeleri ve sıralanışları üretir; gücü
**budamadan** gelir: işe yaramayacağı belli olan dalı hiç açmamak. Sekiz
vezirin 92 çözümü yalnızca 2057 düğüm gezilerek bulundu.

## 3. Açgözlü algoritmalar (Bölüm 2)

Her adımda o an en iyi görüneni seç, geri dönme. Hızlıdır ama **her zaman
doğru değildir**: toplantı seçiminde "en erken biten" doğru, "en kısa" yanlış;
kesirli sırt çantasında doğru, bütün sırt çantasında yanlış. Doğruluğu bir
**değiş tokuş** argümanıyla gösterilir. Huffman kodlaması da açgözlüdür.

## 4. Dinamik programlama (Bölüm 3–4)

Örtüşen alt problemleri **bir kez** çöz ve sakla. `fib(30)`'da 2 692 537
çağrı bellekle 59'a indi. Tarif: durumu tanımla, geçişi yaz, başlangıç
değerlerini koy, sırayı belirle, cevabı oku.

| Problem | Durum | Maliyet |
|---|---|---|
| En az para | `dp[tutar]` | `O(tutar × para)` |
| 0/1 sırt çantası | `dp[kapasite]` (ters gez) | `O(n × kapasite)` |
| LCS, düzenleme uzaklığı | `dp[i][j]` | `O(n × m)` |
| LIS | `tails` + `bisect` | `O(n log n)` |
| Kadane | sonda biten en iyi | `O(n)` |

## 5. Graflar (Bölüm 5–9)

Düğümler ve kenarlar; Python'da çoğunlukla **komşuluk listesi** (sözlük).

| Soru | Algoritma | Maliyet |
|---|---|---|
| En az adım (ağırlıksız) | BFS | `O(n + m)` |
| Bağlı bileşenler, döngü | DFS / BFS | `O(n + m)` |
| En kısa yol (negatif yok) | Dijkstra (heap) | `O(m log n)` |
| Negatif kenar | Bellman-Ford | `O(n · m)` |
| Bütün çiftler | Floyd–Warshall | `O(n³)` |
| Hedef biliniyorsa | A* (tahmin + maliyet) | çoğu zaman Dijkstra'dan az düğüm |
| Bağımlılık sırası | Kahn / DFS | `O(n + m)` |
| En ucuz bağlantı | Kruskal / Prim | `O(m log m)` |
| Aynı grupta mı? | birleşim-bulma | pratikte sabit |

Veri hattında 19 saatlik iş, paralel çalışabilen işler sayesinde 18 saatte
bitti: **kritik yol**. Kruskal'ı `k` grupta durdurmak tek bağlantılı
kümelemeyi verdi ve scikit-learn ile aynı grupları buldu.

## 6. Metin ve sayı algoritmaları (Bölüm 10–11)

- **KMP** önek tablosuyla metinde geri dönmeden arar: kötü durumda saf arama
  yarım milyondan fazla, KMP yaklaşık yirmi bin karşılaştırma.
- **Rabin-Karp** kayan hash ile pencereyi tek sayıyla karşılaştırır; çok kalıp
  ve kopya bulmada güçlü. **Trie** önek aramasını önek uzunluğu kadar adıma
  indirir.
- **Öklid** `gcd(a, b) = gcd(b, a % b)`; **kalbur** 100 000'e kadar deneme
  bölmesinden yaklaşık 14 kat az işle asalları bulur; **hızlı üs alma** bir
  milyonluk üssü 27 çarpmayla hesaplar.

## 7. Rastgelelik ve olasılıksal yapılar (Bölüm 12–13)

- **Quickselect** ortalama `O(n)`; rastgele pivot en kötü durumu olasılıksız
  yapar. **Fisher-Yates** `randint(0, i)` ile yansız karıştırır.
  **Rezervuar örnekleme** akıştan `k` öğelik bellekle eşit olasılıklı örnek
  alır. Monte Carlo hatası `1/√n` gibi küçülür.
- **Bloom filtresi** "kesinlikle yok / muhtemelen var" (derste %0,73 yanlış
  pozitif), **Count-Min** yalnızca fazla tahmin eder, **HyperLogLog** 1024
  sayaçla farklı öğe sayısını %4'ün altında hatayla tahmin etti, **MinHash**
  Jaccard benzerliğini küçük imzalarla tahmin eder.

## 8. Sezgisel yöntemler ve kalıplar (Bölüm 14–15)

- Kaba kuvvet küçükte mümkün, büyükte imkânsız: 60 şehirde 80 basamaklı tur
  sayısı. En yakın komşu + 2-opt rastgele turun 3155'ini 690'a indirdi.
  Tavlama benzetimi kötü adımı azalan olasılıkla kabul ederek çukurdan çıkar.
- Önce bütçe: `n` ~20 → `2ⁿ`, ~1000 → `n²`, ~10⁶ → `n log n`. Cevap üzerinde
  ikili arama, monoton yığın, durum uzayında BFS, ortada buluşma. Hızlı
  çözümü kaba kuvvete karşı rastgele girdilerle sına.

## Hangi soruya hangi teknik?

| Problemde şu varsa | Teknik |
|---|---|
| Parçalar bağımsız, birleştirmesi ucuz | böl ve fethet |
| Bütün seçenekler gerekli, erken eleme mümkün | geri izleme + budama |
| Yerel en iyi seçim güvenli (kanıtlanabilir) | açgözlü |
| "En iyi / kaç yol" + örtüşen alt problemler | dinamik programlama |
| İlişkiler, ağlar, bağımlılıklar | graf algoritmaları |
| Çok büyük veri, yaklaşık cevap yeter | olasılıksal yapılar, örnekleme |
| Kesin çözüm pahalı, iyi çözüm yeter | sezgisel yöntemler |

## Özet

ALG 2'deki her teknik aynı soruya farklı bir cevap: **tekrar eden ya da
gereksiz işi nasıl atarım?** Bölerek, budayarak, saklayarak, grafın yapısını
kullanarak ya da kesinlikten biraz vazgeçerek. ALG 3'te bu araçlar makine
öğrenmesi algoritmalarının içinde yeniden karşına çıkacak.
