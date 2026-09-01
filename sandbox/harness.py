"""Kullanıcı kodunu çalıştırıp kontrolleri uygulayan yardımcı.

Bu dosya **ayrı bir süreçte** çalışır ve uygulamanın hiçbir modülünü import
etmez. Tek başına ayakta durur, çünkü kullanıcının kodu bu sürecin içinde
çalışıyor ve o sürecin çökmesi uygulamayı etkilememeli.

Kullanım:
    python harness.py <job.json>

`job.json` içeriği:
    {
      "code_path":   çalıştırılacak dosya,
      "result_path": sonucun yazılacağı dosya,
      "checks":      uygulanacak kontroller
    }

Sonuç **stdout'a değil, dosyaya** yazılır. Sebebi basit: kullanıcının kodu
zaten stdout'a `print` ediyor, o kanalı sonuç için kullanamayız.

Not: Bu bir güvenlik sandbox'ı değildir. Kullanıcı kendi kodunu kendi
bilgisayarında çalıştırıyor. Buradaki koruma, kodun çökmesi veya takılması
durumunda uygulamanın etkilenmemesidir.
"""

from __future__ import annotations

import ast
import contextlib
import io
import json
import sys
import traceback
from pathlib import Path

# Çıktı bu sınırı aşarsa kesilir. Sonsuz döngü içinde print eden bir kod
# birkaç saniyede yüzlerce megabayt üretebiliyor.
MAX_OUTPUT_CHARS = 100_000

# Karşılaştırma mesajlarında gösterilecek değerin azami uzunluğu.
MAX_REPR_CHARS = 200


def clip(text: str, limit: int = MAX_OUTPUT_CHARS) -> tuple[str, bool]:
    """Metni sınıra kadar kırpar. (metin, kırpıldı mı) döndürür."""
    if len(text) <= limit:
        return text, False
    return text[:limit], True


def safe_repr(value: object) -> str:
    """Değeri güvenli biçimde metne çevirir.

    Kullanıcının tanımladığı bir sınıfın __repr__ metodu hata verebilir;
    o yüzden try ile sarmalıyoruz.
    """
    try:
        text = repr(value)
    except Exception:
        text = f"<{type(value).__name__} nesnesi>"
    clipped, _ = clip(text, MAX_REPR_CHARS)
    return clipped


# --- Kaynak koda bakan kontroller ------------------------------------------
# Bunlar kod çalışmadan önce yapılır, çünkü kod hata verse bile
# "döngü kullanmamışsın" gibi geri bildirimi verebilmek istiyoruz.


