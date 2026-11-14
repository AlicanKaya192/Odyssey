"""Yavaş alıştırmaların süresini ölçer (Intel Mac'te zaman aşımı tanısı).

Her alıştırmanın çözümü denetleyiciyle tek başına çalıştırılıp süresi
yazılıyor; ardından aynı ölçüm `VECLIB_MAXIMUM_THREADS=1` ile (macOS'un
Accelerate kütüphanesi kendi iş parçacıklarını açabiliyor) tekrarlanıyor.
Zaman sınırı ölçüm için 600 sn'ye çıkarılıyor; alıştırma dosyalarına
dokunulmuyor.

Kullanım: python tools/timing_probe.py <alıştırma klasörü> ...
"""

from __future__ import annotations

import os
import platform
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.core.catalog import Exercise  # noqa: E402
from app.core.runner import run_code  # noqa: E402

MEASURE_LIMIT = 600


def measure(path: Path) -> tuple[float, str]:
    ex = Exercise.load(path)
    code = ex.solution_files("tr") if ex.is_multi_file else ex.solution_code
    start = time.perf_counter()
    result = run_code(code, ex.checks, MEASURE_LIMIT, path, language=ex.language, entry=ex.entry)
    return time.perf_counter() - start, f"{result.status} passed={result.passed}"


def main(paths: list[str]) -> int:
    print(f"{platform.platform()} {platform.machine()} çekirdek={os.cpu_count()}")
    for label, extra in (("varsayılan", {}), ("VECLIB_MAXIMUM_THREADS=1", {"VECLIB_MAXIMUM_THREADS": "1"})):
        os.environ.update(extra)
        print(f"-- {label}")
        for raw in paths:
            path = ROOT / raw
            seconds, status = measure(path)
            limit = Exercise.load(path).timeout_sec
            print(f"{path.name:18} {seconds:7.1f} sn  sınır {limit:>4}  {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
