"""Öğrencinin yazdığı T-SQL'i gerçek bir MSSQL sunucusunda çalıştırır.

`harness.py` gibi bu dosya da **tek başına ayakta durur**: uygulamanın
hiçbir modülünü import etmez, çünkü ayrı bir süreçte çalışıyor.

Neden SQLite değil de gerçek MSSQL: kurumlarda kullanılan T-SQL'in kendine
özgü bir söz dizimi var (`TOP`, `IDENTITY`, `NVARCHAR`, `STRING_AGG`,
`OVER`). Ölçüldü — bunların yarısı SQLite'ta yok. Öğrenci `SELECT TOP 10`
yazıp "çalışmadı" görseydi yanlış bir şey öğrenirdi.

**Sıfırlama işlem geri almayla yapılıyor.** Öğrencinin SQL'i bir işlemin
içinde çalışıyor ve sonuç ne olursa olsun geri alınıyor. MSSQL'de DDL de
işleme dahil: `DROP TABLE` yazan bir öğrenciden sonra bile veritabanı el
değmemiş kalıyor (ölçüldü: 7 ms, sıfırdan kurmak 3.1 saniye).

Kullanım (harness üzerinden):
    sonuc = run(job)   # job içinde language == "tsql"
"""

from __future__ import annotations

import datetime
import decimal
import hashlib
import re
from pathlib import Path

# Bağlantı denemesi bu kadar bekliyor. Sunucu kapalıysa uzun beklemenin
# anlamı yok; kullanıcıya "kurulu değil" demek daha hızlı.
CONNECT_TIMEOUT_SEC = 5

# Denenecek sürücüler: yenisi önce. 18, 17'de olmayan bazı ayarları
# istiyor (`TrustServerCertificate`), o yüzden dizeleri ayrı.
DRIVERS = ("ODBC Driver 18 for SQL Server", "ODBC Driver 17 for SQL Server")

# Denenecek sunucu adları. Sıra önemli: Express en yaygın kurulum, LocalDB
# ise Visual Studio ile gelen sessiz kurulum.
SERVERS = (r".\SQLEXPRESS", r"(localdb)\MSSQLLocalDB", ".", "localhost")

# Alıştırma veritabanlarının ön eki. Kullanıcının kendi veritabanlarıyla
# karışmasın diye ayırt edici.
DB_PREFIX = "Odyssey_"

# Tohumun sürümünü saklayan tablo. İçerik güncellenince tohum değişiyor;
# veritabanı bu yüzden yeniden kuruluyor.
SEED_TABLE = "__odyssey_seed"

# Kayan noktalı karşılaştırmada kabul edilen fark. `AVG` gibi işlemler
# `85000.000000` üretiyor; yazarın beklenen değeri `85000.0` yazması
# yeterli olmalı.
FLOAT_TOLERANCE = 1e-6

# Toplu iş ayıracı. `GO` T-SQL'in değil SSMS'in komutu ama öğrenci
# alışkanlıkla yazıyor; sunucuya gönderilirse sözdizimi hatası veriyor.
BATCH_SEPARATOR = re.compile(r"^\s*GO\s*;?\s*$", re.IGNORECASE | re.MULTILINE)


class SqlUnavailable(Exception):
    """Sunucuya ulaşılamadı.

    `reason` arayüzün hangi mesajı göstereceğini seçiyor: sürücü mü yok,
    sunucu mu kapalı.
    """

    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(reason)
        self.reason = reason
        self.detail = detail


# --- bağlantı ---------------------------------------------------------


def _connection_string(driver: str, server: str, database: str) -> str:
    parts = [
        f"DRIVER={{{driver}}}",
        f"SERVER={server}",
        f"DATABASE={database}",
        "Trusted_Connection=yes",
    ]
    if "18" in driver:
        # 18'den itibaren şifreleme varsayılan olarak açık ve yerel
        # kurulumların sertifikası kendinden imzalı; bu ayar olmadan
        # bağlantı sertifika hatasıyla düşüyor.
        parts.append("TrustServerCertificate=yes")
    return ";".join(parts) + ";"


