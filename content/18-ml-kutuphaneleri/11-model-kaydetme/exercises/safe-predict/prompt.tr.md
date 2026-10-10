`safe_predict(rows)` sözlük listesinden bir DataFrame kurup pozitif sınıfın
olasılıklarını (3 basamak) döndürüyor. Gelen sözlüklerde anahtarların sırası
karışık olabilir; model eğitimdeki sırayı (`COLUMNS`) bekliyor. Başlangıç
kodu sıralamadan veriyor ve hata alıyor.

**Beklenen çıktı:**

```
[0.978, 0.021]
```
