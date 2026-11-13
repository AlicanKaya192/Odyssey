"""Random Forest'ın Windows ile Mac'te neden farklı sonuç verdiğini ölçer.

`02-makine-ogrenmesi/12-genel-tekrar/review-regression` alıştırmasının
ormanını kurup her ağacın yapısını JSON'a yazar. Başka bir makinenin
dökümü verilirse ilk ayrışan ağacı ve düğümü bulur; o düğümde bütün
ayrım adaylarını kaba kuvvetle (brute force) puanlayıp en iyi ikisinin
farkını yazar. Fark yuvarlama düzeyindeyse iki makine eşit iki adaydan
farklı olanı seçiyor demektir.

Kullanım:
  forest_probe.py dump <cikti.json>
  forest_probe.py compare <bu_makine.json> <oteki.json>
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble._forest import _generate_sample_indices
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA = (ROOT / "content/02-makine-ogrenmesi/12-genel-tekrar/exercises/"
        "review-regression/cars.csv")
NUMERIC = ["age", "km", "engine"]
TEXT = ["fuel", "gearbox"]


def prepared():
    df = pd.read_csv(DATA)
    X = df[NUMERIC + TEXT]
    y = df["price"]
    X_train, _, y_train, _ = train_test_split(
        X, y, test_size=0.25, random_state=42)
    prep = ColumnTransformer([
        ("num", Pipeline([
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]), NUMERIC),
        ("cat", OneHotEncoder(handle_unknown="ignore"), TEXT),
    ], sparse_threshold=0)
    return np.asarray(prep.fit_transform(X_train), dtype=np.float64), \
        y_train.to_numpy(dtype=np.float64)


def forest(X, y):
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    return model.fit(X, y)


def digest(array) -> str:
    return hashlib.sha256(np.ascontiguousarray(array).tobytes()).hexdigest()[:16]


def dump(path: Path) -> None:
    X, y = prepared()
    model = forest(X, y)
    trees = []
    for est in model.estimators_:
        t = est.tree_
        trees.append({
            "feature": t.feature.tolist(),
            "threshold": [float(v).hex() for v in t.threshold],
            "value": digest(t.value),
        })
    info = {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "sklearn": sklearn.__version__,
        "X": digest(X),
        "y": digest(y),
        "trees": trees,
    }
    path.write_text(json.dumps(info), encoding="utf-8")
    print(f"{len(trees)} ağaç yazıldı; X {info['X']} y {info['y']}")


def node_samples(est, X, idx, node):
    """Ağacın eğitildiği örneklerden `node` düğümüne ulaşanların dizinleri."""
    path = est.decision_path(X[idx])
    return idx[path[:, node].toarray().ravel() > 0]


def candidates(X, y, rows, weights):
    """Bu satırlarla mümkün bütün ayrımları MSE azalmasına göre sıralar."""
    out = []
    for f in range(X.shape[1]):
        order = np.argsort(X[rows, f], kind="stable")
        xs, ys, ws = X[rows, f][order], y[rows][order], weights[order]
        cw, cwy, cwy2 = np.cumsum(ws), np.cumsum(ws * ys), np.cumsum(ws * ys * ys)
        total_w, total_wy, total_wy2 = cw[-1], cwy[-1], cwy2[-1]
        for i in range(len(xs) - 1):
            if xs[i] == xs[i + 1]:
                continue
            lw, rw = cw[i], total_w - cw[i]
            lwy, rwy = cwy[i], total_wy - cwy[i]
            # sklearn'ün "proxy" ölçüsü: sol²/ağırlık + sağ²/ağırlık
            proxy = lwy * lwy / lw + rwy * rwy / rw
            out.append((proxy, f, (xs[i] + xs[i + 1]) / 2))
    out.sort(key=lambda c: -c[0])
    return out


def compare(mine: Path, other: Path) -> int:
    a = json.loads(mine.read_text(encoding="utf-8"))
    b = json.loads(other.read_text(encoding="utf-8"))
    for key in ("platform", "machine", "python", "numpy", "sklearn", "X", "y"):
        print(f"{key:9} {a[key]}  |  {b[key]}")
    if a["X"] != b["X"] or a["y"] != b["y"]:
        print("Girdi verisi farklı: fark ön işlemede.")
        return 1
    X, y = prepared()
    model = forest(X, y)
    n = X.shape[0]
    same = 0
    for k, (ta, tb) in enumerate(zip(a["trees"], b["trees"])):
        if ta == tb:
            same += 1
            continue
        print(f"İlk ayrışan ağaç: {k} (öncesinde {same} ağaç aynı)")
        for node, (fa, fb, ha, hb) in enumerate(zip(
                ta["feature"], tb["feature"], ta["threshold"], tb["threshold"])):
            if (fa, ha) != (fb, hb):
                break
        else:
            print("Yapı aynı, yalnızca yaprak değerleri farklı (toplama sırası).")
            return 0
        print(f"İlk ayrışan düğüm: {node}")
        print(f"  bu makine: özellik {fa}, eşik {float.fromhex(ha)!r}")
        print(f"  öteki    : özellik {fb}, eşik {float.fromhex(hb)!r}")
        est = model.estimators_[k]
        idx = _generate_sample_indices(est.random_state, n, n)
        counts = np.bincount(idx, minlength=n).astype(np.float64)
        unique = np.flatnonzero(counts)
        rows = node_samples(est, X, unique, node)
        ranked = candidates(X, y, rows, counts[rows])
        print(f"  düğümde {len(rows)} farklı örnek; en iyi adaylar:")
        for proxy, f, thr in ranked[:4]:
            print(f"    proxy {proxy!r}  özellik {f}  eşik {thr!r}")
        if len(ranked) > 1:
            gap = ranked[0][0] - ranked[1][0]
            print(f"  en iyi iki aday arasındaki fark {gap!r} "
                  f"(göreli {gap / abs(ranked[0][0]):.3e})")
        return 0
    print(f"Bütün {same} ağaç aynı.")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[0] == "dump":
        dump(Path(argv[1]))
        return 0
    if len(argv) == 3 and argv[0] == "compare":
        return compare(Path(argv[1]), Path(argv[2]))
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
