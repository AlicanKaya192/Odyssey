Doluluğu bir hedefin altında tutmak için gereken en az çalışanı bulan `workers_needed(rate, service_ms, target)` fonksiyonunu yaz:

- 1 çalışandan başla.
- Doluluk (`rate × service_ms / 1000 / workers`) `target`'tan büyük olduğu sürece bir çalışan ekle.
- Çalışan sayısını döndür.

**Beklenen çıktı:**

```
1
2
20
```
