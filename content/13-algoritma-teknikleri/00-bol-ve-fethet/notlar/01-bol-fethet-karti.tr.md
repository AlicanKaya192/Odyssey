## İskelet

```python
def solve(problem):
    if KUCUK_MU(problem):            # temel durum: doğrudan çöz
        return DOGRUDAN(problem)
    parts = BOL(problem)
    answers = [solve(p) for p in parts]
    return BIRLESTIR(answers)
```

## Sık görülen şekiller

`T(n)` "boyu `n` olan problemin maliyeti" demek.

| Şekil | Örnek | Maliyet |
|---|---|---|
| `T(n) = T(n/2) + 1` | ikili arama | `O(log n)` |
| `T(n) = T(n/2) + n` | quickselect (ortalama) | `O(n)` |
| `T(n) = 2T(n/2) + 1` | ağacın bütün düğümlerini gezmek | `O(n)` |
| `T(n) = 2T(n/2) + n` | merge sort, en büyük alt dizi | `O(n log n)` |
| `T(n) = 3T(n/2) + n` | Karatsuba | `O(n^1.58)` |
| `T(n) = 4T(n/2) + n` | dört parçalı çarpma | `O(n²)` |
| `T(n) = T(n − 1) + n` | quick sort'un kötü pivotu | `O(n²)` |
| `T(n) = 2T(n − 1) + 1` | Hanoi kuleleri | `O(2ⁿ)` |

Son iki satırın dersi: parçalar **yarıya** değil **birer birer** küçülürse
böl-fethetin kazancı kaybolur.

## Ağaçla hesaplama

1. Kökte ne kadar iş var? (`f(n)`)
2. Her seviyede kaç parça, her parça ne boyda? Seviyenin toplam işi?
3. Kaç seviye var? (yarıya bölünüyorsa `log₂ n`)
4. Seviyeleri topla. Seviyeler eşitse `seviye işi × log n`; aşağı doğru
   küçülüyorsa kökteki iş; büyüyorsa yaprak sayısı.

## Sık hatalar

- Temel durumu unutmak ya da parçayı küçültmemek → sonsuz özyineleme.
- `mid` hesabında kaymak: `lo..mid` ve `mid+1..hi` ikisi de en az bir eleman
  içermeli; `lo..mid-1` ile `mid..hi` iki elemanlıda sonsuz döngü yapabilir.
- Her çağrıda listeyi dilimlemek (`values[:mid]`) kopya üretir; büyük veride
  `lo`, `hi` indeksleriyle çalışmak bellek kazandırır.
- Parçalar örtüşüyorsa (aynı alt problem iki kez) önce önbelleğe bak:
  dinamik programlama.
