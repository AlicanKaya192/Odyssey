## İki yol

| | Kahn | DFS |
|---|---|---|
| Fikir | bekleyeni olmayanı al, sayaçları azalt | önce bağımlılıkları bitir |
| Yapı | kuyruk (ya da heap) + giren derece | özyineleme + üç durum |
| Döngü | sıra eksik kalır | `active` düğüme yeniden gelinir |
| Maliyet | `O(n + m)` | `O(n + m)` |

Topolojik sıra çoğunlukla **tek değildir**: birbirini beklemeyen işler
(`clean` ile `validate`) her iki sırada da olabilir. Belli bir sıra
isteniyorsa (alfabetik) kuyruk yerine heap.

## Nerede?

- Ders ön koşulları, kurulum sırası (paket bağımlılıkları; `pip` de böyle
  çözer)
- Derleme sistemleri: önce değişen dosyaya bağlı olanlar
- Tablo hesapları: hücre, kullandığı hücrelerden sonra hesaplanır
- Veri hatları: Airflow, dbt, Prefect işleri DAG olarak tanımlar
- Sinir ağlarında ileri geçiş: hesap grafı topolojik sırayla yürütülür,
  geri yayılım ters sırayla

## DAG'de en kısa ve en uzun yol

DAG'de topolojik sırayla tek geçişte gevşetmek, negatif kenar olsa bile en
kısa yolu `O(n + m)`'de verir (Dijkstra'dan hızlı). Aynı geçişle `max`
alınırsa **en uzun yol**: kritik yol. Döngülü genel grafta en uzun yol çok zor
bir problemdir; DAG'de kolay.

## Sık hatalar

- Okun yönünü karıştırmak: "`clean`, `extract`'ı bekler" ile "`extract` →
  `clean`" aynı şey; kenarı ters eklemek sırayı ters çevirir.
- Hiç bağımlılığı olmayan ve hiçbir işin beklemediği işi unutmak: düğüm
  kümesi hem anahtarlardan hem değerlerden kurulur.
- Döngüyü sessizce yutmak: Kahn'da `len(order) < len(nodes)` denetimi şart.
