**Kırmızı bir çalışmada sıra**

1. Hangi iş, hangi adım düştü?
2. Günlükte **ilk** hata satırı (sondaki "exit code 1" sonuç, neden değil).
3. Yerelde aynı sürümlerle, aynı komutla tekrar et.
4. Tekrar etmiyorsa farklara bak (aşağıdaki tablo).
5. Hâlâ bulunamıyorsa ayrıntılı günlük: `ACTIONS_STEP_DEBUG` = `true`,
   çalışmayı "debug logging" ile yeniden başlat.

**Hattı hata ayıklamaya hazırlamak**

```yaml
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - run: python -m pip install -r requirements.txt
      - run: python -m pytest -q --junitxml=report.xml
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: test-report
          path: report.xml
```

| Parça | Ne kazandırır |
|---|---|
| `timeout-minutes` | Asılı test işi saatlerce beklemez (varsayılan 360) |
| `--junitxml` | Makinenin okuyabileceği test raporu |
| `if: failure()` + artifact | Rapor yalnızca düşünce saklanır |

**"Bende çalışıyor" farkları**

| Fark | Belirti |
|---|---|
| Linux'ta dosya adında büyük-küçük harf | `FileNotFoundError: data.csv` |
| UTC saat | Tarih testleri gece yarısına yakın düşüyor |
| Sabitlenmemiş paket | Dün geçen test bugün düşüyor, kod değişmeden |
| Elle oluşturulmuş dosya | Hatta `FileNotFoundError` |
| Satır sonu (`\r\n` / `\n`) | Metin karşılaştırması düşüyor |

**Karantina**

```yaml
  quarantine:
    runs-on: ubuntu-latest
    continue-on-error: true
    steps:
      - uses: actions/checkout@v4
      - run: python -m pip install -r requirements.txt
      - run: python -m pytest -q -m flaky
```

- Ana iş `-m "not flaky"` ile, karantina `-m flaky` ile.
- İşaret `pyproject.toml`'da: `markers = ["flaky: known flaky tests"]`.
- Her karantinadaki testin sahibi ve son tarihi olur.
- Yeniden çalıştırma düğmesi düzeltme değildir.
