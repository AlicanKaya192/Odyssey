## Genişten uzuna

| Yazım | Ne yapar |
|---|---|
| `df.melt(id_vars="city", var_name="month", value_name="sales")` | sütunları satırlara eritir |
| `df.melt(id_vars=..., value_vars=["jan", "feb"])` | yalnızca bazı sütunları |
| `df.stack()` | sütunları indeksin iç düzeyine indirir |
| `pd.wide_to_long(df, stubnames="score", i="id", j="year", sep="_")` | `score_2024` gibi adlardan |
| `df.explode("tags")` | listedeki her elemanı bir satır yapar |

## Uzundan genişe

| Yazım | Ne yapar |
|---|---|
| `df.pivot(index=, columns=, values=)` | yeniden düzenler; tekrarlı çiftte hata |
| `df.pivot_table(..., aggfunc="sum")` | tekrarları hesapla birleştirir |
| `pivot_table(..., fill_value=0)` | eksik hücreyi doldurur |
| `pivot_table(..., margins=True)` | satır ve sütun toplamları |
| `pd.crosstab(a, b)` | birlikte geçme sayısı |
| `s.unstack()` | iç düzeyi sütunlara çevirir |
| `s.unstack(fill_value=0)` | eksik hücreyi doldurarak |

## Sonrası

| Yazım | Ne yapar |
|---|---|
| `wide[["jan", "feb"]]` | sütunlara doğal sıra |
| `wide.reset_index().rename_axis(columns=None)` | düz tabloya döner |
| `long.dropna()` | pandas 3 `stack`'inin tuttuğu eksikleri atar |

## Hatalar

| Belirti | Sebep |
|---|---|
| `Index contains duplicate entries, cannot reshape` | `pivot`'ta tekrarlı çift |
| pivot_table beklenenden küçük sayılar | varsayılan `aggfunc` ortalama |
| Sütunlar `feb, jan` sırasında | sonuç alfabetik sıralanır |
| Tablonun sol üstünde ad | sütun ekseninin adı (`columns.name`) |
| stack sonrası beklenmedik `nan` | pandas 3 eksiği atmıyor |
| explode sonrası `loc` seri döndürüyor | indeks kopyalandı |
