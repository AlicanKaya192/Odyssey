Dersteki deneyi kendin yap: bugünün satışı dünle, geçen haftanın
aynı günüyle ve satırlar karıştırılınca ne kadar ilişkili?

İki diziyi **bir adım kaydırarak** eşleştirmenin yolu dilimleme:

```python
values[:-1]   # sonuncusu haric hepsi: "dun"
values[1:]    # ilki haric hepsi:      "bugun"
```

Aynı sıradaki iki eleman her zaman (dün, bugün) çifti oluyor. Yedi adım için
`values[:-7]` ve `values[7:]`.

**Yapman gerekenler:**

1. `store_sales.csv` dosyasının `sales` sütununu NumPy dizisi olarak al
   (`.to_numpy()`).
2. Bugün-dün korelasyonunu `np.corrcoef(a, b)[0, 1]` ile hesapla.
3. Bugün ile 7 gün önceki korelasyonu hesapla.
4. Tabloyu `sample(frac=1, random_state=42)` ile karıştır, karışık sıradaki
   `sales` dizisinde bugün-dün korelasyonunu hesapla.
5. Üç sayıyı üç ondalığa yuvarlayıp alt alta yazdır.

**Beklenen çıktı:**

```
0.695
0.958
0.018
```

Sayılar aynı sayılar; üçüncüde değişen tek şey sıra. Zaman serisinde bilgi
sıralanışta duruyor.
