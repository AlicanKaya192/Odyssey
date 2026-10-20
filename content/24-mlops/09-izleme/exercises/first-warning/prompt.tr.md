Birkaç izleme sinyalinin aylık sonucu bir sözlükte: `{ad: [ay 0'da çaldı mı, ay 1'de çaldı mı, ...]}`. `first_warning(signals)` fonksiyonunu yaz:

- Herhangi bir sinyalin çaldığı **ilk** ayı bul.
- `[ay, o ay çalan sinyallerin adları]` döndür; adlar abece sırasıyla.
- Hiçbir sinyal hiç çalmadıysa `None`.

Listelerin boyları farklı olabilir; bir sinyalin listesi bitmişse o aylarda çalmamış sayılır.

**Beklenen çıktı:**

```
[2, ['predicted_rate', 'usage_mean']]
None
```
