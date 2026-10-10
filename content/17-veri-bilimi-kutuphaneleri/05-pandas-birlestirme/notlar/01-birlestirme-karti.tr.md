## Hangisi?

| İstek | Yazım |
|---|---|
| Anahtar sütunla eşleştir | `a.merge(b, on="key", how="left")` |
| Anahtar adları farklı | `a.merge(b, left_on="x", right_on="y")` |
| Anahtar indekste | `a.join(b)` ya da `merge(..., left_index=True, right_index=True)` |
| Aynı yapıdaki parçaları alt alta | `pd.concat(parcalar, ignore_index=True)` |
| Parçanın kaynağı belli olsun | `pd.concat(parcalar, keys=adlar)` |
| Yan yana (indekse göre) | `pd.concat([a, b], axis=1)` |
| En yakın zamana göre | `pd.merge_asof(a, b, on="time")` |

## how

| `how` | Kalan |
|---|---|
| `inner` | iki tarafta da olan anahtarlar (merge'ün varsayılanı) |
| `left` | soldakilerin hepsi (join'in varsayılanı) |
| `right` | sağdakilerin hepsi |
| `outer` | ikisinin hepsi |
| `cross` | her satır her satırla (anahtarsız) |

## Denetimler

| Yazım | Ne yapar |
|---|---|
| `indicator=True` | `_merge` sütunu: `both` / `left_only` / `right_only` |
| `validate="many_to_one"` | sağ tarafta anahtar tekrarlanırsa `MergeError` |
| `len(sonuc) == len(a)` | bilgi eklerken satır sayısı değişmemeli |
| `b["key"].is_unique` | eşleşilecek tarafın anahtarı benzersiz mi |
| `a["key"].dtype == b["key"].dtype` | anahtar türleri eşit mi |

## Hatalar

| Belirti | Sebep |
|---|---|
| Satırlar kayboldu | varsayılan `inner`; eşleşmeyen düştü |
| Satırlar çoğaldı, toplam büyüdü | sağ tarafta tekrarlı anahtar |
| `You are trying to merge on int64 and str columns` | anahtar türleri farklı |
| `sales_x`, `sales_y` sütunları | aynı adlı sütun; `suffixes` ver |
| Tam sayı sütunu ondalık oldu | eşleşmeyen satırda `NaN` |
| concat sonrası `loc` seri döndürüyor | tekrarlı indeks; `ignore_index=True` |
