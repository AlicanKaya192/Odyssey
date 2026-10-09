Bu modül standart kütüphanenin **gündelik** yüzünü gösterdi: sayılar,
tarihler, dosyalar, metin, veri yapıları. Büyüyen projelerde başka ihtiyaçlar
çıkar ve onların da çoğu standart kütüphanede.

## Python Kütüphaneleri: İleri

Bir sonraki modül daha büyük programların araçlarını anlatıyor:

- **Fonksiyonlarla çalışmak:** `functools` (`lru_cache`, `partial`),
  `operator`, sıralama anahtarları.
- **Kodu açık yazmak:** `typing` ile tip belirtimleri, `dataclasses` ile
  kayıt sınıfları, `abc` ve protokoller.
- **Kaynakları yönetmek:** `contextlib` ile kendi `with` bloklarını yazmak.
- **Gerçek programlar:** `logging` (print yerine kayıt), `argparse` (komut
  satırı aracı), `sqlite3` (dosyada veritabanı), `pickle` ve serileştirme.
- **Doğru hesap ve güvenlik:** `decimal` (para), `fractions`, `hashlib`
  (özet), `secrets` (güvenli rastgele).
- **Hız:** `threading`, `concurrent.futures`, `asyncio`; `timeit` ve
  `cProfile` ile ölçmek.
- **Sağlam kod:** `unittest`, `doctest`; bellek sızıntısı ve nasıl önlendiği.

## Veri bilimi tarafı

Bu patikanın üçüncü ve dördüncü modülleri standart kütüphanenin dışına
çıkıyor: NumPy, pandas, Matplotlib, seaborn, SciPy, sonra scikit-learn ve
model kütüphaneleri. Burada öğrendiklerin orada da geçerli: pandas tarihleri
`datetime` gibi biçimlendirir, sütunlarda `.str` ile regex kullanır, dosya
yollarını `Path` olarak alır.

## Kendi başına keşfetmek

- Bir modülün bütün fonksiyonları: `dir(modül)`, açıklama `help(modül.ad)`.
- Python'un resmî belgesinde "The Python Standard Library" sayfası modülleri
  konularına göre listeler; her modül sayfasında örnekler var.
- Bir iş için önce "standart kütüphanede var mı?" diye sor: varsa kurulum
  yok, sürüm sorunu yok, her bilgisayarda aynı.
