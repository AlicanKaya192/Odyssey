Kârı en büyük eşiği seçen `best_threshold(probs, labels, candidates, saved, cost)` fonksiyonunu yaz:

- `candidates` içindeki her eşik için kârı hesapla: olasılığı en az eşik olan her müşteri için `saved * etiket - cost`.
- En büyük kârı veren eşiği seç; eşitlikte listede önce geleni.
- `[eşik, kâr]` döndür.

**Beklenen çıktı:**

```
[0.3, 34]
[0.7, -1]
```