def called_names(tree: ast.AST) -> set[str]:
    """Kodda çağrılan fonksiyon adlarını toplar."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name):
            names.add(func.id)
        elif isinstance(func, ast.Attribute):
            names.add(func.attr)
    return names


def has_node_type(tree: ast.AST, node_name: str) -> bool:
    """Kodda belirtilen türde bir düğüm var mı? (örn. "For", "While")"""
    node_type = getattr(ast, node_name, None)
    if node_type is None or not isinstance(node_type, type):
        return False
    return any(isinstance(node, node_type) for node in ast.walk(tree))


def annotation_source(node: ast.AST | None) -> str | None:
    """Bir belirtim düğümünü metne çevirir.

    `ast.unparse` biçimi normalleştiriyor: `dict[str,str]` de
    `dict[str, str]` de aynı metne dönüyor, `str|None` de `str | None`
    oluyor. Bu yüzden öğrenci boşluğu farklı koyduğu için düşmüyor.
    """
    return None if node is None else ast.unparse(node)


def find_function(tree: ast.AST, name: str) -> ast.FunctionDef | None:
    """Verilen adı taşıyan fonksiyon tanımını bulur."""
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return node  # type: ignore[return-value]
    return None


def find_annotated_variable(tree: ast.AST, name: str) -> str | None:
    """`sayac: int = 0` biçimindeki bir değişkenin belirtimini döndürür."""
    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id == name:
                return annotation_source(node.annotation)
    return None


def compare_annotation(check: dict, tree: ast.AST | None) -> dict:
    """Tip belirtimi kontrolü.

    Belirtimler **kaynak koda** bakılarak doğrulanıyor, çalışma anına
    değil. Sebebi: belirtim çalışma anında hiçbir şey yapmıyor — kod
    belirtimsiz de sorunsuz çalışır. Dolayısıyla "yazdın mı" sorusunun
    cevabı yalnızca yazılan metinde var.

    İki biçimi var:
      { "type": "annotation", "name": "to_upper",
        "params": {"text": "str"}, "returns": "str" }
      { "type": "annotation", "variable": "count", "is": "int" }
    """
    if tree is None:
        return {"passed": False, "detail": {"unparsed": True}}

    variable = check.get("variable")
    if variable:
        actual = find_annotated_variable(tree, variable)
        expected = check.get("is", "")
        if actual is None:
            return {"passed": False, "detail": {"variable": variable, "bare": True,
                                                "expected": expected}}
        return {
            "passed": actual == expected,
            "detail": {"variable": variable, "expected": expected, "actual": actual},
        }

    name = check.get("name", "")
    target = find_function(tree, name)
    if target is None:
        return {"passed": False, "detail": {"name": name, "missing": True}}

    written = {
        arg.arg: annotation_source(arg.annotation)
        for arg in [*target.args.posonlyargs, *target.args.args, *target.args.kwonlyargs]
    }

    for param, expected in (check.get("params") or {}).items():
        if param not in written:
            return {"passed": False,
                    "detail": {"name": name, "param": param, "no_param": True}}
        actual = written[param]
        if actual is None:
            return {"passed": False,
                    "detail": {"name": name, "param": param, "bare": True,
                               "expected": expected}}
        if actual != expected:
            return {"passed": False,
                    "detail": {"name": name, "param": param,
                               "expected": expected, "actual": actual}}

    expected_return = check.get("returns")
    if expected_return is not None:
        actual_return = annotation_source(target.returns)
        if actual_return is None:
            return {"passed": False,
                    "detail": {"name": name, "returns": True, "bare": True,
                               "expected": expected_return}}
        if actual_return != expected_return:
            return {"passed": False,
                    "detail": {"name": name, "returns": True,
                               "expected": expected_return, "actual": actual_return}}

    return {"passed": True, "detail": {"name": name}}


# --- Çalışan koda bakan kontroller ------------------------------------------


def compare_stdout(check: dict, stdout: str) -> dict:
    """Çıktı kontrolü. Karşılaştırma biçimi `match` ile seçilir."""
    expected = str(check.get("expected", ""))
    mode = check.get("match", "trimmed_lines")

    if mode == "exact":
        passed = stdout == expected
    elif mode == "contains":
        passed = expected in stdout
    elif mode == "regex":
        import re

        passed = re.search(expected, stdout) is not None
    else:
        # trimmed_lines: satır başı/sonu boşlukları ve sondaki boş satırlar
        # yok sayılır. Kullanıcıyı görünmez bir boşluk yüzünden çevirmek
        # öğretici değil.
        def normalise(text: str) -> list[str]:
            lines = [line.strip() for line in text.splitlines()]
            while lines and not lines[-1]:
                lines.pop()
            return lines

        passed = normalise(stdout) == normalise(expected)

    return {
        "passed": passed,
        "detail": {
            "expected": expected,
            "actual": clip(stdout, MAX_REPR_CHARS)[0],
            "match": mode,
        },
    }


def find_value_holder(namespace: dict, expected) -> str:
    """Beklenen degeri tutan baska bir degiskenin adini dondurur.

    Alistirmanin istedigi ad yoksa is orada bitmiyordu: "boyle bir degisken
    tanimlamamissin" deyip geciyorduk. Oysa cogu zaman kisi isi dogru
    yapmis, yalnizca degiskene baska bir ad vermis oluyor. Ayni degeri
    tutan bir ad varsa onu buluyoruz ki geri bildirim "yanlis yaptin"
    yerine "adini su yapman gerekiyor" diyebilsin.

    Tip de karsilastiriliyor: True ile 1 Python'da esit, ama ogrenci
    acisindan ayni sey degil.
    """
    if expected is None:
        return ""

    for ad, deger in namespace.items():
        if ad.startswith("_"):
            continue
        try:
            if type(deger) is type(expected) and deger == expected:
                return ad
        except Exception:
            # Karsilastirmasi hata veren nesneler var (numpy dizileri gibi);
            # boyle bir deger adayimiz degil.
            continue
    return ""


def compare_variable(check: dict, namespace: dict) -> dict:
    """Değişken kontrolü: tanımlanmış mı ve değeri doğru mu?"""
    name = check.get("name", "")

    if name not in namespace:
        return {
            "passed": False,
            "detail": {
                "name": name,
                "missing": True,
                "lookalike": find_value_holder(namespace, check.get("equals")),
            },
        }

    actual = namespace[name]
    expected = check.get("equals")

    # bool ve int Python'da eşit sayılıyor (True == 1). Öğrencinin yanlış
    # tipte cevabı doğru sayılmasın diye tipi de karşılaştırıyoruz.
    same_type = type(actual) is type(expected)
    passed = same_type and actual == expected

    return {
        "passed": passed,
        "detail": {
            "name": name,
            "missing": False,
            "expected": safe_repr(expected),
            "actual": safe_repr(actual),
        },
    }


def compare_function(check: dict, namespace: dict) -> dict:
    """Fonksiyon kontrolü: her örnek çağrı beklenen sonucu veriyor mu?"""
    name = check.get("name", "")
    target = namespace.get(name)

    if target is None or not callable(target):
        return {"passed": False, "detail": {"name": name, "missing": True}}

    for case in check.get("cases", []):
        args = case.get("args", [])
        expected = case.get("returns")

        try:
            actual = target(*args)
        except Exception as exc:
            return {
                "passed": False,
                "detail": {
                    "name": name,
                    "missing": False,
                    "args": ", ".join(safe_repr(a) for a in args),
                    "raised": f"{type(exc).__name__}: {exc}",
                },
            }

        if actual != expected:
            return {
                "passed": False,
                "detail": {
                    "name": name,
                    "missing": False,
                    "args": ", ".join(safe_repr(a) for a in args),
                    "expected": safe_repr(expected),
                    "actual": safe_repr(actual),
                },
            }

    return {"passed": True, "detail": {"name": name, "missing": False}}


def compare_method(check: dict, namespace: dict) -> dict:
    """Sınıf kontrolü: nesne kurulup metotları çağrılıyor.

    `function` kontrolü yalnızca üst seviye fonksiyonlara bakıyor, `variable`
    ise nesne karşılaştıramıyor. Bir sınıfın **çalıştığını** doğrulamak için
    nesneyi gerçekten kurup metodunu çağırmak gerekiyor.

    Biçimi:
      { "type": "method", "class": "Dog", "args": ["Rex"],
        "cases": [
          { "method": "speak", "args": [], "returns": "Rex says woof" },
          { "attribute": "name", "equals": "Rex" }
        ] }
    """
    name = check.get("class", "")
    target = namespace.get(name)

    if target is None:
        return {"passed": False, "detail": {"cls": name, "missing": True}}
    if not isinstance(target, type):
        return {"passed": False, "detail": {"cls": name, "not_class": True}}

    args = check.get("args", [])
    try:
        instance = target(*args)
    except Exception as exc:
        return {
            "passed": False,
            "detail": {"cls": name, "init_raised": f"{type(exc).__name__}: {exc}",
                       "args": ", ".join(safe_repr(a) for a in args)},
        }

    for case in check.get("cases", []):
        attribute = case.get("attribute")
        if attribute:
            if not hasattr(instance, attribute):
                return {"passed": False,
                        "detail": {"cls": name, "attribute": attribute, "no_member": True}}
            actual = getattr(instance, attribute)
            expected = case.get("equals")
            if type(actual) is not type(expected) or actual != expected:
                return {"passed": False,
                        "detail": {"cls": name, "attribute": attribute,
                                   "expected": safe_repr(expected),
                                   "actual": safe_repr(actual)}}
            continue

        method = case.get("method", "")
        bound = getattr(instance, method, None)
        if bound is None or not callable(bound):
            return {"passed": False,
                    "detail": {"cls": name, "method": method, "no_member": True}}

        call_args = case.get("args", [])
        try:
            actual = bound(*call_args)
        except Exception as exc:
            return {
                "passed": False,
                "detail": {"cls": name, "method": method,
                           "args": ", ".join(safe_repr(a) for a in call_args),
                           "raised": f"{type(exc).__name__}: {exc}"},
            }

        if "returns" in case and actual != case["returns"]:
            return {
                "passed": False,
                "detail": {"cls": name, "method": method,
                           "args": ", ".join(safe_repr(a) for a in call_args),
                           "expected": safe_repr(case["returns"]),
                           "actual": safe_repr(actual)},
            }

    return {"passed": True, "detail": {"cls": name}}


# JSON'da demet diye bir tip yok; liste yazılınca `variable` kontrolü
# `type(actual) is type(expected)` karşılaştırmasında düşüyordu. Demet
# Python'da ayrı bir tip ve müfredatta öğretiliyor (`06-listeler`), ayrıca
# `sqlite3` satırları demet döndürüyor — beklenen değerin demet olduğunu
# yazabilmek gerekiyor.
#
# Bunu tipi gevşeterek değil, **açıkça yazarak** çözüyoruz:
#
#     { "type": "variable", "name": "point",
#       "equals": { "__tuple__": [3, 7] } }
#
# İç içe de çalışıyor: `[{"__tuple__": ["Ada", 90]}]` bir demet listesi.
TUPLE_KEY = "__tuple__"


def revive(value):
    """Kontrol tanımındaki demet işaretlerini gerçek demete çevirir."""
    if isinstance(value, dict):
        if set(value) == {TUPLE_KEY}:
            return tuple(revive(item) for item in value[TUPLE_KEY])
        return {key: revive(item) for key, item in value.items()}
    if isinstance(value, list):
        return [revive(item) for item in value]
    return value


def run_checks(checks: list[dict], tree: ast.AST | None, stdout: str, namespace: dict) -> list[dict]:
    """Bütün kontrolleri sırayla uygular."""
    results = []

    for check in checks:
        check = revive(check)
        kind = check.get("type")
        outcome: dict

        if kind == "stdout":
            outcome = compare_stdout(check, stdout)
        elif kind == "variable":
            outcome = compare_variable(check, namespace)
        elif kind == "function":
            outcome = compare_function(check, namespace)
        elif kind == "ast_require":
            found = tree is not None and has_node_type(tree, check.get("node", ""))
            outcome = {"passed": found, "detail": {"node": check.get("node", "")}}
        elif kind == "method":
            outcome = compare_method(check, namespace)
        elif kind == "annotation":
            outcome = compare_annotation(check, tree)
        elif kind == "ast_forbid":
            forbidden = check.get("call", "")
            used = tree is not None and forbidden in called_names(tree)
            outcome = {"passed": not used, "detail": {"call": forbidden}}
        else:
            outcome = {"passed": False, "detail": {"unknown_type": kind}}

        results.append({
            "type": kind,
            "passed": outcome["passed"],
            "detail": outcome["detail"],
            "hint": check.get("hint", {}),
        })

    return results


def format_user_traceback(exc: BaseException, code_path: str) -> dict:
    """Hata bilgisini, kullanıcının anlayacağı biçimde toparlar.

    Yığın izinden yalnızca kullanıcının kendi dosyasına ait satırlar tutulur;
    bu dosyanın (harness) satırları gösterilmez, kafa karıştırır.
    """
    if isinstance(exc, SyntaxError):
        return {
            "type": type(exc).__name__,
            "message": exc.msg or str(exc),
            "line": exc.lineno,
            "traceback": "",
        }

    frames = [
        frame for frame in traceback.extract_tb(exc.__traceback__)
        if frame.filename == code_path
    ]
    line = frames[-1].lineno if frames else None
    rendered = "".join(traceback.format_list(frames)) if frames else ""

    return {
        "type": type(exc).__name__,
        "message": str(exc),
        "line": line,
        "traceback": rendered,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("Kullanım: harness.py <job.json>", file=sys.stderr)
        return 2

    job = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    code_path = str(Path(job["code_path"]).resolve())
    result_path = Path(job["result_path"])
    checks = job.get("checks", [])

    source = Path(code_path).read_text(encoding="utf-8")

    # Kodun yanındaki dosyalar import edilebilsin.
    #
    # Denetleyici `-I` (izole kip) ile çalışıyor; o kip çalışan dosyanın
    # klasörünü `sys.path`'ten çıkarıyor. Bunun sonucu: alıştırmanın yanına
    # konan bir modül (`toolbox.py` gibi) kopyalandığı hâlde
    # `ModuleNotFoundError` veriyordu — "Modüller" bölümünde kullanıcıdan
    # tam olarak bunu yapması isteniyor.
    #
    # Eklenen tek klasör, o çalıştırmaya özel geçici çalışma klasörü:
    # içinde yalnızca kullanıcının kodu ve alıştırmanın kendi dosyaları var.
    workspace = str(Path(code_path).parent)
    if workspace not in sys.path:
        sys.path.insert(0, workspace)

    result: dict = {
        "status": "ok",
        "stdout": "",
        "stderr": "",
        "truncated": False,
        "error": None,
        "checks": [],
    }

    # 1) Önce kaynağı ayrıştır. Sözdizimi hatası varsa kod hiç çalışmaz ama
    #    yine de düzgün bir hata mesajı verebiliriz.
    tree: ast.AST | None = None
    try:
        tree = ast.parse(source, filename=code_path)
    except SyntaxError as exc:
        result["status"] = "error"
        result["error"] = format_user_traceback(exc, code_path)
        result["checks"] = run_checks(checks, None, "", {})
        result_path.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
        return 0

    # 2) Kodu temiz bir isim alanında çalıştır.
    namespace: dict = {"__name__": "__main__", "__file__": code_path}
    out_buffer, err_buffer = io.StringIO(), io.StringIO()

    try:
        compiled = compile(tree, filename=code_path, mode="exec")
        # input() çağrısı süreci sonsuza kadar bekletmesin diye stdin boş.
        with contextlib.redirect_stdout(out_buffer), contextlib.redirect_stderr(err_buffer):
            with contextlib.suppress(SystemExit):
                sys.stdin = io.StringIO()
                exec(compiled, namespace)
    except BaseException as exc:  # KeyboardInterrupt dahil her şeyi yakala
        result["status"] = "error"
        result["error"] = format_user_traceback(exc, code_path)

    stdout, truncated_out = clip(out_buffer.getvalue())
    stderr, truncated_err = clip(err_buffer.getvalue())

    result["stdout"] = stdout
    result["stderr"] = stderr
    result["truncated"] = truncated_out or truncated_err

    # 3) Kod hata verse bile kontrolleri uygula: kısmen doğru bir çözümde
    #    hangi adımların tuttuğunu görmek öğrenciye yol gösterir.
    result["checks"] = run_checks(checks, tree, stdout, namespace)

    result_path.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
