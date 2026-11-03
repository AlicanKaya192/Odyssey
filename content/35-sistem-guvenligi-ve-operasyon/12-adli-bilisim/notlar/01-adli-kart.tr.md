## Temel ilkeler

| İlke | Anlamı |
|---|---|
| Bütünlük | Kanıtın özeti toplandığı an kaydedilir, her adımda doğrulanabilir |
| Kopya üzerinde çalış | Asıl kanıta dokunulmaz; yazma engelleyiciyle okunur |
| Gözetim zinciri | Her el değiştirme: kim verdi, kim aldı, ne zaman, neden |
| Uçuculuk sırası | Önce bellek ve bağlantılar, sonra disk, sonra yedekler |
| Tekrarlanabilirlik | Başka bir uzman aynı adımlarla aynı sonuca varabilmeli |
| Belgelemek | Her adım, araç ve sürümüyle kayda geçer |

## Uçuculuk sırası

| Sıra | Kaynak |
|---|---|
| 1 | Bellek (RAM) |
| 2 | Ağ bağlantıları, çalışan süreçler |
| 3 | Geçici dosyalar |
| 4 | Disk |
| 5 | Yedekler, arşivler |

## Bazı dosya imzaları

| Tür | İlk baytlar (onaltılık) | Metin hâli |
|---|---|---|
| PDF | `25 50 44 46` | `%PDF` |
| PNG | `89 50 4E 47` | `.PNG` |
| ZIP (ve docx, xlsx) | `50 4B 03 04` | `PK..` |

## Python kalıpları

- Kanıt özeti: `hashlib.sha256(veri).hexdigest()`.
- İmza: `veri.startswith(imza)`; onaltılık metinden bayta `bytes.fromhex("89504e47")`.
- Uzantı: `ad.rsplit(".", 1)[1]`.
- Zinciri denetlemek: her teslimde `veren == onceki_alan`.

## Akılda tutulacak

- Kanıt değişmediği kanıtlanabiliyorsa değerlidir.
- Uzantı kolayca değişir; dosyanın türünü ilk baytlar söyler.
- Dosya zamanları değiştirilebilir; tek başına kesin kanıt değildir.
- Raporda bulunmayan da yazılır; tahmin kanıt gibi anlatılmaz.
