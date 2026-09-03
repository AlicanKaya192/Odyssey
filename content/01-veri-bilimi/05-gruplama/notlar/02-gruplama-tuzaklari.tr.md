## 1. Anahtarı eksik satırlar sessizce düşüyor

```python
d = pd.DataFrame({"g": ["a", "a", None], "v": [1, 2, 3]})
print(d.groupby("g")["v"].sum())
```

```text
g
a    3
Name: v, dtype: int64
```

Toplam 6 olması gerekirdi. Üçüncü satırın anahtarı boş olduğu için hiçbir
gruba girmedi ve **sonuçtan tamamen kayboldu**.

Hata yok, uyarı yok. Rapordaki toplam yanlış çıkıyor ve sebebini aramak
saatler alıyor.

**Görmek için:**

```python
d.groupby("g", dropna=False)["v"].sum()
```

**Alışkanlık:** gruplamadan önce `data["g"].isna().sum()` çalıştır.

## 2. `count()` ile `size()` aynı şey değil

```python
d = pd.DataFrame({"g": ["a", "a", "b"], "v": [1.0, None, 3.0]})
print(d.groupby("g")["v"].count().tolist())
print(d.groupby("g").size().tolist())
```

```text
[1, 1]
[2, 1]
```

`count()` **dolu** hücreleri, `size()` **bütün** satırları sayıyor.
`a` grubunda iki satır var ama biri boş.

"Grupta kaç kayıt var" diye `count()` yazarsan eksik değerli satırları
kaçırıyorsun.

## 3. Hesaplar eksikleri atlıyor

```python
print(d.groupby("g")["v"].mean())
```

```text
g
a    1.0
b    3.0
```

`a` grubunun ortalaması 1.0 çıktı çünkü ikinci değer boştu ve hesaba
girmedi. Bu, serideki davranışın aynısı: pandas eksikleri atlıyor.

Doğru mu? Duruma bağlı. Ama **kaç değerin atlandığını bilmeden** ortalamaya
güvenmemek gerekiyor. `count()` ile `size()` birlikte bakılıyor.

## 4. Tamamı boş grupta `sum()` sıfır veriyor

```python
d = pd.DataFrame({"g": ["a"], "v": [np.nan]})
print(d.groupby("g")["v"].sum())
```

```text
g
a    0.0
```

Hiç veri yok ama toplam 0.0 çıkıyor. `mean()` bu durumda `nan` veriyor,
`sum()` sıfır.

Sıfır ile "veri yok" aynı şey değil. Raporda sıfır gördüğünde bunun bir
ölçüm mü yoksa boşluk mu olduğunu ayırt etmen gerekiyor.

## 5. Grup anahtarı index'e taşınıyor

```python
result = data.groupby("city")["score"].mean()
print(result["Ankara"])       # calisir
print(result[0])              # calismaz - KeyError
```

`groupby` sonucunda anahtar **index** oluyor, sütun değil. Sonucu bir
tabloyla birleştirecekseniz sorun çıkarıyor.

İki çözüm:

```python
data.groupby("city", as_index=False)["score"].mean()   # sutun kalir
data.groupby("city")["score"].mean().reset_index()     # sonradan cevir
```

## 6. `[...]` ile `[[...]]` burada da fark ediyor

```python
data.groupby("c")["s"].mean()      # seri
data.groupby("c")[["s"]].mean()    # tek sutunlu tablo
```

DataFrame'deki aynı kural. Sonucu bir tabloyla birleştirecekseniz ikincisi,
üzerine `idxmax()` gibi seri metotları uygulayacaksanız birincisi.

## 7. `apply` yerine `agg`

```python
data.groupby("c")["s"].apply(lambda x: x.max() - x.min())   # calisir
data.groupby("c")["s"].agg(lambda x: x.max() - x.min())     # ayni sonuc, daha hizli
```

`apply` her grup için Python'a geri dönüyor ve grup nesnesini kuruyor;
`agg` daha doğrudan çalışıyor.

Hazır bir hesap varsa (`mean`, `sum`, `max`) metnini vermek en hızlısı:
`agg("mean")`. Lambda yalnızca hazırı olmayan hesaplar için.

## 8. Gruplar alfabetik sıralanıyor

```python
data.groupby("city")["score"].mean()
```

Sonuç alfabetik geliyor — veride hangi sırada olduklarından bağımsız.

Genelde iyi ama iki durumda sorun: sıralı bir anahtar varsa (ay adları,
"düşük/orta/yüksek") alfabetik sıra anlamsız oluyor.

Kendi sıranı istiyorsan sonradan sıralıyorsun:

```python
result.sort_values(ascending=False)
result.reindex(["dusuk", "orta", "yuksek"])
```

`sort=False` de verebiliyorsun; o zaman veride ilk görülme sırası korunuyor.

## 9. Pivot tablodaki `NaN` sıfır değil

```python
data.pivot_table(index="city", columns="grade", values="score", aggfunc="mean")
```

Boş hücreler o kombinasyonun **veride hiç olmadığı** anlamına geliyor.
Ankara'da C notu alan kimse yok — bu, "Ankara'da C ortalaması sıfır"
demek değil.

`fill_value=0` ile doldurabiliyorsun ama bunu yaparken ne dediğinin farkında
ol: sonraki hesaplarda o sıfırlar gerçek ölçüm gibi davranıyor ve
ortalamaları aşağı çekiyor.

## 10. `transform` ile `agg` karıştırılıyor

```python
data.groupby("city")["score"].mean()        # 3 satir (grup sayisi)
data.groupby("city")["score"].transform("mean")  # 6 satir (satir sayisi)
```

İkisi de grup ortalamasını hesaplıyor ama sonuçları farklı boyda.

- Rapor üretiyorsan `agg` / `mean`.
- Her satırı kendi grubuyla karşılaştıracaksan `transform`.

`transform` sonucunu doğrudan tabloya sütun olarak ekleyebiliyorsun; `agg`
sonucunu ekleyemiyorsun, boyu tutmuyor.

## 11. Çok seviyeli index'le çalışmak zahmetli

```python
result = data.groupby(["city", "grade"])["score"].mean()
print(result["Ankara"])          # calisir
print(result["Ankara", "A"])     # calisir
print(result.loc["A"])           # calismaz
```

İki anahtarla gruplayınca index iki katmanlı oluyor ve seçim kuralları
değişiyor.

Çoğu zaman düzleştirmek daha kolay:

```python
result.reset_index()     # normal tablo
result.unstack()         # ikinci anahtar sutun olur (pivot gibi)
```

## 12. Grup başına "en iyi satır" bulmak

Yanlış deneme:

```python
data.groupby("city")["score"].max()      # yalnizca sayilar, kim oldugu yok
```

Doğrusu iki adım:

```python
data.loc[data.groupby("city")["score"].idxmax()]
```

`idxmax()` grup başına birer **satır etiketi** veriyor, `loc` de o satırların
tamamını getiriyor — adıyla, şehriyle, notuyla.

**Dikkat:** grup içinde beraberlik varsa `idxmax` ilk satırı alıyor.
