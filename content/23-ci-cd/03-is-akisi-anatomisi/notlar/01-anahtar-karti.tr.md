**Üst düzey**

| Anahtar | Ne işe yarar |
|---|---|
| `name` | İş akışının adı |
| `on` | Tetikleyiciler |
| `env` | Bütün işlerde geçerli ortam değişkenleri |
| `jobs` | İşler (her işin anahtarı kendi adı) |

**İş** (`jobs.<ad>`)

| Anahtar | Ne işe yarar |
|---|---|
| `runs-on` | Makine (zorunlu): `ubuntu-latest`, `windows-latest`, `macos-latest` |
| `name` | Ekrandaki ad |
| `env` | Bu işin adımlarında geçerli değişkenler |
| `timeout-minutes` | Süre sınırı |
| `needs` | Önce bitmesi gereken işler (beşinci bölüm) |
| `if` | Koşul (beşinci bölüm) |
| `strategy` | Matris (altıncı bölüm) |
| `steps` | Adımlar (zorunlu) |

**Adım** (`steps` listesinin elemanı)

| Anahtar | Ne işe yarar |
|---|---|
| `name` | Ekrandaki ad |
| `uses` | Hazır eylem, sürümüyle |
| `with` | Eylemin ayarları |
| `run` | Komut; birden çok satır için <code>run: &#124;</code> |
| `env` | Yalnızca bu adımda geçerli değişkenler |
| `working-directory` | Komutun çalışacağı klasör |

**Değişkeni okumak**

- `run` komutunun içinde (bash): `$APP_ENV`
- Komutun dışında, ifade yazımıyla: `${{ env.APP_ENV }}`
- Aynı ad birden çok düzeyde varsa adıma en yakın olan kazanır:
  adım > iş > iş akışı.
