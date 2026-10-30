"""Rust alıştırmaları: kişinin kodu gerçek derleyiciyle derleniyor ve çalışıyor.

Derleyiciyi kişi kuruyor (rustup; patikanın ilk bölümü öğretiyor). Yoksa
alıştırma hata vermiyor, `rust` durumu dönüyor ve arayüz ne eksik olduğunu
söylüyor (Docker alıştırması gibi).

Klasörde `Cargo.toml` varsa `cargo`, yoksa doğrudan `rustc`. İkisinde de
tanılar JSON okunuyor: hata kodu ve satır oradan, terminale derleyicinin
kendi metni gidiyor. Kod yalnızca başarılı derlemede çalışıyor. Python'daki
gibi `main` her çalıştırmada koşuyor; kişi kendi `println!`'lerini görsün.

Kontroller:
- `stdout`: ana çalıştırmanın çıktısı.
- `stdio`: her durumda program argüman ve girdiyle yeniden çalışıyor.
- `rust_test`: yazarın testleri kişinin kaynağının sonuna eklenip
  `--test` ile derleniyor (`use super::*`, özel öğeler de görünür).
- `rust_tests`: kişinin kendi testleri; `min` ve bozuk sürümler (`mutants`).
- `rust_require` / `rust_forbid`: yorum ve metin atılmış kaynakta desen.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import threading
from dataclasses import dataclass, field
from pathlib import Path

from docker_runner import _fail, _ok

MAX_OUTPUT_BYTES = 100_000
MAX_DETAIL_CHARS = 1_500
BUILD_DIR = ".odyssey-build"
EDITION = "2024"
HIDDEN_MODULE = "odyssey_hidden"
HIDDEN_TEST = "check_"

# Uygulama denetiminin çalıştırmayı engellediğini söyleyen Windows hataları
# (`updater.BLOCKED_ERRORS` ile aynı ölçüm: 4551 uygulama denetimi).
BLOCKED_ERRORS = {4551, 1260, 225, 226}
EXIT_PANIC = 101
# Windows'ta işletim sisteminin öldürdüğü süreç: durum kodu çıkış kodu olarak
# geliyor (yığın taşması 0xC00000FD, erişim hatası 0xC0000005).
CRASH_CODE_MIN = 0xC0000000

NO_TOOLCHAIN = re.compile(r"could not choose a version|no override and no default toolchain", re.I)
NO_LINKER = re.compile(r"linker `[^`]*` not found|link\.exe.*not found", re.I)
PANIC = re.compile(r"panicked at ([^\n]+?):(\d+):\d+:\n([^\n]*)")
TEST_LINE = re.compile(r"^test (\S+)(?: - should panic)? \.\.\. (ok|FAILED)\s*$", re.M)
FAILURE_BLOCK = re.compile(r"^---- (\S+) stdout ----\n(.*?)(?=^---- |^failures:|\Z)", re.M | re.S)
# Yorum, metin ve karakter sabitleri. `'a` ömrü kapanış tırnağı olmadığı için
# karakter sabiti sanılmıyor; `'"'` metin başlangıcı sanılmıyor.
NOISE = re.compile(
    r"""
    //[^\n]*
  | /\*.*?\*/
  | b?r(?P<hashes>\#*)".*?"(?P=hashes)
  | b?"(?:\\.|[^"\\])*"
  | b?'(?:\\.[^']*|[^\\'\n])'
    """,
    re.VERBOSE | re.DOTALL,
)


def find_tool(name: str) -> str | None:
    """Araç yolu. Kurulumdan sonra program yeniden başlatılmadıysa PATH eski
    olabilir; rustup'ın varsayılan klasörüne de bakılıyor."""
    found = shutil.which(name)
    if found:
        return found
    cargo_home = Path(os.environ.get("CARGO_HOME") or Path.home() / ".cargo")
    candidate = cargo_home / "bin" / (name + (".exe" if sys.platform == "win32" else ""))
    return str(candidate) if candidate.is_file() else None


class ToolchainProblem(Exception):
    """Kişinin kodundan değil, kurulumdan gelen sorun; `state` arayüze gider."""

    def __init__(self, state: str):
        super().__init__(state)
        self.state = state


@dataclass
class Diagnostic:
    level: str
    message: str
    rendered: str
    code: str = ""
    file: str = ""
    line: int = 0


@dataclass
class Build:
    ok: bool
    diagnostics: list[Diagnostic] = field(default_factory=list)
    # Tanı üretmeden düşen derleme (bozuk Cargo.toml gibi): aracın kendi metni.
    raw_error: str = ""
    executables: list[Path] = field(default_factory=list)

    @property
    def errors(self) -> list[Diagnostic]:
        return [d for d in self.diagnostics if d.level == "error"]


@dataclass
class Execution:
    stdout: str
    stderr: str
    code: int
    truncated: bool = False


def _diagnostic(message: dict) -> Diagnostic | None:
    if not isinstance(message, dict) or not message.get("rendered"):
        return None
    primary = next((s for s in message.get("spans") or [] if s.get("is_primary")), None) or {}
    code = (message.get("code") or {}).get("code") or ""
    return Diagnostic(
        level=str(message.get("level", "")),
        message=str(message.get("message", "")),
        rendered=str(message["rendered"]),
        code=str(code),
        file=str(primary.get("file_name", "")).replace("\\", "/"),
        line=int(primary.get("line_start") or 0),
    )


def _json_lines(text: str) -> list[dict]:
    items = []
    for line in text.splitlines():
        if line.startswith("{"):
            try:
                items.append(json.loads(line))
            except ValueError:
                continue
    return items


def _hidden_window_flags() -> int:
    return subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0


class _Project:
    """Tek dosya (`rustc`) ya da Cargo projesi: derleme ayrıntısı burada kalıyor."""

    def __init__(self, workspace: Path, entry: Path):
        self.workspace = workspace
        self.entry = entry
        self.is_cargo = (workspace / "Cargo.toml").is_file()
        self.tool = find_tool("cargo" if self.is_cargo else "rustc")
        if self.tool is None:
            raise ToolchainProblem("missing")

    def build(self, *, tests: bool = False) -> Build:
        build = self._cargo(tests) if self.is_cargo else self._rustc(tests)
        for text in [build.raw_error, *(d.rendered for d in build.errors)]:
            if NO_TOOLCHAIN.search(text):
                raise ToolchainProblem("missing")
            if NO_LINKER.search(text):
                raise ToolchainProblem("no_linker")
        return build

    def _call(self, args: list[str], env: dict | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            args, cwd=self.workspace, capture_output=True, stdin=subprocess.DEVNULL,
            text=True, encoding="utf-8", errors="replace",
            creationflags=_hidden_window_flags(), env=env,
        )

    def _rustc(self, tests: bool) -> Build:
        folder = self.workspace / BUILD_DIR
        folder.mkdir(exist_ok=True)
        output = folder / (("tests" if tests else "program") + (".exe" if sys.platform == "win32" else ""))
        args = [self.tool, f"--edition={EDITION}", "--error-format=json", "-C", "debuginfo=0",
                self.entry.relative_to(self.workspace).as_posix(), "-o", str(output)]
        if tests:
            # Yazarın test kodu kişiye uyarı olarak dönmesin.
            args += ["--test", "-A", "warnings"]
        done = self._call(args)
        diagnostics = [d for d in map(_diagnostic, _json_lines(done.stderr)) if d is not None]
        if done.returncode != 0:
            return Build(False, diagnostics, raw_error="" if diagnostics else self._clean(done.stderr))
        return Build(True, diagnostics, executables=[output])

    def _cargo(self, tests: bool) -> Build:
        env = {**os.environ, "CARGO_TARGET_DIR": str(self.workspace / BUILD_DIR), "CARGO_TERM_COLOR": "never"}
        args = [self.tool, "test", "--no-run"] if tests else [self.tool, "build"]
        done = self._call([*args, "--offline", "--message-format=json", "--quiet"], env)
        diagnostics: list[Diagnostic] = []
        executables: list[Path] = []
        for item in _json_lines(done.stdout):
            if item.get("reason") == "compiler-message":
                found = _diagnostic(item.get("message"))
                if found is not None:
                    diagnostics.append(found)
            elif item.get("reason") == "compiler-artifact" and item.get("executable"):
                if bool((item.get("profile") or {}).get("test")) == tests:
                    executables.append(Path(item["executable"]))
        if done.returncode != 0:
            return Build(False, diagnostics, raw_error="" if diagnostics else self._clean(done.stderr))
        return Build(True, diagnostics, executables=executables)

    def _clean(self, text: str) -> str:
        """Geçici klasörün yolu (kullanıcı adını taşıyor) ekrana gitmesin."""
        return text.replace(str(self.workspace) + os.sep, "").replace(str(self.workspace), ".").strip()


def execute(program: Path, cwd: Path, argv: list[str], stdin: str) -> Execution:
    """Programı çalıştırır; çıktı sınırı aşılırsa durdurur (süre dış sürecin işi)."""
    try:
        process = subprocess.Popen(
            [str(program), *argv], cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, creationflags=_hidden_window_flags(),
        )
    except OSError as exc:
        if getattr(exc, "winerror", None) in BLOCKED_ERRORS:
            raise ToolchainProblem("blocked") from exc
        raise
    collected = {"stdout": bytearray(), "stderr": bytearray()}
    over_limit = threading.Event()

    def drain(stream, buffer: bytearray) -> None:
        while chunk := stream.read(65536):
            room = MAX_OUTPUT_BYTES - len(buffer)
            buffer.extend(chunk[:max(room, 0)])
            if len(chunk) > room:
                over_limit.set()
                process.kill()
                # Süreç ölene kadar okumaya devam: boru dolu kalıp asılmasın.

    readers = [threading.Thread(target=drain, args=(process.stdout, collected["stdout"]), daemon=True),
               threading.Thread(target=drain, args=(process.stderr, collected["stderr"]), daemon=True)]
    for reader in readers:
        reader.start()
    try:
        if stdin:
            process.stdin.write(stdin.encode("utf-8"))
        process.stdin.close()
    except OSError:
        pass  # Program girdiyi okumadan bitti ya da kapattı; hata değil.
    code = process.wait()
    for reader in readers:
        reader.join()
    return Execution(
        stdout=collected["stdout"].decode("utf-8", "replace"),
        stderr=collected["stderr"].decode("utf-8", "replace"),
        code=code,
        truncated=over_limit.is_set(),
    )


def runtime_error(run: Execution) -> dict | None:
    """Çalışma hatası: panik ya da işletim sisteminin öldürdüğü süreç."""
    if run.truncated:
        return None
    if run.code == EXIT_PANIC:
        found = PANIC.search(run.stderr)
        if found:
            file, line, message = found.groups()
            return {"type": "panic", "message": message, "line": int(line), "file": file.replace("\\", "/")}
        return {"type": "panic", "message": run.stderr.strip()[:MAX_DETAIL_CHARS]}
    if run.code >= CRASH_CODE_MIN or run.code < 0:
        return {"type": "crash", "message": f"0x{run.code & 0xFFFFFFFF:08X}"}
    return None


def strip_noise(source: str) -> str:
    """Yorum ve metinleri atar: yorumdaki `.clone()` kod sayılmasın."""
    return NOISE.sub(" ", source)


# --- kontroller -------------------------------------------------------------


def _hidden_tests_source(check: dict) -> str:
    bodies = "\n".join(
        f"    #[test]\n    fn {HIDDEN_TEST}{index}() {{\n        {test['code']}\n    }}"
        for index, test in enumerate(check.get("tests", []))
    )
    prelude = str(check.get("prelude", ""))
    return f"\n#[cfg(test)]\nmod {HIDDEN_MODULE} {{\n    use super::*;\n    {prelude}\n{bodies}\n}}\n"


def _test_report(project: _Project, build: Build) -> tuple[list[tuple[str, bool]], dict[str, str]]:
    """Test programlarını çalıştırır: (ad, geçti mi) listesi ve düşenlerin metni."""
    results: list[tuple[str, bool]] = []
    failures: dict[str, str] = {}
    for program in build.executables:
        run = execute(program, project.workspace, ["--test-threads=1"], "")
        text = run.stdout.replace("\r\n", "\n")
        results += [(name, state == "ok") for name, state in TEST_LINE.findall(text)]
        for name, block in FAILURE_BLOCK.findall(text):
            failures[name] = _failure_text(block)
    return results, failures


def _failure_text(block: str) -> str:
    """Testin panik metni; süreç kimliği ve geri izleme notu atılıyor."""
    lines = [line for line in block.strip().splitlines()
             if "panicked at" not in line and not line.startswith("note: run with")]
    return "\n".join(lines).strip()[:MAX_DETAIL_CHARS]


def _first_error_text(build: Build) -> str:
    if build.errors:
        return build.errors[0].rendered.strip()[:MAX_DETAIL_CHARS]
    return build.raw_error[:MAX_DETAIL_CHARS]


def check_hidden_tests(check: dict, project: _Project) -> dict:
    original = project.entry.read_text(encoding="utf-8")
    try:
        project.entry.write_text(original + _hidden_tests_source(check), encoding="utf-8")
        build = project.build(tests=True)
        if not build.ok:
            return _fail("signature", error=_first_error_text(build))
        results, failures = _test_report(project, build)
    finally:
        project.entry.write_text(original, encoding="utf-8")

    prefix = f"{HIDDEN_MODULE}::{HIDDEN_TEST}"
    outcomes = {name.removeprefix(prefix): passed for name, passed in results if name.startswith(prefix)}
    tests = check.get("tests", [])
    if len(outcomes) != len(tests):
        return _fail("crashed")
    for index, test in enumerate(tests):
        if not outcomes.get(str(index)):
            return _fail("failed", name=test.get("label", str(index)),
                         error=failures.get(f"{prefix}{index}", ""))
    return _ok(count=len(tests))


def check_user_tests(check: dict, project: _Project) -> dict:
    build = project.build(tests=True)
    if not build.ok:
        return _fail("compile_error", error=_first_error_text(build))
    results, failures = _test_report(project, build)
    if not results:
        return _fail("no_tests")
    failed = [name for name, passed in results if not passed]
    if failed:
        return _fail("failed", name=failed[0], count=len(failed), total=len(results),
                     error=failures.get(failed[0], ""))
    low = int(check.get("min", 1))
    if len(results) < low:
        return _fail("too_few", count=len(results), min=low)
    for mutant in check.get("mutants") or []:
        if not _mutant_caught(mutant, project):
            bug = mutant.get("bug", "")
            return _fail("missed_bug", bug=bug if isinstance(bug, dict) else str(bug), total=len(results))
    return _ok(count=len(results))


def _mutant_caught(mutant: dict, project: _Project) -> bool:
    """Bozuk sürümde en az bir test düşüyor mu? Kişi başka türlü yazdıysa ve
    bozulacak metin yoksa sınanacak bir şey de yok: yakalanmış sayılıyor."""
    target = project.workspace / str(mutant["file"]) if mutant.get("file") else project.entry
    original = target.read_text(encoding="utf-8")
    if "source" in mutant:
        changed = str(mutant["source"])
    else:
        old, new = mutant["replace"]
        if old not in original:
            return True
        changed = original.replace(old, new)
    try:
        target.write_text(changed, encoding="utf-8")
        build = project.build(tests=True)
        if not build.ok:
            return True
        results, _ = _test_report(project, build)
    finally:
        target.write_text(original, encoding="utf-8")
    return any(not passed for _, passed in results)


def check_source(check: dict, kind: str, project: _Project) -> dict:
    target = project.workspace / str(check["file"]) if check.get("file") else project.entry
    found = re.search(str(check["pattern"]), strip_noise(target.read_text(encoding="utf-8")))
    show = check.get("show", check["pattern"])
    if kind == "rust_forbid" and found:
        return _fail("forbidden", show=show)
    if kind == "rust_require" and not found:
        return _fail("required", show=show)
    return _ok()


def check_stdio(check: dict, program: Path, workspace: Path, compare_stdout) -> dict:
    """Her durumda programı çalıştırır; ayrıntı biçimi Python'daki `stdio` ile aynı."""
    for index, case in enumerate(check.get("cases", [])):
        argv = [str(a) for a in case.get("argv", [])]
        stdin = str(case.get("stdin", ""))
        run = execute(program, workspace, argv, stdin)
        shared = {"case": index, "stdin": stdin, "argv": argv, "command": " ".join(["./main", *argv]),
                  "transcript": run.stdout[:MAX_DETAIL_CHARS]}
        error = runtime_error(run)
        if error:
            return {"passed": False, "detail": {**shared, "error": f"{error['type']}: {error['message']}"}}
        if "stdout" in case:
            compared = compare_stdout({"expected": case["stdout"], "match": check.get("match", "trimmed_lines")},
                                      run.stdout)
            if not compared["passed"]:
                return {"passed": False, "detail": {**shared, **compared["detail"]}}
        if "exit" in case and run.code != case["exit"]:
            return {"passed": False, "detail": {**shared, "exit": run.code, "expected_exit": case["exit"]}}
    return {"passed": True, "detail": {"cases": len(check.get("cases", []))}}


# --- akış -------------------------------------------------------------------


UNAVAILABLE_REASONS = {"missing": "no_rust", "no_linker": "no_linker", "blocked": "blocked"}


def _unavailable(state: str) -> dict:
    """Kurulum eksik: kontrol tek ve düşük, terminal ne yapılacağını söylüyor."""
    detail = {"reason": UNAVAILABLE_REASONS[state], "values": {}}
    return {
        "status": "ok", "stdout": "", "stderr": "", "truncated": False, "error": None,
        "rust": {"state": state},
        "checks": [{"type": "rust", "passed": False, "detail": detail, "hint": {}}],
    }


def _compile_failure(build: Build, multi_file: bool) -> dict:
    errors = build.errors
    first = next((d for d in errors if d.line), errors[0] if errors else None)
    if first is None:
        error = {"type": "rustc", "message": build.raw_error.splitlines()[0] if build.raw_error else ""}
        stderr = build.raw_error
    else:
        message = f"{first.code}: {first.message}" if first.code else first.message
        error = {"type": "rustc", "message": message, "code": first.code}
        if first.line:
            error["line"] = first.line
        if multi_file and first.file:
            error["file"] = first.file
        stderr = "\n".join(d.rendered.rstrip() for d in errors)
    return {"status": "error", "stdout": "", "stderr": stderr, "truncated": False, "error": error,
            "rust": {"state": "ok"}, "checks": []}


def _evaluate(check: dict, project: _Project, main_run: Execution, program: Path | None, compare_stdout) -> dict:
    kind = check.get("type", "")
    if kind == "stdout":
        return compare_stdout(check, main_run.stdout)
    if kind == "stdio":
        return check_stdio(check, program, project.workspace, compare_stdout)
    if kind == "rust_test":
        outcome = check_hidden_tests(check, project)
    elif kind == "rust_tests":
        outcome = check_user_tests(check, project)
    elif kind in ("rust_forbid", "rust_require"):
        outcome = check_source(check, kind, project)
    else:
        outcome = _fail("bad_type", type=kind)
    return {"passed": outcome["passed"], "detail": {"reason": outcome["reason"], "values": outcome["values"]}}


def run(job: dict, compare_stdout) -> dict:
    workspace = Path(job.get("workspace") or Path(job["code_path"]).parent).resolve()
    entry = Path(job["code_path"]).resolve()
    checks = job.get("checks", [])
    multi_file = bool(job.get("user_files"))
    try:
        project = _Project(workspace, entry)
        build = project.build()
        if not build.ok:
            return _compile_failure(build, multi_file)

        program = build.executables[0] if build.executables else None
        demo = next((c["cases"][0] for c in checks if c.get("type") == "stdio" and c.get("cases")), {})
        main_run = Execution("", "", 0)
        if program is not None:
            main_run = execute(program, workspace, [str(a) for a in demo.get("argv", [])],
                               str(demo.get("stdin", "")))
        result = {"status": "ok", "stdout": main_run.stdout, "stderr": main_run.stderr,
                  "truncated": main_run.truncated, "error": None, "rust": {"state": "ok"}, "checks": []}
        error = runtime_error(main_run)
        if error:
            if not multi_file:
                error.pop("file", None)
            result.update(status="error", error=error)
            return result
        for check in checks:
            outcome = _evaluate(check, project, main_run, program, compare_stdout)
            result["checks"].append({"type": check.get("type", ""), "passed": outcome["passed"],
                                     "detail": outcome["detail"], "hint": check.get("hint", {})})
        return result
    except ToolchainProblem as problem:
        return _unavailable(problem.state)
