## Üç algoritma bir bakışta

| | Kabarcık | Seçmeli | Eklemeli |
|---|---|---|---|
| Fikir | Komşuları yer değiştir, büyük sona çıksın | Kalanların en küçüğünü başa koy | Sıradakini sıralı kısımda yerine kaydır |
| En iyi durum | `O(n)` (erken çıkışla, sıralı liste) | `O(n²)` | `O(n)` (sıralı liste) |
| Ortalama / en kötü | `O(n²)` | `O(n²)` | `O(n²)` |
| Ek bellek | `O(1)` | `O(1)` | `O(1)` |
| Kararlı mı? | evet | hayır | evet |
| Ne zaman? | öğretmek için | yazma çok pahalıysa | küçük ya da neredeyse sıralı liste |

Üçü de **yerinde (in-place)** sıralar: listenin kopyası değil, kendisi
değişir (derste kopyasını sıraladık ki asıl liste korunsun).

## Döngü sınırları

```python
# Kabarcık: her geçişte sondaki doğru yere oturur
for end in range(n - 1, 0, -1):
    for i in range(end):              # items[i] ile items[i + 1]

# Seçmeli: start'tan sonrasının en küçüğü
for start in range(n - 1):
    for i in range(start + 1, n):

# Eklemeli: 0..i-1 sıralı, items[i]'yi yerleştir
for i in range(1, n):
    j = i - 1
    while j >= 0 and items[j] > current:
```

## Kararlılığı bozmamak için

Eşit elemanları **yer değiştirme**: karşılaştırmada `>` kullan, `>=` değil.
Eklemeli sıralamada `items[j] >= current` yazmak, eşit elemanı ötekinin
önüne geçirir ve kararlılık gider.

## Ters sayımı (inversion)

Bir listede yanlış sırada duran ikililerin (`i < j` ama `items[i] >
items[j]`) sayısına **ters sayım** denir. Kabarcığın yer değiştirme sayısı
ve eklemelinin kaydırma sayısı tam olarak ters sayım kadardır (derste ikisi
de 250 393 çıktı). Sıralı listede 0, ters sıralı listede `n(n−1)/2`.
