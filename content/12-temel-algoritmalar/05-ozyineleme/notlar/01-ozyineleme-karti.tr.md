## Kalıp

```text
def solve(problem):
    if problem en küçük hâlindeyse:        # temel durum
        return doğrudan cevap
    smaller = problemi bir adım küçült
    answer_small = solve(smaller)          # kendini çağır
    return answer_small'dan büyüğün cevabını kur
```

## Kontrol listesi

1. **Temel durum var mı?** Boş liste, `n <= 1`, boş metin…
2. **Her çağrı temel duruma yaklaşıyor mu?** `n - 1`, `items[1:]`,
   `text[1:]`. `solve(n)` içinden `solve(n)` çağırmak sonsuz döngüdür.
3. **Özyinelemeli çağrının sonucu kullanılıyor mu?** En sık hata:

   ```python
   def total(items):
       if not items:
           return 0
       items[0] + total(items[1:])     # return unutuldu → None döner
   ```

4. **Bütün yollar `return` ile bitiyor mu?** Bir `if` dalında `return`
   unutmak fonksiyonun o dalda `None` döndürmesine yol açar.

## Sık kalıplar

| Problem | Temel durum | Adım |
|---|---|---|
| `n!` | `n <= 1` → 1 | `n * f(n - 1)` |
| Liste toplamı | boş → 0 | `items[0] + f(items[1:])` |
| Metni ters çevirmek | boş → `""` | `f(text[1:]) + text[0]` |
| Rakam toplamı | `n < 10` → `n` | `n % 10 + f(n // 10)` |
| Üs alma | `exp == 0` → 1 | `base * f(base, exp - 1)` |
| İç içe liste | eleman liste değil → kendisi | her alt liste için `f(alt)` |

## Değiştirilebilir varsayılan değer tuzağı

Özyinelemede biriktirme listesi taşırken **varsayılan değeri liste yapma**:

```python
def collect(items, result=[]):     # yanlış: aynı liste bütün çağrılarda paylaşılır
    ...

def collect(items, result=None):   # doğru
    if result is None:
        result = []
    ...
```

Varsayılan değer fonksiyon tanımlanırken **bir kez** kurulur; ikinci kez
çağırınca birinci çağrının sonuçları hâlâ listede durur.
