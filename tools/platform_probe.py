"""Bir alıştırmanın çözümü Windows'ta ve Mac'te neden farklı çıkıyor?

Her durum için çözümü geçici bir kopyada çalıştırır, çıktısını ve içinde
eğitilen her karar ağacının (Random Forest'ınkiler dahil) girdisinin ve
yapısının özetini kaydeder. İki makinenin dökümü karşılaştırılınca ilk
ayrışan eğitimde girdi mi farklı (veriyi üreten hesap), yoksa aynı girdiden
farklı ağaç mı çıkıyor (ağacın kendi hesabı) görülür. Bir durum çözüme
küçük değişiklikler de uygulayabilir: aday düzeltmeler tek çalıştırmada
denenir.

Kullanım:
  platform_probe.py run <cikti.json>
  platform_probe.py compare <bu_makine.json> <oteki.json>
"""
from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

ML = "02-makine-ogrenmesi"
MLLIB = "18-ml-kutuphaneleri"
# Denetimdeki durum: hdbscan_summary(100).
HDB_SIZES = ("print(hdbscan_summary(5))",
             "print(hdbscan_summary(5))\nfor s in (40, 60, 80, 100, 120, 150):\n    print(s, hdbscan_summary(s))")
HOUSE_INT = ("+ 8 * np.minimum(df[\"floor\"], 8) + rng.normal(0, 15, 2000))",
             "+ 8 * np.minimum(df[\"floor\"], 8) + rng.normal(0, 15, 2000)).round()")
RFC = "RandomForestClassifier(n_estimators=200, random_state=42)"


def leaf(n):
    return (RFC, f"RandomForestClassifier(n_estimators=200, min_samples_leaf={n}, random_state=42)")


def opts(text):
    return (RFC, f"RandomForestClassifier(n_estimators=200, {text}, random_state=42)")


PIPE = f"{ML}/11-pipeline-ve-model-kaydetme/exercises/pipeline-in-cv"
PICK = f"{ML}/12-genel-tekrar/exercises/pick-the-model"
CASES = [
    ("pipeline-cv-leaf30", PIPE, "solution.py", [leaf(30)]),
    ("pipeline-cv-depth5", PIPE, "solution.py", [opts("max_depth=5")]),
    ("pick-model-leaf30", PICK, "solution.py", [leaf(30)]),
    ("pick-model-leaf50", PICK, "solution.py", [leaf(50)]),
    ("pick-model-depth5", PICK, "solution.py", [opts("max_depth=5")]),
    ("pick-model-depth8", PICK, "solution.py", [opts("max_depth=8")]),
]
CASES_2 = [
    # (ad, alıştırma klasörü, çözüm dosyası, [(eski, yeni), ...])
    ("cars-forest-int-price", f"{ML}/12-genel-tekrar/exercises/review-regression", "solution.py",
     [('y = df["price"]', 'y = df["price"].round()')]),
    ("pipeline-cv-leaf10", f"{ML}/11-pipeline-ve-model-kaydetme/exercises/pipeline-in-cv", "solution.py", [leaf(10)]),
    ("pipeline-cv-leaf20", f"{ML}/11-pipeline-ve-model-kaydetme/exercises/pipeline-in-cv", "solution.py", [leaf(20)]),
    ("pick-model-leaf10", f"{ML}/12-genel-tekrar/exercises/pick-the-model", "solution.py", [leaf(10)]),
    ("pick-model-leaf20", f"{ML}/12-genel-tekrar/exercises/pick-the-model", "solution.py", [leaf(20)]),
    ("rf-search-leaf10", f"{MLLIB}/05-model-secimi/exercises/random-forest-search", "solution.py",
     [("RandomForestClassifier(random_state=0)", "RandomForestClassifier(min_samples_leaf=10, random_state=0)")]),
    ("rf-search-leaf20", f"{MLLIB}/05-model-secimi/exercises/random-forest-search", "solution.py",
     [("RandomForestClassifier(random_state=0)", "RandomForestClassifier(min_samples_leaf=20, random_state=0)")]),
    ("copy-effect-int", f"{MLLIB}/15-model-aciklama/exercises/copy-effect", "solution.py", [HOUSE_INT]),
    ("perm-mae-int", f"{MLLIB}/15-model-aciklama/exercises/perm-mae", "solution.py", [HOUSE_INT]),
    ("hdbscan-sizes", f"{MLLIB}/10-kumeleme-ve-boyut-indirgeme/exercises/hdbscan-summary", "solution.py",
     [HDB_SIZES]),
]

