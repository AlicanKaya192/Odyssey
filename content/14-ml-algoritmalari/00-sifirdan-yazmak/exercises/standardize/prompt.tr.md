`standardize(train, test)` fonksiyonunu yaz: ortalama ve standart sapmayı
**yalnızca eğitim** verisinden (sütun başına, `ddof=0`) hesapla ve **test**
verisini `(x − ortalama) / sapma` ile ölçekle. Sonucu
`.round(3).tolist()` ile döndürsün.

scikit-learn'ün `StandardScaler`'ı yok.

**Beklenen çıktı:**

```
[[0.0, 0.566], [-2.236, -2.828]]
```
