"""Practice data: a shop's orders in 2024.

make_orders(n) always returns the same n rows (fixed seed), so everyone
who runs it gets the same table. Read only: you import it, you do not
change it.
"""
import numpy as np
import pandas as pd

CITIES = ["Istanbul", "Ankara", "Izmir", "Bursa", "Antalya", "Konya", "Adana", "Trabzon"]
CITY_P = [0.34, 0.16, 0.13, 0.09, 0.09, 0.07, 0.07, 0.05]
CATEGORIES = ["books", "electronics", "home", "toys", "clothing", "sports"]
CATEGORY_P = [0.22, 0.14, 0.20, 0.12, 0.22, 0.10]
MID_PRICE = [180, 2400, 450, 320, 520, 760]
PAYMENTS = ["card", "cash", "transfer"]
PAYMENT_P = [0.72, 0.08, 0.20]


def make_orders(n, seed=7):
    """n orders from 2024, in time order."""
    rng = np.random.default_rng(seed)
    cat = rng.choice(len(CATEGORIES), size=n, p=CATEGORY_P)
    price = np.round(np.array(MID_PRICE, dtype=float)[cat] * rng.lognormal(0.0, 0.35, size=n), 2)
    seconds = np.sort(rng.integers(0, 366 * 24 * 3600, size=n))
    time = pd.Timestamp("2024-01-01") + pd.to_timedelta(seconds, unit="s")
    return pd.DataFrame({
        "order_id": np.arange(1, n + 1),
        "order_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "customer_id": rng.integers(1, max(10, n // 4), size=n),
        "city": np.array(CITIES)[rng.choice(len(CITIES), size=n, p=CITY_P)],
        "category": np.array(CATEGORIES)[cat],
        "quantity": rng.choice([1, 1, 1, 1, 2, 2, 3, 4, 5], size=n),
        "unit_price": price,
        "payment": np.array(PAYMENTS)[rng.choice(len(PAYMENTS), size=n, p=PAYMENT_P)],
    })


def write_orders_csv(path, n, seed=7):
    """Writes make_orders(n) to a CSV file and returns the path."""
    make_orders(n, seed).to_csv(path, index=False)
    return path
