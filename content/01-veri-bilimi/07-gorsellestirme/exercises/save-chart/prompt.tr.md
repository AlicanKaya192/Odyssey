Bir histogram çizip **dosyaya kaydedeceksin** — raporlamanın gerçek
adımı bu.

**Yapman gerekenler:**

1. `score` sütununun dağılımını gösteren bir **histogram** çiz, `bins=4`
   kullan.
2. Başlığı `Score distribution`, x eksenini `Score` yap.
3. Grafiği `chart.png` adıyla kaydet; `dpi=150` ve `bbox_inches="tight"`
   kullan.
4. Tuvali kapat.
5. Sırayla yazdır: dosya var mı, boyutu sıfırdan büyük mü, ve başlık.

**Beklenen çıktı:**

```
True
True
Score distribution
```

**Bilmen gerekenler:**

- **Histogram** çubuk grafikten farklı: orada kategoriler var, burada **sayı
  aralıkları**. `describe()` ortalamayı veriyordu, histogram **şekli**
  gösteriyor — iki tepe mi var, sağa mı yatık, uç değerler nerede.
- `dpi=150` rapora koyulacak kalitede çözünürlük veriyor.
- `bbox_inches="tight"` kenardaki fazla boşluğu kırpıyor; uzun etiketler
  kesilmesin diye.
- `plt.close(fig)` tuvali kapatıyor. Döngü içinde grafik üretiyorsan bu
  şart: yoksa açık tuvaller birikiyor ve matplotlib uyarı veriyor.

`plt.show()` diye bir çağrı da var ama Odyssey'de pencere yok; zaten
raporlama için dosyaya kaydetmek daha kullanışlı.
