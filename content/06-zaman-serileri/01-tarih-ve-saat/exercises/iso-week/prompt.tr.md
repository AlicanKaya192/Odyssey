Haftalık bir rapor her tarihi `YIL-Whafta` biçiminde bir haftaya
atıyor: `2024-W10` gibi. Yıl sonundaki tarihler tuzaklı.

```python
days = ["2024-03-09", "2024-12-29", "2024-12-30", "2025-01-01", "2021-01-01"]
```

**Yapman gerekenler:**

1. Her metni `date.fromisoformat` ile tarihe çevir.
2. `isocalendar()` ile yılı ve hafta numarasını al.
3. Her satıra tarihi ve etiketi yazdır. Etiket, hafta numarası iki haneli
   olacak şekilde: `f"{year}-W{week:02d}"`.

**Beklenen çıktı:**

```
2024-03-09 2024-W10
2024-12-29 2024-W52
2024-12-30 2025-W01
2025-01-01 2025-W01
2021-01-01 2020-W53
```

30 Aralık 2024 ve 1 Ocak 2025 aynı haftada: 2025'in 1. haftası. 1 Ocak 2021
ise 2020'nin 53. haftası. Yılı `d.year`'dan alsaydın bu satırlar yanlış
yıla yazılacaktı.
