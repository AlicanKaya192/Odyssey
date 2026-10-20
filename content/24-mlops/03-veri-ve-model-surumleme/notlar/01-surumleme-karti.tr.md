Büyük dosyaları sürümlemenin düzeni:

| Nerede | Ne durur | Neden |
|---|---|---|
| Git | Kod, işaret dosyaları (`.ptr`, `.dvc`), `.gitignore` | Küçük metin; her commit "bu kod, bu veri" der |
| Depo (store) | Veri ve model dosyalarının kendisi | Büyük ve ikili; geçmişi Git'i şişirmesin |
| `.gitignore` | Büyük dosyaların adları | Yanlışlıkla Git'e girmesinler |

## İşaret dosyası

```text
{
  "path": "customers_v1.csv",
  "sha256": "<64 karakterlik özet>",
  "size": 131847
}
```

- `path`: dosya geri getirilince nereye yazılacak.
- `sha256`: depodaki yeri ve bütünlük denetimi.
- `size`: hızlı ilk denetim; boy tutmuyorsa özeti hesaplamaya gerek yok.

## Depodaki yol

Özet `2448b8...` ise dosya `store/24/48b8...` yolundadır: ilk iki
karakter klasör, gerisi ad. Aynı içerik her zaman aynı yola düşer, bu
yüzden ikinci kez kopyalanmaz.

## İşlemler

| İşlem | Ne yapar |
|---|---|
| `put(path)` | Özeti hesapla, dosyayı depoya kopyala (yoksa), işaret dosyası yaz |
| `get(pointer)` | Depodan oku, özeti yeniden hesapla, tutuyorsa dosyayı yaz |
| Fark | Kimlik sütunuyla eklenen, silinen, değişen satırları say |

## Gerçek araçlarda karşılıkları

| Bu bölümde | DVC | Git LFS |
|---|---|---|
| `put("data.csv")` | `dvc add data.csv` | `git lfs track "*.csv"` + `git add` |
| `.ptr` dosyası | `.dvc` dosyası | Git'teki işaret metni |
| Depo klasörü | `.dvc/cache` + uzak depo (`dvc push`) | LFS sunucusu |
| `get(...)` | `dvc pull`, `dvc checkout` | `git lfs pull` |

## Terimler

- **Sürümleme** (versioning): bir şeyin her hâlini saklayıp adıyla geri
  getirebilmek.
- **İçerik adresli depolama** (content-addressed storage): dosyayı
  içeriğinin özetiyle adlandırıp saklamak.
- **İşaret dosyası** (pointer file): büyük dosyanın yolunu, özetini ve
  boyunu tutan küçük metin.
- **İkili dosya** (binary file): metin olmayan dosya; model dosyası gibi.
