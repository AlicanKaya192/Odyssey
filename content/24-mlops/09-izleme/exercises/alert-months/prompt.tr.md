Dersteki `alert_months(values, reference, limit, patience)` fonksiyonunu yaz. `values` aylık bir ölçü (0. aydan başlıyor):

- Bir ayın değeri `reference`'tan `limit`'ten **fazla** uzaksa o ay eşik aşılmış sayılır.
- Üst üste kaç ay aşıldığını say; aşılmayan ayda sayaç sıfırlanır.
- Sayaç `patience`'a ulaştığı ve geçtiği her ayı listeye ekle.

**Beklenen çıktı:**

```
[3, 4, 5, 6, 7]
[4, 5, 6, 7]
[]
```
