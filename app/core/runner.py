"""Kullanıcı kodunu ayrı bir süreçte çalıştırır.

Kod doğrudan uygulamanın içinde çalıştırılmaz. Sonsuz bir döngü, bellek
tüketen bir işlem ya da beklenmedik bir çökme uygulamayı da yanına almasın
diye ayrı bir süreç açılır ve şunlar uygulanır:

- **İzole çalışma klasörü**: kod geçici bir klasörde çalışır, proje
  dosyalarına bulaşmaz.
- **İzole yorumlayıcı** (`-I`): kullanıcının `PYTHONPATH` ayarları ve
  site-packages kirinden etkilenmez.
- **Zaman aşımı**: süre dolarsa süreç ağacı öldürülür.
- **Çıktı sınırı**: `harness.py` çıktıyı 100KB'de kırpar.

Yine de bu bir güvenlik sandbox'ı değildir; kullanıcı kendi kodunu kendi
bilgisayarında çalıştırıyor.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import uuid
from dataclasses import dataclass, field
from pathlib import Path

from ..paths import artifacts_dir, exercise_python, is_frozen, sandbox_dir, workspace_dir

# Paketlenmiş uygulamanın kendini denetleyici olarak çağırdığı bayrak.
HARNESS_FLAG = "--run-harness"

# Süreç ağacını öldürdükten sonra beklenecek azami süre.
KILL_GRACE_SEC = 5

# Alıştırma klasöründe kopyalanmayacak dosyalar: bunlar meta veri ve çözüm.
# __pycache__: alistirma klasorunde bir kez calistirilmis bir modulden
# kalmis olabiliyor; bayat .pyc dosyalarini calisma klasorune tasimanin
# anlami yok.
SKIPPED_NAMES = {"exercise.json", "__pycache__"}
SKIPPED_SUFFIXES = {".md"}
# starter.py, starter.tr.py, solution.en.py ... hepsi disarida kalir.
SKIPPED_PREFIXES = ("starter", "solution", "prompt")


@dataclass
class CheckResult:
    """Tek bir kontrolün sonucu."""

    type: str
    passed: bool
    detail: dict
    hint: dict = field(default_factory=dict)


@dataclass
class RunResult:
    """Bir çalıştırmanın bütün sonucu."""

    status: str  # "ok" | "error" | "timeout" | "crashed"
    stdout: str = ""
    stderr: str = ""
    truncated: bool = False
    error: dict | None = None
    checks: list[CheckResult] = field(default_factory=list)
    # Kullanıcının kodunun ürettiği görsellerin yolları.
    artifacts: list[Path] = field(default_factory=list)
    timeout_sec: int = 0

    @property
    def passed(self) -> bool:
        """Alıştırma geçildi mi? Hata yoksa ve tüm kontroller tuttuysa."""
        return (
            self.status == "ok"
            and bool(self.checks)
            and all(check.passed for check in self.checks)
        )

    @property
    def failed_checks(self) -> list[CheckResult]:
        return [check for check in self.checks if not check.passed]


def interpreter() -> Path:
    """Kullanıcı kodunu çalıştıracak Python.

    Alıştırma ortamı kuruluysa o kullanılır (numpy, pandas oradadır).
    Kurulu değilse uygulamanın kendi yorumlayıcısına düşülür; böylece ortam
    kurulmadan da standart kütüphaneyle çözülen alıştırmalar çalışır.
    """
    dedicated = exercise_python()
    return dedicated if dedicated.exists() else Path(sys.executable)


def _harness_command(job_path: Path) -> list[str]:
    """Denetleyiciyi çalıştıracak komutu kurar.

    Paketlenmiş `.exe` içinde ayrı bir `python.exe` yok; `sys.executable`
    uygulamanın kendisi. Onu doğrudan çağırmak arayüzü ikinci kez açardı.
    Bu yüzden uygulama kendini özel bir bayrakla çağırıyor: `main.py` bu
    bayrağı görünce arayüzü hiç kurmadan denetleyiciyi çalıştırıyor.

    Alıştırma ortamı kuruluysa (numpy, pandas gerektiren bölümler için)
    normal yol izlenir.
    """
    dedicated = exercise_python()

    if dedicated.exists():
        return [str(dedicated), "-I", str(sandbox_dir() / "harness.py"), str(job_path)]

    if is_frozen():
        return [sys.executable, HARNESS_FLAG, str(job_path)]

    return [sys.executable, "-I", str(sandbox_dir() / "harness.py"), str(job_path)]


def exercise_env_ready() -> bool:
    """Alıştırmalara ayrılmış ortam kurulu mu?"""
    return exercise_python().exists()


def _kill_tree(process: subprocess.Popen) -> None:
    """Süreci ve altındaki bütün süreçleri öldürür.

    Windows'ta `process.kill()` yalnızca ana süreci öldürür; kullanıcının
    kodu alt süreç açtıysa onlar arkada kalır. `taskkill /T` ağacın tamamını
    alır.
    """
    if sys.platform == "win32":
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(process.pid)],
            capture_output=True,
            check=False,
        )
    else:
        process.kill()

    try:
        process.wait(timeout=KILL_GRACE_SEC)
    except subprocess.TimeoutExpired:
        pass


def _rescue_artifacts(entries: list[dict]) -> list[Path]:
    """Üretilen görselleri çalışma klasörü silinmeden önce kurtarır.

    `run_code` sonunda çalışma klasörünü siliyor; grafik orada üretildiği
    için onunla birlikte gidiyordu. Kullanıcı "dosya oluştu" yazısını
    görüyor ama dosyayı hiç göremiyordu.
    """
    hedef = artifacts_dir()
    # Yalnızca son çalıştırmanın çıktısı duruyor; eskiler birikmiyor.
    for eski in hedef.glob("*"):
        try:
            eski.unlink()
        except OSError:
            pass

    kurtarilan: list[Path] = []
    for girdi in entries:
        kaynak = Path(str(girdi.get("path", "")))
        if not kaynak.is_file():
            continue
        varis = hedef / kaynak.name
        try:
            shutil.copy2(kaynak, varis)
        except OSError:
            continue
        kurtarilan.append(varis)
    return kurtarilan


def _prepare_workspace(exercise_dir: Path | None) -> Path:
    """Bu çalıştırmaya özel geçici bir klasör hazırlar."""
    directory = workspace_dir() / uuid.uuid4().hex[:12]
    directory.mkdir(parents=True, exist_ok=True)

    # Alıştırmanın ihtiyaç duyduğu veri dosyalarını (CSV gibi) yanına al.
    if exercise_dir and exercise_dir.exists():
        for item in exercise_dir.iterdir():
            if (
                item.name in SKIPPED_NAMES
                or item.suffix in SKIPPED_SUFFIXES
                or item.name.startswith(SKIPPED_PREFIXES)
            ):
                continue
            if item.is_file():
                shutil.copy2(item, directory / item.name)
            elif item.is_dir():
                shutil.copytree(item, directory / item.name, dirs_exist_ok=True)

    return directory


def run_code(
    code: str,
    checks: list[dict],
    timeout_sec: int = 10,
    exercise_dir: Path | None = None,
) -> RunResult:
    """Kodu çalıştırır ve kontrolleri uygular."""
    workspace = _prepare_workspace(exercise_dir)
    code_path = workspace / "cozum.py"
    job_path = workspace / "job.json"
    result_path = workspace / "result.json"

    try:
        code_path.write_text(code, encoding="utf-8")
        job_path.write_text(
            json.dumps(
                {
                    "code_path": str(code_path),
                    "result_path": str(result_path),
                    "checks": checks,
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        command = _harness_command(job_path)

        # Windows'ta arkada siyah konsol penceresi açılmasın.
        creation_flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

        process = subprocess.Popen(
            command,
            cwd=workspace,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            creationflags=creation_flags,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        try:
            _, process_stderr = process.communicate(timeout=timeout_sec)
        except subprocess.TimeoutExpired:
            _kill_tree(process)
            return RunResult(status="timeout", timeout_sec=timeout_sec)

        if not result_path.exists():
            # harness sonucu yazamadan öldü: beklenmedik bir durum.
            return RunResult(
                status="crashed",
                stderr=(process_stderr or "").strip(),
                timeout_sec=timeout_sec,
            )

        raw = json.loads(result_path.read_text(encoding="utf-8"))
        return RunResult(
            artifacts=_rescue_artifacts(raw.get("artifacts", [])),
            status=raw.get("status", "ok"),
            stdout=raw.get("stdout", ""),
            stderr=raw.get("stderr", ""),
            truncated=raw.get("truncated", False),
            error=raw.get("error"),
            checks=[
                CheckResult(
                    type=item.get("type", ""),
                    passed=item.get("passed", False),
                    detail=item.get("detail", {}),
                    hint=item.get("hint", {}),
                )
                for item in raw.get("checks", [])
            ],
            timeout_sec=timeout_sec,
        )

    finally:
        shutil.rmtree(workspace, ignore_errors=True)
