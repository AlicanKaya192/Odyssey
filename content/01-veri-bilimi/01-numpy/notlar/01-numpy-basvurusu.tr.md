# NumPy Başvurusu

Alıştırmalarda takıldığında bakabileceğin liste. Hepsi `import numpy as np`
yapıldığını varsayıyor.

## Dizi oluşturma

| Yazım | Ne yapar |
|---|---|
| `np.array([1, 2, 3])` | Listeden dizi üretir |
| `np.array([[1, 2], [3, 4]])` | İki boyutlu dizi |
| `np.zeros(5)` | Beş sıfır (ondalık) |
| `np.zeros(5, dtype=int)` | Beş sıfır (tamsayı) |
| `np.ones(3)` | Üç tane bir |
| `np.full(4, 7)` | Dört tane yedi |
| `np.arange(0, 10, 2)` | 0'dan 10'a **ikişer**: `[0 2 4 6 8]` |
| `np.linspace(0, 1, 5)` | 0 ile 1 arası **beş** sayı, uçlar dâhil |
| `np.eye(3)` | Birim matris |

`arange` bitişi dışarıda bırakıyor, `linspace` içeri alıyor. En sık
karıştırılan ikili bu.

## Özellikler

| Yazım | Ne verir |
|---|---|
| `a.ndim` | Boyut sayısı |
| `a.shape` | `(satır, sütun)` demeti |
| `a.size` | Toplam eleman sayısı |
| `a.dtype` | Eleman tipi |
| `len(a)` | **İlk boyuttaki** eleman sayısı — iki boyutta satır sayısı |

`a.shape` bir demet: `a.shape[0]` satır, `a.shape[1]` sütun sayısı.

## Şekil değiştirme

| Yazım | Ne yapar |
|---|---|
| `a.reshape(2, 3)` | Aynı veriyi 2x3 olarak gösterir |
| `a.reshape(-1)` | Düzleştirir; `-1` "gerisini sen hesapla" demek |
| `a.reshape(3, -1)` | Üç satır, sütun sayısı hesaplansın |
| `a.T` | Devrik: satırlar sütun olur |
| `a.flatten()` | Düzleştirir ve **kopya** verir |
| `a.ravel()` | Düzleştirir, mümkünse **kopya vermez** |

Eleman sayısı tutmak zorunda; tutmuyorsa `ValueError`.

## Seçim

| Yazım | Ne seçer |
|---|---|
| `a[0]` | İlk eleman (iki boyutta ilk satır) |
| `a[-1]` | Son eleman |
| `a[1:4]` | 1'den 4'e (4 dâhil değil) |
| `a[::2]` | Bir atlayarak |
| `a[::-1]` | Tersten |
| `a[1, 2]` | İkinci satır, üçüncü sütun |
| `a[:, 0]` | Bütün satırların ilk sütunu |
| `a[0, :]` | İlk satırın tamamı |
| `a[[0, 3]]` | Fancy index: 0. ve 3. eleman |
| `a[a > 5]` | Koşullu seçim |

**Dilim kopya değil, kopya için `.copy()`.** Fancy index ve koşullu seçim
zaten kopya veriyor.

## Koşullar

| Yazım | Ne yapar |
|---|---|
| `a > 5` | `True`/`False` dizisi |
| `a[a > 5]` | Koşula uyan elemanlar |
| `(a > 5) & (a < 10)` | İki koşul birlikte — **parantez zorunlu** |
| `(a < 2) \| (a > 8)` | Ya biri ya öbürü |
| `~(a > 5)` | Tersi |
| `np.where(a > 5, 1, 0)` | Uyanlara 1, uymayanlara 0 yaz |
| `(a > 5).sum()` | Kaç tanesi uyuyor (`True` = 1) |
| `(a > 5).any()` | En az biri uyuyor mu |
| `(a > 5).all()` | Hepsi uyuyor mu |

`and` / `or` / `not` **çalışmıyor**; dizide tek bir doğruluk değeri yok.

## Matematik

| Yazım | Ne yapar |
|---|---|
| `a + 10` | Her elemana 10 ekler |
| `a * b` | Eleman eleman çarpar |
| `a ** 2` | Her elemanın karesi |
| `a @ b` | Matris çarpımı (eleman eleman değil) |
| `np.sqrt(a)` | Karekök |
| `np.round(a, 2)` | Virgülden sonra iki basamak |
| `np.abs(a)` | Mutlak değer |

## Toplulaştırma

| Yazım | Ne verir |
|---|---|
| `a.sum()` | Toplam |
| `a.mean()` | Ortalama |
| `a.std()` | Standart sapma |
| `a.min()` / `a.max()` | En küçük / en büyük |
| `a.argmin()` / `a.argmax()` | En küçüğün / en büyüğün **sırası** |
| `np.median(a)` | Medyan |
| `np.unique(a)` | Tekrarsız değerler, sıralı |
| `np.sort(a)` | Sıralanmış **kopya** |
| `a.cumsum()` | Yürüyen toplam |

`arg` ile başlayanlar değeri değil **indeksi** veriyor.

## axis

| Yazım | Sonuç |
|---|---|
| `a.sum()` | Tek sayı |
| `a.sum(axis=0)` | Her **sütun** için bir sayı |
| `a.sum(axis=1)` | Her **satır** için bir sayı |

Hatırlama yolu: `axis` "hangi boyut kaybolacak" demek. `axis=0` satırları
yok ediyor, geriye sütun başına birer sonuç kalıyor.

Tabloda satır = kayıt olduğu için `axis=0` genelde "her özelliğin
ortalaması" demek.

## Eksik değerler

| Yazım | Ne yapar |
|---|---|
| `np.nan` | Eksik değer |
| `np.isnan(a)` | Hangi hücreler boş |
| `a[~np.isnan(a)]` | Boş olmayanlar |
| `np.nanmean(a)` | Boşları atlayarak ortalama |
| `np.nansum(a)` | Boşları atlayarak toplam |
| `np.isnan(a).sum()` | Kaç tane boş var |

`np.nan` her zaman ondalık; içinde `nan` olan bir dizi `int` olamıyor.

## Rastgele sayı

| Yazım | Ne yapar |
|---|---|
| `np.random.seed(42)` | Sonucu tekrarlanabilir yapar |
| `np.random.randint(0, 10, size=5)` | 0-9 arası beş tamsayı |
| `np.random.random(5)` | 0-1 arası beş ondalık |
| `np.random.normal(10, 2, 5)` | Ortalaması 10, sapması 2 olan beş sayı |

`seed` çağırmazsan her çalıştırmada başka sonuç geliyor. Alıştırma
çözerken beklenen çıktı varsa `seed` şart.
