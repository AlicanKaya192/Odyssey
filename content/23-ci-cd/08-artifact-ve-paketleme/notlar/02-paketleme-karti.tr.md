**En küçük `pyproject.toml`**

```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "greeter"
version = "0.1.0"
```

**Komutlar**

| Komut | Ne yapar |
|---|---|
| `python -m pip install build` | Derleme aracını kurar |
| `python -m build` | `dist/` içine tekerlek (`.whl`) ve kaynak paketi (`.tar.gz`) |
| `pip wheel . --no-deps -w dist` | Yalnızca tekerlek (pip'in kendisiyle) |
| `pip install dist/*.whl` | Tekerleği kurar |
| `pip install --target klasör paket.whl` | Belirli bir klasöre kurar |

**Tekerleğin adı**

```text
greeter-0.1.0-py3-none-any.whl
│       │     │   │    └ platform: her işletim sistemi
│       │     │   └ ABI: Python'un iç yapısına bağlı değil
│       │     └ Python: her Python 3
│       └ sürüm
└ ad
```

C eklentisi olan paketlerde son üç parça değişir (ör.
`cp313-cp313-win_amd64`): her Python sürümü ve işletim sistemi için ayrı
tekerlek derlenir; matris burada da işe yarar.

**İçi**

| Dosya | İçinde |
|---|---|
| `greeter/...` | Kodun kendisi |
| `greeter-0.1.0.dist-info/METADATA` | Ad, sürüm, bağımlılıklar |
| `greeter-0.1.0.dist-info/RECORD` | Her dosyanın özeti |
| `greeter-0.1.0.dist-info/WHEEL` | Tekerleğin biçim bilgisi |

**Duman testi neyi yakalar?**

- Pakete girmemiş bir dosya (veri dosyası, alt paket).
- Yalnızca proje klasöründen çalışınca bulunan bir içe aktarma.
- `pyproject.toml`'a yazılmamış bir bağımlılık.
