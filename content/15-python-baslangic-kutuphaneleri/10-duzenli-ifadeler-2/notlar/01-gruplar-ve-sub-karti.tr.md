## Gruplar

| Yazım | Anlamı |
|---|---|
| `(...)` | yakalayan grup |
| `(?P<ad>...)` | adlı grup |
| `(?:...)` | yakalamayan grup (yalnızca sınır) |
| `m.group(1)`, `m.group("ad")`, `m["ad"]` | bir grup |
| `m.groups()` | bütün gruplar, demet |
| `m.groupdict()` | adlı gruplar, sözlük |

## Kalıp öğeleri

| Yazım | Anlamı |
|---|---|
| <code>a&#124;b</code> | a ya da b |
| `+?`, `*?`, `??` | tembel (olabildiğince az) |
| `\1` (kalıp içinde) | 1. grubun aynısı tekrar: `(\w)\1` → `ll`, `ss` |

## Fonksiyonlar

| Yazım | Ne yapar |
|---|---|
| `re.findall(k, m)` | grup yoksa eşleşmeler, varsa grup demetleri |
| `re.finditer(k, m)` | eşleşme nesneleri, sırayla |
| `re.sub(k, yeni, m)` | değiştirir; yeni metinde `\1`, `\g<ad>` |
| `re.sub(k, fonksiyon, m)` | her eşleşme için fonksiyonun döndürdüğü |
| `re.sub(..., count=n)` | yalnızca ilk n |
| `re.subn(k, yeni, m)` | `(yeni metin, değişen sayısı)` |
| `re.split(k, m)` | kalıba göre böler |
| `re.compile(k, bayraklar)` | derlenmiş kalıp |

## Bayraklar

| Bayrak | Etkisi |
|---|---|
| `re.IGNORECASE` (`re.I`) | büyük/küçük harf fark etmez |
| `re.MULTILINE` (`re.M`) | `^ $` her satırın başı/sonu |
| `re.DOTALL` (`re.S`) | `.` satır sonuyla da eşleşir |
| `re.VERBOSE` (`re.X`) | kalıpta boşluk ve yorum serbest |

Birleştirmek: `re.I | re.M`.
