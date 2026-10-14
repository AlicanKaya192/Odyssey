| Kapı | Araç | Hattaki komut | Kapanırsa |
|---|---|---|---|
| Sözdizimi | Python | `python -m py_compile dosya.py` | Kod okunamıyor. |
| Biçim | ruff, black | `ruff format --check .` | Bir dosya biçimsiz. |
| Lint | ruff, flake8, pylint | `ruff check .` | Kural çiğnenmiş (dosya, satır, kural kodu yazar). |
| Tip | mypy | `mypy .` | Tipler tutarsız. |
| Test | pytest | `python -m pytest` | Bir test düştü. |
| Kapsam | coverage.py, pytest-cov | `python -m pytest --cov=paket --cov-fail-under=80` | Kapsam eşiğin altında. |

**Hatırlatmalar**

- Biçimlendirici hatta her zaman `--check` ile çalışır; düzeltmeyi
  geliştirici yapar (`ruff format .`).
- Kapının kararı çıkış kodundan gelir: `0` geçti, başka her sayı kapandı.
- Ucuz kapılar önde: sözdizimi → biçim → lint → test → kapsam.
- Aynı komutları göndermeden önce kendi bilgisayarında da çalıştır.
  Bunu kendiliğinden yapmanın yolu commit'ten önce çalışan kancalar
  (pre-commit).

**Statik analiz ile test**

| | Statik analiz | Test |
|---|---|---|
| Kodu çalıştırır mı? | Hayır, okur | Evet |
| Neyi görür? | Programın bütün yollarını | Yalnızca denenen yolları |
| Neyi göremez? | Çalışırken ne olacağını | Denenmeyen yolları |
| Hız | Saniyeler | Saniyelerden dakikalara |
