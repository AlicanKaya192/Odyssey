## package başlığı

| Alan | Örnek | Not |
|---|---|---|
| `name` | `"todo-cli"` | Küçük harf ve tire yaygın |
| `version` | `"1.2.3"` | Büyük, orta, küçük parça |
| `edition` | `"2024"` | Yazılmazsa en eski kurallar (2015) geçerli olur |
| `description` | `"Short text"` | Paket yayınlarken gerekir |
| `license` | `"MIT"` | Paket yayınlarken gerekir |
| `rust-version` | `"1.85"` | En düşük desteklenen derleyici |

## Sürüm numarası nasıl yazılır?

Bağımlılıklarda yazdığın sürüm bir aralıktır, tek sürüm değildir:

| Yazım | Kabul edilen |
|---|---|
| `"1.2.3"` | 1.2.3 ve üstü, 2.0.0'dan küçük |
| `"1.2"` | 1.2.0 ve üstü, 2.0.0'dan küçük |
| `"1"` | 1.0.0 ve üstü, 2.0.0'dan küçük |
| `"=1.2.3"` | Yalnızca 1.2.3 |

Kural **anlamsal sürümleme** (semver): büyük numara değişmedikçe eski kod çalışmaya devam etmeli.

## Baskıyı yazmayı unutursan

`edition` yazılmazsa Cargo uyarır ve en eski baskıyı kullanır. O zaman `async` gibi kelimeler
tanınmaz ve garip hatalar görürsün. Bu bölümün alıştırmalarından biri tam olarak bunu gösteriyor.

## Cargo'nun derleme anında verdiği değerler

`env!` ile okunabilir:

| Ad | Değer |
|---|---|
| `CARGO_PKG_NAME` | `name` |
| `CARGO_PKG_VERSION` | `version` |
| `CARGO_PKG_DESCRIPTION` | `description` |
