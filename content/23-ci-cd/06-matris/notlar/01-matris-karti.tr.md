**Yerleşim**

```yaml
  test:
    runs-on: ${{ matrix.os }}
    continue-on-error: ${{ matrix.experimental == true }}
    strategy:
      fail-fast: false
      max-parallel: 4
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ["3.12", "3.13"]
        exclude:
          - os: windows-latest
            python-version: "3.12"
        include:
          - os: ubuntu-latest
            python-version: "3.14"
            experimental: true
```

`strategy` işin altında (`runs-on` ile aynı hizada), `matrix`
`strategy`'nin altında, `exclude` ve `include` `matrix`'in altında.

**Anahtarlar**

| Anahtar | Anlamı |
|---|---|
| `matrix.<boyut>` | Değer listesi; iş sayısı uzunlukların çarpımı |
| `exclude` | Uyan birleşimleri çıkarır (önce uygulanır) |
| `include` | Uyan birleşime anahtar ekler; uymayan yeni iş olur |
| `fail-fast` | Varsayılan `true`: biri düşünce öbürleri iptal |
| `max-parallel` | Aynı anda en fazla kaç iş |

**Değeri okumak**

- `${{ matrix.os }}`, `${{ matrix.python-version }}`
- `include` ile yalnızca bazı işlere eklenen anahtar öbür işlerde boş.

**Sayılar**

| Matris | İş |
|---|---|
| 2 işletim sistemi × 2 sürüm | 4 |
| 3 × 4 | 12 |
| 3 × 4 × 2 (iki bağımlılık sürümü) | 24 |
| Bir matristen en fazla | 256 |

**Sık kurulum**

- Bütün Python sürümleri Linux'ta.
- Windows ve macOS yalnızca en yeni sürümle (`include` ile).
- Çıkmamış sürüm `experimental: true` + `continue-on-error`.