def find_server(hint: str = "") -> tuple[str, str]:
    """Çalışan bir sunucu bulur; `(sürücü, sunucu)` döndürür.

    `hint` daha önce bulunmuş bir sunucu adı: önce o deneniyor, böylece
    her çalıştırmada bütün adaylar taranmıyor.
    """
    try:
        import pyodbc
    except ImportError as exc:  # pragma: no cover - ortama bağlı
        raise SqlUnavailable("driver_missing", str(exc)) from exc

    kurulu = {d for d in pyodbc.drivers()}
    surucular = [d for d in DRIVERS if d in kurulu]
    if not surucular:
        raise SqlUnavailable("driver_missing", ", ".join(sorted(kurulu)))

    sunucular = ([hint] if hint else []) + [s for s in SERVERS if s != hint]
    son_hata = ""
    for sunucu in sunucular:
        for surucu in surucular:
            try:
                baglanti = pyodbc.connect(
                    _connection_string(surucu, sunucu, "master"),
                    timeout=CONNECT_TIMEOUT_SEC,
                    autocommit=True,
                )
            except Exception as exc:  # pyodbc.Error ve altları
                son_hata = str(exc)
                continue
            baglanti.close()
            return surucu, sunucu
    raise SqlUnavailable("server_missing", son_hata[:300])


def _connect(driver: str, server: str, database: str, *, autocommit: bool):
    import pyodbc

    return pyodbc.connect(
        _connection_string(driver, server, database),
        timeout=CONNECT_TIMEOUT_SEC,
        autocommit=autocommit,
    )


# --- veritabanı kurulumu ---------------------------------------------


def database_name(key: str) -> str:
    """Alıştırma kimliğinden geçerli bir veritabanı adı üretir.

    Kimlikler tire içeriyor (`first-select`) ve köşeli parantezsiz
    kullanılamıyor; ayrıca iki farklı bölümde aynı adlı alıştırma
    olabiliyor. Kısa bir özet ikisini de çözüyor.
    """
    temiz = re.sub(r"[^A-Za-z0-9]", "_", key)[:40]
    ozet = hashlib.sha1(key.encode("utf-8")).hexdigest()[:8]
    return f"{DB_PREFIX}{temiz}_{ozet}"


def _split_batches(sql: str) -> list[str]:
    """`GO` ayıracına göre böler; boş parçaları atar."""
    return [p.strip() for p in BATCH_SEPARATOR.split(sql) if p.strip()]


def ensure_database(driver: str, server: str, name: str, seed_sql: str) -> None:
    """Veritabanı yoksa kurar, tohum değiştiyse yeniden kurar.

    Tohumun özeti veritabanının içinde saklanıyor. İçerik güncellenip
    tohum değiştiğinde eski veritabanı düşürülüp yenisi kuruluyor;
    aynıysa hiçbir şey yapılmıyor (ölçüldü: kurulum 3.1 sn, kontrol 5 ms).
    """
    ozet = hashlib.sha256(seed_sql.encode("utf-8")).hexdigest()

    ana = _connect(driver, server, "master", autocommit=True)
    try:
        imlec = ana.cursor()
        imlec.execute("SELECT DB_ID(?)", name)
        varsa = imlec.fetchone()[0] is not None

        if varsa:
            try:
                vt = _connect(driver, server, name, autocommit=True)
                try:
                    c = vt.cursor()
                    c.execute(
                        f"SELECT ozet FROM dbo.{SEED_TABLE}"
                    )
                    satir = c.fetchone()
                    if satir and satir[0] == ozet:
                        return  # güncel
                finally:
                    vt.close()
            except Exception:
                # Tablo yok ya da veritabanı bozuk: baştan kuruluyor.
                pass
            _drop(imlec, name)

        imlec.execute(f"CREATE DATABASE [{name}]")
    finally:
        ana.close()

    vt = _connect(driver, server, name, autocommit=True)
    try:
        imlec = vt.cursor()
        for parca in _split_batches(seed_sql):
            imlec.execute(parca)
        imlec.execute(f"CREATE TABLE dbo.{SEED_TABLE} (ozet CHAR(64) NOT NULL)")
        imlec.execute(f"INSERT INTO dbo.{SEED_TABLE} (ozet) VALUES (?)", ozet)
    finally:
        vt.close()


def _drop(cursor, name: str) -> None:
    """Açık bağlantı olsa bile veritabanını düşürür."""
    cursor.execute(
        f"ALTER DATABASE [{name}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE"
    )
    cursor.execute(f"DROP DATABASE [{name}]")
    cursor.execute("USE master")


