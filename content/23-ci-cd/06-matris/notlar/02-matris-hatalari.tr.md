| Yazılan | Sonuç | Doğrusu |
|---|---|---|
| `python-version: [3.10, 3.11]` | `3.10` sayı olur, `3.1` istenir | `["3.10", "3.11"]` |
| `runs-on: ubuntu-latest` (matriste `os` varken) | Her iş Linux'ta; `os` boyutu yalnızca adı değiştirir | `runs-on: ${{ matrix.os }}` |
| `setup-python`'a sabit sürüm | Bütün işler aynı Python'la | `python-version: ${{ matrix.python-version }}` |
| `matrix` doğrudan işin altında | Dosya geçersiz: `matrix` işin anahtarı değil | `strategy:` → `matrix:` |
| `include` girdisinde asıl değer başka (`python-version: "3.14"`) | Var olanı değiştirmez, yeni iş açar | Bilerek yaz: yeni iş mi, ek anahtar mı? |
| Her yere `continue-on-error: true` | Hiçbir hata hattı durdurmaz | `${{ matrix.experimental == true }}` |
| Hata yerini görmeden işler iptal | `fail-fast` varsayılan `true` | `fail-fast: false` |

**Hangi işin düştüğünü okumak**

İş adı birleşimi gösterir:

```text
test (ubuntu-latest, 3.12)    ✓
test (ubuntu-latest, 3.13)    ✓
test (windows-latest, 3.13)   ✕
```

Yalnızca Windows düştüyse şüphelenilecekler: dosya yolunda `/` ile `\`,
satır sonları (`\r\n`), büyük-küçük harf (Windows'ta `Data.csv` ile
`data.csv` aynı dosya), kabuk farkı (PowerShell).

Yalnızca yeni Python düştüyse: kaldırılmış ya da değişmiş bir özellik,
henüz o sürüme çıkmamış bir bağımlılık.
