# -*- coding: utf-8 -*-
"""Odyssey practice data for the Statistics and A/B Testing path.

Every function uses its own fixed seed, so every computer gets the
same numbers. Do not change existing functions: the lessons quote
numbers measured from them. Add a new function for a new need.
"""
import numpy as np
import pandas as pd


def make_population(n=100_000, seed=7):
    """All users of a made-up shopping app (the population).

    Columns:
      user_id  - "U000001", ...
      age      - years (18 to 75)
      visits   - visits last month (count)
      minutes  - average session length in minutes (right-skewed)
      bought   - 1 if the user bought something last month, else 0
      spend    - money spent last month (0 for users who did not buy)
      load_ms  - average page load time in milliseconds (bell-shaped)

    Heavy users (many visits) stay longer and buy more often.
    """
    rng = np.random.default_rng(seed)
    age = np.clip(np.round(rng.normal(38, 11, n)), 18, 75).astype(int)
    visits = rng.poisson(3.0, n)
    minutes = np.round(rng.lognormal(1.8 + 0.07 * visits, 0.6), 2)
    p_buy = np.clip(0.04 + 0.025 * visits, 0, 0.9)
    bought = (rng.random(n) < p_buy).astype(int)
    spend = np.where(bought == 1, np.round(rng.lognormal(4.6, 0.7, n), 2), 0.0)
    load_ms = np.round(rng.normal(850, 120, n)).astype(int)
    ids = [f"U{i:06d}" for i in range(1, n + 1)]
    return pd.DataFrame({"user_id": ids, "age": age, "visits": visits,
                         "minutes": minutes, "bought": bought, "spend": spend,
                         "load_ms": load_ms})


def make_speed_test(n=40, seed=61):
    """Page load times (ms) of n page views after a server change.

    Before the change the average was 850 ms (see make_population).
    After the change the true average is 890 ms.
    """
    rng = np.random.default_rng(seed)
    return np.round(rng.normal(890, 120, n)).astype(int)


def make_design_test(n=500, seed=62):
    """A/B test of a new page design, n users per group.

    Columns: group ("A" old design, "B" new design), minutes (average
    session length). In truth B makes sessions 10% longer.
    """
    rng = np.random.default_rng(seed)
    a = np.round(rng.lognormal(2.0, 0.6, n), 2)
    b = np.round(rng.lognormal(2.0 + np.log(1.10), 0.6, n), 2)
    return pd.DataFrame({"group": ["A"] * n + ["B"] * n,
                         "minutes": np.concatenate([a, b])})


def make_paired_speed(n=25, seed=63):
    """Load time (ms) of the same n pages before and after compressing images.

    Pages differ a lot from each other; the change saves 20 ms per page.
    Columns: page ("P01", ...), before, after.
    """
    rng = np.random.default_rng(seed)
    base = rng.normal(900, 150, n)
    before = np.round(base + rng.normal(0, 25, n)).astype(int)
    after = np.round(base - 20 + rng.normal(0, 25, n)).astype(int)
    pages = [f"P{i:02d}" for i in range(1, n + 1)]
    return pd.DataFrame({"page": pages, "before": before, "after": after})


def make_checkout_test(n=4000, seed=64):
    """A/B test of a new checkout button, n users per group.

    Columns: group ("A", "B"), bought (0/1). True rates: A 11.4%, B 13.0%.
    """
    rng = np.random.default_rng(seed)
    a = (rng.random(n) < 0.114).astype(int)
    b = (rng.random(n) < 0.130).astype(int)
    return pd.DataFrame({"group": ["A"] * n + ["B"] * n,
                         "bought": np.concatenate([a, b])})


def make_weekday_orders(n=1400, seed=65):
    """The weekday ("Mon" ... "Sun") of n orders. Weekends are a bit busier."""
    rng = np.random.default_rng(seed)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    weights = np.array([0.13, 0.13, 0.13, 0.13, 0.14, 0.17, 0.17])
    return pd.Series(rng.choice(days, size=n, p=weights), name="day")


def make_devices(n=3000, seed=66):
    """Users with their device and whether they bought.

    Columns: device ("mobile", "desktop", "tablet"), bought (0/1).
    Shares 60/30/10%; true buying rates 10%, 15%, 12%.
    """
    rng = np.random.default_rng(seed)
    device = rng.choice(["mobile", "desktop", "tablet"], size=n, p=[0.6, 0.3, 0.1])
    rate = np.select([device == "mobile", device == "desktop"], [0.10, 0.15], 0.12)
    bought = (rng.random(n) < rate).astype(int)
    return pd.DataFrame({"device": device, "bought": bought})


def make_layout_test(n=150, seed=67):
    """Four page layouts ("A", "B", "C", "D"), n users each.

    Columns: layout, minutes (time on the page, bell-shaped).
    True means: A 8.0, B 8.0, C 8.8, D 8.2; the spread is 3 in every group.
    """
    rng = np.random.default_rng(seed)
    means = {"A": 8.0, "B": 8.0, "C": 8.8, "D": 8.2}
    parts = []
    for name, mu in means.items():
        parts.append(pd.DataFrame({"layout": name,
                                   "minutes": np.round(rng.normal(mu, 3.0, n), 2)}))
    return pd.concat(parts, ignore_index=True)
