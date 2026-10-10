Bu modül bir programı **büyütmek** için gereken standart araçları gösterdi.
Bundan sonrası iki yöne açılıyor: veri bilimi kütüphaneleri ve gerçek
projelerde kullanılan ek araçlar.

## Veri Bilimi ve ML Kütüphaneleri

Bu patikanın sonraki iki modülü standart kütüphanenin dışına çıkıyor:
NumPy, pandas, Matplotlib, seaborn, SciPy; sonra scikit-learn ve model
kütüphaneleri. Burada öğrendiklerin orada da işine yarayacak:

- **Tipler ve dataclass'lar** model ayarlarını ve deney kayıtlarını açık
  tutar.
- **logging** uzun eğitimlerde ne olduğunu kaydeder.
- **argparse** deney betiklerini komut satırından ayarlanabilir yapar.
- **pickle** eğitilmiş modelleri saklamanın en yaygın yoludur (ve aynı
  güvenlik kuralı geçerlidir: güvenmediğin model dosyasını yükleme).
- **concurrent.futures** ve **cProfile** büyük veri işlerini hızlandırmak ve
  ölçmek için.
- **tracemalloc** büyük tabloların belleğini izlemek için (pandas'ın Arrow
  sütunları dışında).

## Gerçek projelerde sık kullanılan ek araçlar

Bunlar ayrı paketler; bilmeye değer:

| Araç | Ne için |
|---|---|
| `pytest` | daha kısa testler (API Yazmak modülünde var) |
| `mypy`, `pyright` | tip belirtimlerini çalıştırmadan denetlemek |
| `ruff`, `black` | biçim ve stil denetimi, otomatik düzeltme |
| `httpx`, `aiohttp` | async HTTP istemcisi |
| `SQLAlchemy` | veritabanı katmanı, birden çok veritabanı |
| `cryptography` | şifreleme (gizleyip geri açmak) |
| `click`, `typer` | argparse'tan kısa komut satırı araçları |

## Kendi başına keşfetmek

- "The Python Standard Library" belgesi bu modüldeki her modülün ayrıntısını
  ve daha fazlasını (`enum`, `struct`, `ipaddress`, `zoneinfo`...) içerir.
- Bir kütüphanenin kaynak koduna bakmak da öğretir: `import inspect;
  print(inspect.getsource(functools.wraps))`.
- Kendi küçük aracını yaz: argparse + logging + sqlite3 + unittest ile bir
  not defteri, bir harcama takipçisi; bu modülün hepsi bir arada.
