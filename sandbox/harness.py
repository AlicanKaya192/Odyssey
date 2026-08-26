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


def compare_variable(check: dict, namespace: dict) -> dict:
    """Değişken kontrolü: tanımlanmış mı ve değeri doğru mu?"""
    name = check.get("name", "")

    if name not in namespace:
        return {"passed": False, "detail": {"name": name, "missing": True}}

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


def run_checks(checks: list[dict], tree: ast.AST | None, stdout: str, namespace: dict) -> list[dict]:
    """Bütün kontrolleri sırayla uygular."""
    results = []

    for check in checks:
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