# --- çalıştırma -------------------------------------------------------


def _normalise(value):
    """Sonuç hücresini JSON'a yazılabilir hâle getirir.

    `Decimal` ve tarih türleri doğrudan JSON'a yazılamıyor; ayrıca
    beklenen değerler `exercise.json` içinde düz JSON olarak duruyor,
    yani karşılaştırma da bu biçim üzerinden yapılmalı.
    """
    if isinstance(value, decimal.Decimal):
        return float(value)
    if isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
        return value.isoformat()
    if isinstance(value, (bytes, bytearray)):
        return value.hex()
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, (int, float, str)):
        return value
    return str(value)


def _fingerprint(cursor) -> list:
    """Şemanın parmak izi: tablo ve sütun listesi.

    `schema_unchanged` kontrolü bunu öğrencinin SQL'inden önce ve sonra
    alıp karşılaştırıyor.
    """
    cursor.execute(
        "SELECT t.name, c.name, ty.name "
        "FROM sys.tables t "
        "JOIN sys.columns c ON c.object_id = t.object_id "
        "JOIN sys.types ty ON ty.user_type_id = c.user_type_id "
        "ORDER BY t.name, c.column_id"
    )
    return [tuple(r) for r in cursor.fetchall()]


def execute(driver: str, server: str, name: str, sql: str, checks: list[dict]) -> dict:
    """SQL'i işlem içinde çalıştırır, sonucu toplar ve **geri alır**.

    Dönen sözlük `harness.py`'nin sonuç biçimine uyuyor: `status`,
    `stdout` (öğrenciye gösterilecek tablo), `error`, `checks`.
    """
    baglanti = _connect(driver, server, name, autocommit=False)
    sonuc: dict = {
        "columns": [],
        "rows": [],
        "affected": -1,
        "error": None,
        "schema_changed": False,
        "verify": {},
    }
    try:
        imlec = baglanti.cursor()
        once = _fingerprint(imlec)

        try:
            son_sutunlar: list[str] = []
            son_satirlar: list[list] = []
            etkilenen = -1
            for parca in _split_batches(sql):
                imlec.execute(parca)
                # Bir toplu iş birden çok sonuç kümesi döndürebiliyor;
                # öğrenciye **sonuncusu** gösteriliyor, çünkü aradaki
                # yardımcı sorgular sonucu değil hazırlığı anlatıyor.
                while True:
                    if imlec.description is not None:
                        son_sutunlar = [d[0] for d in imlec.description]
                        son_satirlar = [
                            [_normalise(h) for h in satir]
                            for satir in imlec.fetchall()
                        ]
                    elif imlec.rowcount is not None and imlec.rowcount >= 0:
                        etkilenen = imlec.rowcount
                    if not imlec.nextset():
                        break
            sonuc["columns"] = son_sutunlar
            sonuc["rows"] = son_satirlar
            sonuc["affected"] = etkilenen
        except Exception as exc:
            sonuc["error"] = _format_sql_error(exc)

        if sonuc["error"] is None:
            sonuc["schema_changed"] = _fingerprint(imlec) != once
            # Doğrulama sorguları **öğrencinin SQL'inden sonra, geri
            # almadan önce** çalışıyor: `INSERT` yazan bir alıştırmada
            # tablonun son hâline böyle bakılıyor.
            for kontrol in checks:
                sorgu = kontrol.get("query")
                if not sorgu or sorgu in sonuc["verify"]:
                    continue
                try:
                    imlec.execute(sorgu)
                    sonuc["verify"][sorgu] = {
                        "columns": [d[0] for d in imlec.description or []],
                        "rows": [
                            [_normalise(h) for h in satir]
                            for satir in imlec.fetchall()
                        ],
                    }
                except Exception as exc:
                    sonuc["verify"][sorgu] = {"error": _format_sql_error(exc)}
    finally:
        # Ne olursa olsun geri alınıyor: bir sonraki çalıştırma temiz
        # bir veritabanıyla başlıyor.
        try:
            baglanti.rollback()
        except Exception:
            pass
        baglanti.close()
    return sonuc


