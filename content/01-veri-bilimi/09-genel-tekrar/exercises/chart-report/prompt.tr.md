Gruplama ile görselleştirmeyi birleştireceksin: hesapla, çiz, kaydet.

**Yapman gerekenler:**

1. Şehre göre not ortalamasını hesapla, tek ondalığa yuvarla ve **sözlük
   olarak** yazdır.
2. Bir tuval ve çizim alanı oluştur.
3. Ortalamaları çubuk grafik olarak çiz.
4. Ekseni **0 ile 100 arasına** zorla.
5. Başlığı `Average score by city`, y eksenini `Score` yap.
6. `report.png` adıyla kaydet (`dpi=150`, `bbox_inches="tight"`) ve tuvali
   kapat.
7. Tek satırda yan yana yazdır: çubuk sayısı, eksenin üst sınırı (tam
   sayı), başlık ve dosyanın var olup olmadığı.

**Beklenen çıktı:**

```
{'Ankara': 80.0, 'Bursa': 45.0, 'Izmir': 76.5}
3 100 Average score by city True
```

**Bu, modülün en çok tekrarlanan kalıbı:**

```python
ortalama = data.groupby("city")["score"].mean()
ax.bar(ortalama.index, ortalama.values)
```

`groupby(...).mean()` bir seri döndürüyor — `index` gruplar, `values`
sayılar. Çubuk grafik ikisini ayrı istiyor.

**Ekseni sıfırdan başlatmak** burada bir tercih değil: çubuğun uzunluğu
değeri temsil ediyor, alt kısmı kesilirse grafik yalan söylüyor.

Ve grafik dosyaya kaydediliyor — rapora giren şey bu.
