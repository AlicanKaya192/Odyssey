## Yavaştan hızlıya

| Yavaş | Hızlı |
|---|---|
| `for _, row in df.iterrows()` | `df["a"] * df["b"]` |
| `df.apply(f, axis=1)` | sütun işlemi ya da `np.where` / `np.select` |
| `g.agg(lambda s: s.sum())` | `g.sum()` ya da `g.agg("sum")` |
| grup toplamı + `merge` | `g.transform("sum")` |
| döngüde `concat` | parçaları listeye topla, bir kez `concat` |
| `s.apply(len)` | `s.str.len()` |

## Koşul

| Yazım | Ne yapar |
|---|---|
| `np.where(koşul, a, b)` | iki seçenek |
| `np.select([k1, k2], [a, b], default=c)` | çok seçenek; ilk tutan kazanır |
| `s.clip(0, 100)` | sınırlar arasına sıkıştırır |
| `s.where(koşul, diğer)` | koşul tutmayanı değiştirir |

## Bellek

| Yazım | Ne yapar |
|---|---|
| `df.memory_usage(deep=True).sum()` | gerçek bellek (metinler dahil) |
| `pd.to_numeric(s, downcast="integer")` | sığan en küçük tam sayı |
| `s.astype("float32")` | yarı bellek, ~7 basamak |
| `s.astype("category")` | az farklı değerli metin |
| `pd.read_csv(..., usecols=[...], dtype={...})` | okurken seç |

## Değiştirme (pandas 3)

| Yazım | Sonuç |
|---|---|
| `df.loc[koşul, "a"] = 1` | `df` değişir |
| `df[koşul]["a"] = 1` | hiçbir şey; `ChainedAssignmentError` uyarısı |
| `part = df[koşul]; part["a"] = 1` | yalnızca `part` değişir |
| `df.assign(a=...)` | yeni tablo; `df` aynı kalır |

## Zincir

```python
result = (
    df.assign(total=lambda d: d["qty"] * d["price"])
      .query("total > @limit")
      .groupby("city")["total"].sum()
)
```
