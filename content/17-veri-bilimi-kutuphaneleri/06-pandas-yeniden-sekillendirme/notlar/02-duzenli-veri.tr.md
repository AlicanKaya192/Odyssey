"Hangi biçim doğru?" sorusunun bir adı var: **düzenli veri** (tidy data).
Üç kuralı var:

1. Her **değişken** bir sütun (şehir, yıl, puan).
2. Her **gözlem** bir satır (bir öğrencinin bir yıldaki puanı).
3. Her hücrede **tek** değer.

Geniş tablo birinci kuralı çiğner: `score_2024` ve `score_2025` iki ayrı
sütun ama aslında tek değişken (puan) ile bir başka değişkenin (yıl) iki
değeri. Yıl, sütun **adının içine** gizlenmiş.

```python
import pandas as pd

wide = pd.DataFrame({"id": [1, 2], "score_2024": [60, 75], "score_2025": [70, 80]})
long = pd.wide_to_long(wide, stubnames="score", i="id", j="year", sep="_")
print(long.reset_index().values.tolist())
```

```text
[[1, 2024, 60], [2, 2024, 75], [1, 2025, 70], [2, 2025, 80]]
```

- `wide_to_long` bu kalıp için yazılmış: `stubnames="score"` sütun adının
  ortak başı, `sep="_"` ayırıcı, adın geri kalanı (`2024`) `j="year"`
  sütununa gider ve **sayıya çevrilir**.
- `melt` ile de yapılabilirdi, ama sonra `"score_2024"` metninden yılı ayrıca
  kesip sayıya çevirmek gerekirdi.

## Neden uğraşalım?

- `groupby("year")`, `df[df["year"] == 2025]`, grafikte `hue="year"`: hepsi
  yıl bir **sütun** olunca tek satır. Geniş tabloda her yeni yıl kodda yeni bir
  sütun adı demek.
- Üçüncü kural (tek değer) `explode`'un konusu: `"gift,fast"` bir hücrede iki
  değer; açılmadan saymak mümkün değil.

## Rapor geniş, analiz uzun

Düzenli veri **analiz** içindir. İnsana gösterilecek son tablo genellikle
geniştir (aylar yan yana). Akış şu: veriyi uzun biçime getir → hesapla →
sonucu göstermek için `pivot_table` ile genişlet.
