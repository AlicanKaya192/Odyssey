## Sonsuz

| Fonksiyon | Örnek | Sonuç |
|---|---|---|
| `count(10, 5)` | `islice(..., 3)` | 10, 15, 20 |
| `cycle("AB")` | `islice(..., 3)` | A, B, A |
| `repeat("x", 3)` | | x, x, x |

## Dilimlemek ve süzmek

| Fonksiyon | Ne yapar |
|---|---|
| `islice(it, n)` / `islice(it, a, b)` | ilk n / a ile b arası |
| `takewhile(koşul, it)` | koşul tuttukça al, ilk bozulmada dur |
| `dropwhile(koşul, it)` | koşul tuttukça atla, sonrası hep |
| `filterfalse(koşul, it)` | koşulu tutmayanlar |
| `compress(it, seçici)` | seçicide doğru olanlar |

## Birleştirmek ve bölmek

| Fonksiyon | Ne yapar |
|---|---|
| `chain(a, b, ...)` | uç uca |
| `chain.from_iterable(listeler)` | liste listesini düzleştirir |
| `zip_longest(a, b, fillvalue=)` | kısa olanı doldurarak eşler |
| `pairwise(x)` | ardışık ikililer |
| `batched(x, n)` | n'erli parçalar |
| `accumulate(x, işlem)` | birikimli sonuç |
| `groupby(x, key=)` | **yan yana** aynı anahtarlılar |
| `tee(it, n)` | bir yineleyiciden n kopya |

## Kombinatorik

| Fonksiyon | `"ABC"`, 2 için adet |
|---|---|
| `product("ABC", repeat=2)` | 9 |
| `permutations("ABC", 2)` | 6 |
| `combinations("ABC", 2)` | 3 |
| `combinations_with_replacement("ABC", 2)` | 6 |

## Hatırla

- Sonuçlar yineleyici: görmek için `list(...)`, bir kez tükenir.
- Sonsuz yineleyiciyi `list(...)` yapma; `islice` ile sınırla.
- `groupby`'dan önce aynı anahtarla `sorted`.
