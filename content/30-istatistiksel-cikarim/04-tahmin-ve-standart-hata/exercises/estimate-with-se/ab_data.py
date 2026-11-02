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
