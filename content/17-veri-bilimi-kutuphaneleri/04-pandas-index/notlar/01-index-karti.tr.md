## Index

| Yazım | Ne yapar |
|---|---|
| `df.set_index("a")` | sütunu indekse taşır |
| `df.set_index(["a", "b"])` | iki düzeyli MultiIndex |
| `df.reset_index()` | indeksi sütuna geri çevirir |
| `df.loc[etiket]` / `df.iloc[konum]` | etiketle / konumla seçim |
| `s1.add(s2, fill_value=0)` | eksik tarafı 0 sayarak toplar |
| `s.reindex(liste)` | etiketleri verilen sıraya dizer, olmayana `NaN` |
| `idx.is_unique` / `idx.duplicated()` | tekrar denetimi |
| `set_index(..., verify_integrity=True)` | tekrar varsa hata |
| `df.sort_index()` | indekse göre sıralar |

## MultiIndex

| Yazım | Ne yapar |
|---|---|
| `m.loc[("Izmir", 2025)]` | tam etiket (demet) |
| `m.loc["Izmir"]` | dış düzey; o düzey düşer |
| `m.xs(2025, level="year")` | iç düzeyden seçim |
| `m.loc[pd.IndexSlice["A":"B", 2024], :]` | iki düzeyde dilim |
| `m.index.get_level_values("city")` | bir düzeyin etiketleri |
| `m.swaplevel()` | düzeylerin yerini değiştirir |
| `m.droplevel("year")` | bir düzeyi atar |
| `g.unstack()` | iç düzeyi sütunlara çevirir |
| `g.groupby(level="city").sum()` | bir düzey üzerinden toplar |

## Hatalar

| Belirti | Sebep |
|---|---|
| Toplamda beklenmedik `NaN` | etiketler eşleşmiyor (hizalama) |
| Tam sayılar `float64` oldu | hizalamada çıkan `NaN` |
| `.values` ile yanlış toplam | etiket atıldı, sıraya göre toplandı |
| `loc` bazen seri döndürüyor | tekrarlı etiket |
| `cannot reindex on an axis with duplicate labels` | tekrarlı etiket |
| `UnsortedIndexError ... lexsort depth` | dilimden önce `sort_index()` yok |
| `KeyError` iç düzey değerinde | `loc` dış düzeye bakıyor; `xs` kullan |
