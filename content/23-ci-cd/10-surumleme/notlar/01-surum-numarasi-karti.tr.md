**Anlamlı sürümleme: `ANA.YAN.YAMA`**

| Değişiklik | Artan | Örnek (`1.9.3`'ten) |
|---|---|---|
| Eskiyle uyumsuz | ANA | `2.0.0` |
| Geriye uyumlu yeni özellik | YAN | `1.10.0` |
| Yalnızca hata düzeltmesi | YAMA | `1.9.4` |

- Artan parçanın sağındakiler sıfırlanır.
- `0.x`: henüz kararlı değil.

**Commit önekleri (Conventional Commits)**

| Önek | Sürüm |
|---|---|
| `fix:` | YAMA |
| `feat:` | YAN |
| `feat!:`, `fix!:` ya da metinde `BREAKING CHANGE` | ANA |
| `docs:`, `test:`, `ci:`, `refactor:` | Yeni sürüm yok |

Son yayından bu yana gelen commit'lerin **en büyüğü** kazanır.

**Sıralama**

```python
# Yanlış: metin olarak
sorted(["1.9.0", "1.10.0"])            # ['1.10.0', '1.9.0']

# Doğru: sayı demeti
def as_tuple(version):
    return tuple(int(part) for part in version.split("."))

sorted(["1.9.0", "1.10.0"], key=as_tuple)   # ['1.9.0', '1.10.0']
```

```python
# Python paketleri (PEP 440): ekleri de bilen sıralama
from packaging.version import Version

sorted(["1.2.0", "1.2.0rc1", "1.2.0b2"], key=Version)
# ['1.2.0b2', '1.2.0rc1', '1.2.0']
```

**PEP 440 ekleri**

| Yazım | Anlamı | Sırası |
|---|---|---|
| `1.2.0b2` | Beta | `1.2.0`'dan önce |
| `1.2.0rc1` | Sürüm adayı | Betadan sonra, `1.2.0`'dan önce |
| `1.2.0` | Sürüm | |
| `1.2.0.post1` | Yayından sonraki küçük düzeltme | `1.2.0`'dan sonra |

pip aday ve beta sürümleri yalnızca `--pre` ile kurar.
