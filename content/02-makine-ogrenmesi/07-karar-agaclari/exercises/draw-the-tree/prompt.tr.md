Kuralları metin olarak okudun. Şimdi ağacın kendisini **çizeceksin** — ve
hangi sütunun ne kadar iş gördüğünü ölçeceksin.

**Yapman gerekenler:**

1. Aynı akışı kur, **`max_depth=2`** ile ağacı eğit (`random_state=42`).
2. Her sütunun **önem** değerini yazdır: tek satır, **sütun adı ve değer**
   (üç ondalık).
3. **En önemli** sütunun adını yazdır.
4. Ağacı çiz: `plot_tree` ile, `feature_names` ver, sınıf adları
   `stays` ve `leaves`, kutular renkli (`filled=True`).
5. `chart.png` olarak kaydet.

**Beklenen çıktı:**

```
age 0.0
income 0.454
visits 0.546
visits
```

Ağacın çizimi çalıştırma sonrası **sonuç panelinde** görünecek.

**Çizimde her kutuda beş satır var:**

| Satır | Anlamı |
|---|---|
| `visits <= 18.5` | Bu düğümün sorusu |
| `gini = 0.425` | Safsızlık: 0 saf, 0.5 en karışık |
| `samples = 150` | Bu düğüme kaç kayıt düşmüş |
| `value = [104, 46]` | Sınıflara göre dağılım |
| `class = stays` | Çoğunluk sınıfı |

**Sayılara dikkat: `age` sütununun önemi tam 0.0.**

Derinlik 2'lik bir ağaçta yalnızca üç bölünme var ve hiçbiri `age`
kullanmamış. Ama bu, **yaşın önemsiz olduğu anlamına gelmiyor** — yalnızca
"bu ağaçta sıra ona gelmedi" demek. Derinliği 3 yapsan `age` da işe
karışıyor ve önemi 0.169'a çıkıyor.

**Özellik öneminin üç tuzağı var:**

1. **Önem sebep demek değil.** "`visits` en önemli" cümlesinden "müşteriyi
   daha çok girmeye ikna edersek kalır" sonucu çıkmıyor. Belki az giren
   müşteriler zaten ayrılmaya karar vermiş olanlar; o durumda ziyaret sayısı
   bir **sonuç**, sebep değil.

2. **İlişkili sütunlar önemi paylaşıyor.** İki sütun neredeyse aynıysa ağaç
   birini seçiyor, öteki sıfıra yakın önem alıyor. Buradaki `age = 0.0` da
   kısmen bu — ama asıl sebebi derinlik sınırı.

3. **Çok değerli sütunlar şişiyor.** Sürekli sayısal bir sütunda binlerce
   olası eşik var; ağaç orada tesadüfen iyi bir bölünme bulmakta daha
   şanslı. Uç örneği: veriye **müşteri numarası** koyarsan ağaç onunla her
   kaydı ayırabiliyor ve o sütun en önemli görünüyor — hiçbir bilgi
   taşımadığı hâlde.

Daha güvenilir bir ölçü `permutation_importance`: bir sütunu karıştırıp
skorun ne kadar düştüğüne bakıyor ve test kümesinde ölçülebiliyor.