def _format_sql_error(exc: Exception) -> dict:
    """Sunucunun hata mesajını okunur hâle getirir.

    Ham mesaj sürücü ve sunucu adlarıyla dolu:
    `[42S02] [Microsoft][ODBC Driver 18...][SQL Server]Invalid object
    name 'x'. (208)`. Öğrenciyi ilgilendiren yalnızca son cümle.
    """
    ham = ""
    if getattr(exc, "args", None):
        ham = str(exc.args[-1] if len(exc.args) > 1 else exc.args[0])
    ham = ham or str(exc)

    mesaj = ham
    if "[SQL Server]" in ham:
        mesaj = ham.split("[SQL Server]")[-1]
    # Sondaki `(208) (SQLExecDirectW)` gibi kodları at.
    mesaj = re.sub(r"\s*\(\d+\)\s*(\(\w+\))?\s*$", "", mesaj).strip()

    kod = ""
    eslesme = re.match(r"\[(\w+)\]", ham)
    if eslesme:
        kod = eslesme.group(1)
    return {"type": "SqlError", "message": mesaj or ham, "code": kod}


# --- kontroller -------------------------------------------------------

# Yorumlar ve dize sabitleri: `sql_require` / `sql_forbid` bunların
# içindeki kelimeyi saymamalı. `-- JOIN yazma` diyen bir yorum yüzünden
# "JOIN kullanmışsın" demek saçma olurdu.
COMMENT_BLOCK = re.compile(r"/\*.*?\*/", re.DOTALL)
COMMENT_LINE = re.compile(r"--[^\n]*")
STRING_LITERAL = re.compile(r"'(?:[^']|'')*'")


def strip_noise(sql: str) -> str:
    """Yorumları ve dize sabitlerini boşlukla değiştirir."""
    temiz = COMMENT_BLOCK.sub(" ", sql)
    temiz = COMMENT_LINE.sub(" ", temiz)
    return STRING_LITERAL.sub(" '' ", temiz)


def _contains(sql: str, pattern: str) -> bool:
    """Anahtar kelimeyi kelime sınırına saygı göstererek arar.

    `pattern` birden çok kelime içerebiliyor (`GROUP BY`); aradaki boşluk
    sayısı serbest bırakılıyor, çünkü öğrenci satır sonu da koyabiliyor.
    """
    parcalar = [re.escape(p) for p in pattern.split()]
    kalip = r"\b" + r"\s+".join(parcalar) + r"\b"
    return re.search(kalip, sql, re.IGNORECASE) is not None


def _same_cell(actual, expected) -> bool:
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        if isinstance(expected, bool) or isinstance(actual, bool):
            return actual == expected
        return abs(float(actual) - float(expected)) <= FLOAT_TOLERANCE
    return actual == expected


def _same_rows(actual: list, expected: list, ordered: bool) -> bool:
    if len(actual) != len(expected):
        return False
    if not ordered:
        # Sıra önemsizse iki taraf da aynı kurala göre sıralanıyor.
        actual = sorted(actual, key=lambda r: [str(h) for h in r])
        expected = sorted(expected, key=lambda r: [str(h) for h in r])
    for a, b in zip(actual, expected):
        if len(a) != len(b) or not all(_same_cell(x, y) for x, y in zip(a, b)):
            return False
    return True


