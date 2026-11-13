"""Paketlenmiş programın denetleyicisiyle birkaç alıştırmayı çalıştırır.

Paket derlendikten sonra (`build_exe.py`) çalıştırılır; geliştirme
ortamındaki kütüphaneler değil, **paketin içindekiler** sınanır. Alıştırma
kodu `<paket> --run-harness job.json` ile, programın kendi alıştırma
çalıştırmasıyla aynı yoldan koşuyor (`app/core/runner.py`).

Denetlenenler:

- paketin içinde katalog paketi (`catalog.json`) var mı;
- bir Python, bir makine öğrenmesi (pandas + scikit-learn) ve bir grafik
  (matplotlib, `chart.png`) alıştırması `check_exercises.bir_alistirma` ile
  geçiyor mu (çözüm, son ipucu, başlangıç kodunun geçmemesi).

Tam tur değil (bütün alıştırmalar `check_exercises.py`); sürümden önce
paketin ayakta olduğunu gösteren kısa bir duman testi.

Kullanım:
    python tools/smoke_package.py               # dist/ içindeki bu platformun paketi
    python tools/smoke_package.py <dist klasörü>
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from app.core import mpl_cache, runner  # noqa: E402
from app.core.catalog import BUNDLE_NAME  # noqa: E402
from build_exe import package_layout  # noqa: E402
from check_exercises import bir_alistirma  # noqa: E402

# (ne sınanıyor, içerik klasörüne göre alıştırma yolu)
EXERCISES = (
    ("Python", "00-python-temelleri/00-baslangic/exercises/first-program"),
    ("makine öğrenmesi", "02-makine-ogrenmesi/01-ilk-model/exercises/split-and-fit"),
    ("grafik", "01-veri-bilimi/07-gorsellestirme/exercises/trend-line"),
    # Aynı alıştırma bir kez daha: önbellek kalıcıysa ilkinden kısa sürer.
    ("grafik (yeniden)", "01-veri-bilimi/07-gorsellestirme/exercises/trend-line"),
    # LightGBM macOS'ta libomp istiyor; paketin içinde gelmezse burada düşer.
    ("LightGBM", "18-ml-kutuphaneleri/14-gradyan-boosting-kutuphaneleri/exercises/lgbm-early"),
    # Süreç havuzu: paketli programda alt süreçler denetleyicinin kendisi
    # (Windows'ta `freeze_support` ve `WINEXE` düzeltmesi gerekmişti).
    ("süreç havuzu", "11-buyuk-veri/10-paralel-isleme/exercises/primes-with-processes"),
)


def use_package(executable: Path) -> None:
    """Alıştırmalar kurulu alıştırma ortamıyla değil, paketin kendisiyle koşsun."""
    runner._harness_command = lambda job_path: [
        str(executable), runner.HARNESS_FLAG, str(job_path),
    ]


def main() -> int:
    layout = package_layout(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
    executable = layout.executable
    if not executable.is_file():
        print("Paket bulunamadı:", executable)
        return 1

    problems: list[str] = []
    catalog = layout.content / BUNDLE_NAME
    if not catalog.is_file():
        problems.append(f"katalog paketi yok: {catalog}")

    use_package(executable)
    # Program açılınca yaptığı gibi: matplotlib önbelleği (macOS). Bu betik
    # paketin dışında çalıştığı için `needed()` paketin önbellek klasörüne
    # bakamıyor; ısındırma her zaman yapılıyor, paketin denetleyicisi kendi
    # kalıcı klasörünü kullanıyor. Grafik alıştırması ondan sonra ölçülüyor.
    if sys.platform == "darwin":
        sure = mpl_cache.warm()
        if sure is not None:
            print(f"önbellek  matplotlib yazı tipleri  ({sure:.1f} sn)")
    content = PROJECT_ROOT / "content"
    for what, relative in EXERCISES:
        started = time.time()
        found = bir_alistirma(content / relative)
        state = "geçti" if not found else "DÜŞTÜ"
        print(f"{state:6} {what:18} {relative}  ({time.time() - started:.1f} sn)")
        problems += found

    print("-" * 66)
    if problems:
        for problem in problems:
            print("  -", problem)
        return 1
    print(f"Paket ayakta: {executable}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
