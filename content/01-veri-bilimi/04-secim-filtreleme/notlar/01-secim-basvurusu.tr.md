# Seçim Başvurusu

`data` bir DataFrame, `s` bir seri.

## iloc — sıraya göre

| Yazım | Ne seçer |
|---|---|
| `data.iloc[0]` | İlk satır (seri olarak) |
| `data.iloc[-1]` | Son satır |
| `data.iloc[0, 2]` | İlk satırın üçüncü sütunu |
| `data.iloc[1:3]` | 1. ve 2. satır — **bitiş hariç** |
| `data.iloc[:, 0]` | İlk sütunun tamamı |
| `data.iloc[:, [0, 2]]` | Birinci ve üçüncü sütun |
| `data.iloc[[0, 3], [1, 2]]` | Seçili satır ve sütunlar |
| `data.iloc[:5]` | İlk beş satır |

## loc — etikete göre

| Yazım | Ne seçer |
|---|---|
| `data.loc[0]` | `0` **etiketli** satır |
| `data.loc["Mina"]` | `Mina` etiketli satır |
| `data.loc["Mina", "score"]` | Tek hücre |
| `data.loc["Ada":"Mina"]` | Etiket aralığı — **bitiş dâhil** |
| `data.loc[:, "score"]` | Bir sütunun tamamı |
| `data.loc[:, "name":"score"]` | Sütun aralığı, bitiş dâhil |
| `data.loc[maske]` | Koşula uyan satırlar |
| `data.loc[maske, "score"]` | Koşula uyanların bir sütunu |

**Dilim kuralı farkı:** `iloc[1:3]` iki satır, `loc["a":"c"]` üç satır.

## Koşullu filtreleme

| Yazım | Ne yapar |
|---|---|
| `data[data["score"] > 80]` | Koşula uyan satırlar |
| `data[(a) & (b)]` | İki koşul birlikte |
| `data[(a) \| (b)]` | Ya biri ya öbürü |
| `data[~(a)]` | Koşulun tersi |
| `data[data["city"].isin([...])]` | Listedekilerden biri |
| `data[data["age"].between(20, 30)]` | Aralık — **iki uç dâhil** |
| `data[data["name"].str.contains("An")]` | Metin araması |
| `data[data["name"].str.startswith("A")]` | Baştan eşleşme |
| `data[data["score"].isna()]` | Eksik olanlar |
| `data[data["score"].notna()]` | Dolu olanlar |

`and`, `or`, `not` **çalışmıyor**; `&`, `|`, `~` kullanılıyor ve her koşul
parantez içine alınıyor.

## query

| Yazım | Ne yapar |
|---|---|
| `data.query("score > 80")` | Tek koşul |
| `data.query("score > 80 and city == 'Ankara'")` | `and` burada çalışıyor |
| `data.query("city in ['Ankara', 'Izmir']")` | `isin` karşılığı |
| `data.query("score > @limit")` | Dışarıdaki değişkeni `@` ile kullan |

Sütun adları tırnaksız, metin değerler tek tırnakta. Sütun adında boşluk
varsa ters tırnak: ``data.query("`my col` > 5")``.

## Sıralamaya bağlı seçim

| Yazım | Ne verir |
|---|---|
| `data.nlargest(3, "score")` | En büyük üç satır |
| `data.nsmallest(3, "score")` | En küçük üç satır |
| `data.sort_values("score").head(3)` | Aynısı, iki adımda |
| `data.loc[data["score"].idxmax()]` | En büyüğün **satırı** |
| `data.sample(3)` | Rastgele üç satır |

`nlargest` hepsini sıralamıyor, yalnızca en büyükleri buluyor; büyük veride
belirgin şekilde hızlı.

## Değer değiştirme

| Yazım | Ne yapar |
|---|---|
| `data.loc[maske, "score"] = 0` | Koşula uyanların bir sütununu değiştirir |
| `data.loc[maske, ["a", "b"]] = 0` | Birden fazla sütun |
| `data["score"] = data["score"].clip(0, 100)` | Sınırların dışını kırpar |
| `data["city"] = data["city"].replace({"izmir": "Izmir"})` | Değer düzeltir |
| `data.loc[:, "score"] = 0` | Sütunun tamamı |

**Her zaman tek bir `loc` çağrısı.** `data[maske]["score"] = 0` sessizce
hiçbir şey yapmıyor.

## Satır ve sütun atmak

| Yazım | Ne yapar |
|---|---|
| `data.drop(columns=["a"])` | Sütun atar |
| `data.drop(index=[0, 2])` | Etiketi verilen satırları atar |
| `data[data["score"].notna()]` | Eksik olanları atar (filtreyle) |
| `data.dropna(subset=["score"])` | Aynısı, hazır metotla |
| `data.drop_duplicates()` | Tekrar eden satırları atar |

## Yaygın birleşimler

```python
# Bir sehirdeki en yuksek notlu kisinin adi
selected = data[data["city"] == "Ankara"]
print(selected.loc[selected["score"].idxmax(), "name"])

# Iki kosula uyanlarin ortalamasi
mask = (data["score"] >= 70) & (data["age"] < 25)
print(data.loc[mask, "score"].mean())

# Kosula uyan satir sayisi
print((data["score"] >= 80).sum())
```

Son satırdaki numara: maske bir `True`/`False` serisi ve `sum()` onları
sayıyor — filtrelemeden kaç tane olduğunu öğrenmenin en kısa yolu.