# Çözümden önce çalışır: her ağaç eğitiminin girdisini ve sonucunu özetler,
# verinin ilk satırlarını da yazar (veri farkını görmek için).
PRELUDE = r'''
import atexit, hashlib, json, os, sys
import numpy as np

def _h(a):
    if a is None:
        return None
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()[:12]

_fits = []
try:
    from sklearn.tree import _classes
    _orig = _classes.BaseDecisionTree._fit

    def _fit(self, X, y, sample_weight=None, *a, **k):
        out = _orig(self, X, y, sample_weight, *a, **k)
        t = self.tree_
        _fits.append({
            "X": _h(np.asarray(X, dtype=np.float32)), "y": _h(np.asarray(y)),
            "w": _h(None if sample_weight is None else np.asarray(sample_weight)),
            "tree": _h(np.concatenate([t.feature.astype(np.float64), t.threshold])),
            "nodes": int(t.node_count),
        })
        return out
    _classes.BaseDecisionTree._fit = _fit
except Exception as e:
    print("odyssey-probe: no sklearn patch", e, file=sys.stderr)

@atexit.register
def _dump():
    with open(os.environ["ODYSSEY_PROBE_OUT"], "w", encoding="utf-8") as f:
        json.dump(_fits, f)
'''


def run_case(name, folder, solution, edits):
    src = CONTENT / folder
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "w"
        shutil.copytree(src, work)
        code = (work / solution).read_text(encoding="utf-8")
        for old, new in edits:
            assert old in code, (name, old)
            code = code.replace(old, new)
        (work / solution).write_text(code, encoding="utf-8")
        (work / "_probe_prelude.py").write_text(PRELUDE, encoding="utf-8")
        fits_file = Path(tmp) / "fits.json"
        runner = ("import runpy, sys; sys.path.insert(0, '.'); "
                  "exec(open('_probe_prelude.py', encoding='utf-8').read()); "
                  f"runpy.run_path({solution!r}, run_name='__main__')")
        env = dict(os.environ, ODYSSEY_PROBE_OUT=str(fits_file),
                   OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")
        proc = subprocess.run([sys.executable, "-I", "-c", runner], cwd=work, env=env,
                              capture_output=True, text=True, encoding="utf-8", timeout=600)
        fits = json.loads(fits_file.read_text(encoding="utf-8")) if fits_file.exists() else []
        return {"stdout": proc.stdout, "stderr": proc.stderr[-2000:], "code": proc.returncode,
                "fits": fits}


def run(out: Path) -> None:
    import numpy, sklearn, scipy
    info = {"platform": platform.platform(), "machine": platform.machine(),
            "numpy": numpy.__version__, "sklearn": sklearn.__version__,
            "scipy": scipy.__version__, "cases": {}}
    for name, folder, solution, edits in CASES:
        print("…", name, flush=True)
        info["cases"][name] = run_case(name, folder, solution, edits)
        print(info["cases"][name]["stdout"].strip(), flush=True)
    out.write_text(json.dumps(info), encoding="utf-8")


def compare(mine: Path, other: Path) -> int:
    a = json.loads(mine.read_text(encoding="utf-8"))
    b = json.loads(other.read_text(encoding="utf-8"))
    for key in ("platform", "machine", "numpy", "sklearn", "scipy"):
        print(f"{key:9} {a[key]}  |  {b[key]}")
    for name, ca in a["cases"].items():
        cb = b["cases"].get(name)
        if cb is None:
            print(f"\n[{name}] ötekinde yok")
            continue
        same = ca["stdout"] == cb["stdout"]
        print(f"\n[{name}] çıktı {'AYNI' if same else 'FARKLI'}")
        if not same:
            print("  bu:    ", ca["stdout"].strip().replace("\n", " | "))
            print("  öteki: ", cb["stdout"].strip().replace("\n", " | "))
        fa, fb = ca["fits"], cb["fits"]
        if len(fa) != len(fb):
            print(f"  ağaç eğitimi sayısı farklı: {len(fa)} / {len(fb)}")
        for i, (x, y) in enumerate(zip(fa, fb)):
            if x == y:
                continue
            parts = [k for k in ("X", "y", "w") if x[k] != y[k]]
            if parts:
                print(f"  ilk ayrışan eğitim {i}/{len(fa)}: GİRDİ farklı ({', '.join(parts)})")
            else:
                print(f"  ilk ayrışan eğitim {i}/{len(fa)}: girdi aynı, AĞAÇ farklı "
                      f"({x['nodes']} / {y['nodes']} düğüm)")
            break
        else:
            if fa:
                print(f"  {len(fa)} ağaç eğitiminin hepsi aynı")
    return 0


def main(argv):
    if len(argv) == 2 and argv[0] == "run":
        run(Path(argv[1]))
        return 0
    if len(argv) == 3 and argv[0] == "compare":
        return compare(Path(argv[1]), Path(argv[2]))
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
