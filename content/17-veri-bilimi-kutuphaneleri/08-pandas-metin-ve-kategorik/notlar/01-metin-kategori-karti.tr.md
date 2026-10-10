## .str

| Yazım | Ne yapar |
|---|---|
| `s.str.strip()` / `.lower()` / `.title()` | boşluk ve harf temizliği |
| `s.str.len()` | uzunluk (eksik varsa ondalık) |
| <code>s.str.contains("a&#124;b", case=False, na=False)</code> | desen var mı |
| `s.str.contains(".", regex=False)` | düz metin arama |
| `s.str.startswith("TR")` | başlangıç |
| `s.str.replace(r"\d", "#", regex=True)` | desenle değiştirme |
| `s.str.extract(r"(?P<ad>...)")` | grupları sütunlara açar |
| `s.str.split("-", expand=True)` | parçaları sütunlara açar |
| `s.str[:2]` | dilim |

## category

| Yazım | Ne yapar |
|---|---|
| `s.astype("category")` | kategoriye çevirir |
| `s.cat.categories` / `s.cat.codes` | değer listesi / satır kodları |
| `pd.CategoricalDtype([...], ordered=True)` | sırayı sen verirsin |
| `s.cat.remove_unused_categories()` | kullanılmayanları atar |
| `groupby(..., observed=False)` | boş kategorileri de gösterir |
| `pd.cut(s, bins=[...], labels=[...])` | senin sınırlarınla sınıf |
| `pd.qcut(s, q=4)` | eşit sayıda gruba böl |

## Hatalar

| Belirti | Sebep |
|---|---|
| Aynı şehir birkaç kez sayıldı | boşluk ya da harf farkı; `strip`, `lower` |
| `Cannot mask with non-boolean array` | `object` türde eksik değer; `na=False` |
| `.` her şeyi buldu | desen düzenli ifade; `regex=False` |
| Bedenler `L, M, S, XL` sırasında | metin sıralaması; sıralı kategori |
| `cut` sonrası `NaN` | değer sınırların dışında |
| Raporda satırı olmayan kategori | kategori listesi veriden ayrı |
| Kategori bellek kazandırmadı | farklı değer sayısı çok |
