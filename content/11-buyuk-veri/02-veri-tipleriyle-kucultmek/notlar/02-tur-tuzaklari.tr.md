Tür değiştirmek çoğu zaman sessiz: yanlış bir şey olursa pandas çoğunlukla
hata vermiyor, sonuç yanlış çıkıyor. Bu sayfadaki her tuzak bu makinede
denendi.

## 1. `astype` taşanı bozar

```python
pd.Series([100, 200, 300]).astype("int8").tolist()
# [100, -56, 44]
```

Hata yok, uyarı yok. Önce `min()` / `max()`'a bak ya da
`pd.to_numeric(..., downcast="integer")` kullan.

## 2. Hesap da taşar

```python
small = pd.Series([100, 120, 127]).astype("int8")
(small + 1).tolist()
# [101, 121, -128]
```

Sütun küçük bir türdeyse ona eklenen, çarpılan sonuç da aynı türde kalıyor.
Toplam ya da çarpım büyüyecekse önce genişlet: `small.astype("int64") * 1000`.

## 3. `float32` toplamı kayar

Bir milyon fiyatın toplamı `float32` içinde 15 TL sapıyor. Saklarken
`float32`, toplarken `float64`:

```python
total = prices32.astype("float64").sum()
```

## 4. Farklı değeri çok olan metin `category` olunca büyür

984 369 farklı değerli `order_time` sütunu `category` olunca 25,8 MB'tan
29,3 MB'a çıktı. Önce `nunique()`.

## 5. `category` sütununa listede olmayan değer yazılamaz

```python
c = pd.Series(["card", "cash", "card"], dtype="category")
c[0] = "crypto"
# TypeError: Cannot setitem on a Categorical with a new category (crypto) ...
```

Önce kategoriyi ekle: `c = c.cat.add_categories(["crypto"])`.

## 6. Kategorileri farklı iki sütun birleşince tür kaybolur

```python
a = pd.Series(["x", "y"], dtype="category")
b = pd.Series(["y", "z"], dtype="category")
pd.concat([a, b]).dtype      # str
pd.concat([a, a]).dtype      # category
```

Parça parça okuyup birleştirirken (Bölüm 3) sonucu yeniden `category`
yapman gerekebilir.

## 7. Eksik değer tam sayıyı ondalıklı yapar

```python
pd.Series([1, 2, None, 4]).dtype     # float64
```

Eksik değerli tam sayı için büyük harfli `Int8` … `Int64`.

## 8. Tarihte gün mü ay mı?

```python
pd.to_datetime(pd.Series(["03/04/2024"])).iloc[0].month                 # 3
pd.to_datetime(pd.Series(["03/04/2024"]), dayfirst=True).iloc[0].month   # 4
```

pandas varsayılan olarak ayı önce okuyor (Amerikan biçimi). Türkiye'deki
gibi gün önce yazılmışsa `dayfirst=True` ya da daha iyisi açık bir biçim:
`format="%d/%m/%Y"`.