def run_checks(checks: list[dict], outcome: dict, sql: str) -> list[dict]:
    """SQL kontrollerini uygular; `harness.py`'nin biçiminde döndürür."""
    temiz_sql = strip_noise(sql)
    sonuclar = []

    for kontrol in checks:
        tur = kontrol.get("type", "")
        ipucu = kontrol.get("hint", {})

        if tur == "rows":
            sorgu = kontrol.get("query")
            if sorgu:
                kaynak = outcome["verify"].get(sorgu, {})
            else:
                kaynak = {"columns": outcome["columns"], "rows": outcome["rows"]}
            if kaynak.get("error"):
                gecti, ayrinti = False, {"query_error": kaynak["error"]}
            else:
                beklenen = kontrol.get("expected", [])
                sirali = bool(kontrol.get("ordered", True))
                gecti = _same_rows(kaynak.get("rows", []), beklenen, sirali)
                ayrinti = {
                    "expected": beklenen,
                    "actual": kaynak.get("rows", []),
                    "columns": kaynak.get("columns", []),
                    "ordered": sirali,
                }

        elif tur == "columns":
            beklenen = list(kontrol.get("expected", []))
            olan = list(outcome["columns"])
            if kontrol.get("ignore_case", True):
                gecti = [c.lower() for c in olan] == [c.lower() for c in beklenen]
            else:
                gecti = olan == beklenen
            ayrinti = {"expected": beklenen, "actual": olan}

        elif tur == "affected_rows":
            beklenen = int(kontrol.get("expected", 0))
            gecti = outcome["affected"] == beklenen
            ayrinti = {"expected": beklenen, "actual": outcome["affected"]}

        elif tur == "sql_require":
            kalip = str(kontrol.get("pattern", ""))
            gecti = _contains(temiz_sql, kalip)
            ayrinti = {"pattern": kalip}

        elif tur == "sql_forbid":
            kalip = str(kontrol.get("pattern", ""))
            gecti = not _contains(temiz_sql, kalip)
            ayrinti = {"pattern": kalip}

        elif tur == "schema_unchanged":
            gecti = not outcome["schema_changed"]
            ayrinti = {"changed": outcome["schema_changed"]}

        else:
            gecti, ayrinti = False, {"unknown": tur}

        sonuclar.append(
            {"type": tur, "passed": gecti, "detail": ayrinti, "hint": ipucu}
        )
    return sonuclar


# --- giriş noktası ----------------------------------------------------


def render_table(columns: list[str], rows: list[list], limit: int = 50) -> str:
    """Sonuç kümesini öğrenciye gösterilecek düz metne çevirir.

    Python alıştırmalarında bu alanı öğrencinin `print`'leri dolduruyor;
    SQL'de yazdıracak bir şey yok, sonucun kendisi çıktı.
    """
    if not columns:
        return ""
    gosterilen = rows[:limit]
    hucreler = [[("NULL" if h is None else str(h)) for h in satir]
                for satir in gosterilen]
    genislik = [len(c) for c in columns]
    for satir in hucreler:
        for i, h in enumerate(satir):
            if i < len(genislik):
                genislik[i] = max(genislik[i], len(h))

    def yaz(parcalar):
        return "  ".join(p.ljust(genislik[i]) for i, p in enumerate(parcalar))

    satirlar = [yaz(columns), "  ".join("-" * g for g in genislik)]
    satirlar += [yaz(s) for s in hucreler]
    if len(rows) > limit:
        satirlar.append(f"... ({len(rows)} satirdan ilk {limit} tanesi)")
    return "\n".join(satirlar)


def run(job: dict) -> dict:
    """`harness.py` buradan çağırıyor. Sonuç sözlüğünü döndürür."""
    sql = Path(job["code_path"]).read_text(encoding="utf-8")
    checks = job.get("checks", [])
    anahtar = job.get("exercise_key") or Path(job["code_path"]).stem
    tohum_yolu = job.get("seed_path", "")
    ipucu = job.get("server_hint", "")

    sonuc: dict = {
        "status": "ok",
        "stdout": "",
        "stderr": "",
        "truncated": False,
        "error": None,
        "checks": [],
        "artifacts": [],
        "server": "",
    }

    try:
        surucu, sunucu = find_server(ipucu)
    except SqlUnavailable as exc:
        sonuc["status"] = "error"
        sonuc["error"] = {
            "type": "SqlUnavailable",
            "message": exc.reason,
            "detail": exc.detail,
        }
        return sonuc

    sonuc["server"] = sunucu
    ad = database_name(anahtar)
    tohum = ""
    if tohum_yolu and Path(tohum_yolu).exists():
        tohum = Path(tohum_yolu).read_text(encoding="utf-8")

    try:
        ensure_database(surucu, sunucu, ad, tohum)
    except Exception as exc:
        sonuc["status"] = "error"
        sonuc["error"] = _format_sql_error(exc)
        sonuc["error"]["type"] = "SeedError"
        return sonuc

    cikti = execute(surucu, sunucu, ad, sql, checks)
    sonuc["stdout"] = render_table(cikti["columns"], cikti["rows"])
    if cikti["error"] is not None:
        sonuc["status"] = "error"
        sonuc["error"] = cikti["error"]
    sonuc["checks"] = run_checks(checks, cikti, sql)
    return sonuc
