Standart kütüphanede bir iş için hangi modüle bakılır? Bu modülde öğrenilenler
ve ilk akla gelmesi gerekenler:

| İş | Modül | Bölüm |
|---|---|---|
| Karekök, logaritma, kombinasyon | `math` | math ve statistics |
| Ortalama, medyan, standart sapma | `statistics` | math ve statistics |
| Rastgele sayı, karıştırma, örneklem | `random` | random |
| Tarih, saat, süre farkı | `datetime` | datetime |
| Süre ölçmek, beklemek | `time` | time ve Zaman Ölçmek |
| Ortam değişkeni, komut satırı argümanları | `os`, `sys` | os ve sys |
| Dosya yolları, klasörde gezinmek | `pathlib` | pathlib |
| Kopyalamak, taşımak, desenle dosya bulmak | `shutil`, `glob` | shutil ve glob |
| Tablo dosyası okumak/yazmak | `csv` | csv |
| JSON | `json` | Python patikası, JSON bölümü |
| Metinde desen aramak | `re` | Düzenli İfadeler |
| Sayaç, kuyruk, varsayılan sözlük | `collections` | collections |
| Kombinasyon, gruplama, zincirleme | `itertools` | itertools |
| Metni sarmak, Unicode | `textwrap`, `string`, `unicodedata` | Metin Araçları |
| zip, gzip, geçici dosya | `zipfile`, `gzip`, `tempfile` | Arşivler ve Geçici Dosyalar |
| Kopya, düzenli yazdırma, sabit adlar | `copy`, `pprint`, `enum` | copy, pprint ve enum |

İleri Python modülünde: `functools`, `typing`, `dataclasses`, `contextlib`,
`logging`, `argparse`, `sqlite3`, `pickle`, `decimal`, `hashlib`,
`concurrent.futures`, `asyncio`, `unittest`, `timeit`.

## Belgeyi okumak

- Etkileşimli kabukta `help(modül)` ya da `help(modül.fonksiyon)`.
- Resmî belge: docs.python.org → Library Reference; her modülün sayfası
  örnekler içerir.
- Bir fonksiyonun hangi sürümde eklendiği belgede "Added in version 3.x"
  diye yazar; eski bir Python'da yoksa sebebi budur.
