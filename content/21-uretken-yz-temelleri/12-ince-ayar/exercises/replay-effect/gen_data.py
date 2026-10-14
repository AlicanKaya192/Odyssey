"""Data for the Generative AI exercises (read-only).

Every function uses its own random generator with a fixed seed, so the data is
the same on every computer and every run.
"""
import numpy as np

SPECIES = ("perch", "bream")

# Mean (length in cm, weight in g) and covariance of each species.
_FISH = {
    "perch": ((24.0, 310.0), ((16.0, 220.0), (220.0, 5200.0))),
    "bream": ((31.0, 560.0), ((12.0, 260.0), (260.0, 9800.0))),
}


def make_fish(n=600, seed=7):
    """Return (X, y): X is an (n, 2) array of [length_cm, weight_g], y the species names.

    About 55% perch and 45% bream; the two species overlap a little.
    """
    rng = np.random.default_rng(seed)
    labels = np.where(rng.random(n) < 0.55, "perch", "bream")
    X = np.empty((n, 2))
    for name in SPECIES:
        mask = labels == name
        mean, cov = _FISH[name]
        X[mask] = rng.multivariate_normal(mean, cov, size=mask.sum())
    return X.round(1), labels.tolist()


def load_digit_images():
    """Return (X, y): the 1797 handwritten 8x8 digits bundled with scikit-learn.

    X is (1797, 64) with pixels scaled to 0-1; y is the digit (0-9) of each image.
    """
    from sklearn.datasets import load_digits

    digits = load_digits()
    return digits.data / 16.0, digits.target.tolist()
