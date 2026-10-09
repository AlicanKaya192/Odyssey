## Birleşim-bulma

| İşlem | Ne yapar | Maliyet (iki hileyle) |
|---|---|---|
| `find(x)` | grubun kökünü verir | pratikte sabit |
| `union(a, b)` | iki grubu birleştirir, aynıysa `False` | pratikte sabit |
| `find(a) == find(b)` | aynı grupta mı? | pratikte sabit |

- **Boya göre birleştirme:** küçük grubun kökü büyüğün altına.
- **Yol kısaltma:** `find` geçtiği öğeleri köke yaklaştırır.
- Birleşim-bulma grupları **ayıramaz**: bir kenarı silmek desteklenmez.

## Kruskal mı Prim mi?

| | Kruskal | Prim |
|---|---|---|
| Fikir | ucuz kenardan pahalıya, döngü kurmayanı al | bir düğümden büyüt, en ucuz çıkan kenar |
| Yapı | sıralama + birleşim-bulma | heap + komşuluk listesi |
| Maliyet | `O(m log m)` | `O(m log n)` |
| Rahat olduğu yer | kenar listesi, seyrek graf | komşuluk listesi, yoğun graf |
| Kopuk graf | her parça için bir ağaç (orman) | yalnızca başladığı parça |

Ağırlıklar eşitse birden çok en küçük ağaç olabilir; **toplam** her zaman
aynıdır.

## Nerede?

- Ağ tasarımı: kablo, boru hattı, elektrik şebekesi
- Tek bağlantılı kümeleme (Kruskal'ı `k` grupta durdurmak)
- Görüntü bölütleme: komşu pikseller arasındaki farka göre birleştirme
- Gezgin satıcı problemi için hızlı bir alt sınır ve yaklaşık çözüm

## Sık hatalar

- `find` yerine doğrudan `parent[a] = b` yazmak: `a` ile `b`'nin **kökleri**
  birleştirilmeli, kendileri değil.
- Kruskal'da kenarları sıralamayı unutmak: ağaç kurulur ama en ucuzu olmaz.
- Prim'de heap'ten çıkan kenarın ucu zaten ağaçtaysa atlamamak: döngü.
- Kopuk grafta Kruskal'ın `n − 1`'den az kenar döndürdüğünü denetlememek.
