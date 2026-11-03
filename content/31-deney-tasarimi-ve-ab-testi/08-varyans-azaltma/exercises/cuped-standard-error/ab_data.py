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


def make_basket_test(n=25, seed=191):
    """A small A/B test on basket value (money per order), n orders per group.

    Columns: group ("A", "B"), basket. Basket values are very skewed:
    a few orders are huge. In truth B makes baskets 30% larger.
    """
    rng = np.random.default_rng(seed)
    a = np.round(rng.lognormal(4.6, 0.9, n), 2)
    b = np.round(rng.lognormal(4.6 + np.log(1.30), 0.9, n), 2)
    return pd.DataFrame({"group": ["A"] * n + ["B"] * n,
                         "basket": np.concatenate([a, b])})


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


def make_user_log(n=20_000, seed=71):
    """Two weeks of a shop's users before any experiment, one row per user.

    Columns: user_id ("U00001", ...), platform ("mobile" or "desktop"),
    sessions (visits), minutes (total time), bought (0/1), revenue (0 if
    nothing was bought), refunded (0/1, only buyers can refund).
    Heavy users visit more, stay longer and buy more often.
    """
    rng = np.random.default_rng(seed)
    activity = rng.lognormal(0.0, 0.8, n)
    platform = np.where(rng.random(n) < 0.6, "mobile", "desktop")
    sessions = 1 + rng.poisson(2.0 * activity)
    minutes = np.round(sessions * rng.lognormal(1.6, 0.5, n), 1)
    p_buy = np.clip(0.04 + 0.025 * sessions, 0, 0.6)
    p_buy = np.where(platform == "mobile", p_buy * 0.8, p_buy)
    bought = (rng.random(n) < p_buy).astype(int)
    revenue = np.where(bought == 1, np.round(rng.lognormal(4.2, 0.9, n), 2), 0.0)
    refunded = bought * (rng.random(n) < 0.08).astype(int)
    ids = [f"U{i:05d}" for i in range(1, n + 1)]
    return pd.DataFrame({"user_id": ids, "platform": platform, "sessions": sessions,
                         "minutes": minutes, "bought": bought, "revenue": revenue,
                         "refunded": refunded})


def make_assignment_log(n=50_000, seed=72, lost_b=0.0):
    """The logged users of a 50/50 experiment with no real effect.

    Columns: user_id, group ("A" or "B"), platform, bought (0/1).
    Users are split fairly, but with lost_b > 0 that share of B's mobile
    users who did not buy never reaches the log (a tracking bug).
    """
    rng = np.random.default_rng(seed)
    group = np.where(rng.random(n) < 0.5, "A", "B")
    platform = np.where(rng.random(n) < 0.6, "mobile", "desktop")
    p_buy = np.where(platform == "mobile", 0.10, 0.13)
    bought = (rng.random(n) < p_buy).astype(int)
    lost = ((group == "B") & (platform == "mobile") & (bought == 0)
            & (rng.random(n) < lost_b))
    ids = np.array([f"V{i:05d}" for i in range(1, n + 1)])
    keep = ~lost
    return pd.DataFrame({"user_id": ids[keep], "group": group[keep],
                         "platform": platform[keep], "bought": bought[keep]})


def make_experiment(n=30_000, seed=73, lift=0.12, days=14):
    """A finished 50/50 checkout experiment, one row per user.

    Columns: user_id, day (1..days, the day the user entered), group,
    platform, sessions (visits before the test), bought (0/1), revenue,
    refunded (0/1). In truth B raises each user's buying probability by
    `lift` (relative) and leaves order sizes and refunds unchanged.
    """
    rng = np.random.default_rng(seed)
    group = np.where(rng.random(n) < 0.5, "A", "B")
    day = rng.integers(1, days + 1, n)
    platform = np.where(rng.random(n) < 0.6, "mobile", "desktop")
    sessions = 1 + rng.poisson(2.0 * rng.lognormal(0.0, 0.8, n))
    p_buy = np.clip(0.04 + 0.025 * sessions, 0, 0.6)
    p_buy = np.where(platform == "mobile", p_buy * 0.8, p_buy)
    p_buy = np.where(group == "B", p_buy * (1 + lift), p_buy)
    bought = (rng.random(n) < p_buy).astype(int)
    revenue = np.where(bought == 1, np.round(rng.lognormal(4.2, 0.9, n), 2), 0.0)
    refunded = bought * (rng.random(n) < 0.08).astype(int)
    order = np.argsort(day, kind="stable")
    ids = np.array([f"E{i:05d}" for i in range(1, n + 1)])
    return pd.DataFrame({"user_id": ids, "day": day[order], "group": group[order],
                         "platform": platform[order], "sessions": sessions[order],
                         "bought": bought[order], "revenue": revenue[order],
                         "refunded": refunded[order]})


def make_metric_panel(n=8000, seed=75, effect=True):
    """One experiment watched through 20 metrics, one row per user.

    Columns: user_id, group, metric_01 .. metric_20. Every metric has
    mean about 10. With effect=True, B truly raises metric_01 by 3%,
    metric_02 by 2% and metric_03 by 1.5%; the other 17 do not change.
    With effect=False no metric changes (an A/A test).
    """
    rng = np.random.default_rng(seed)
    group = np.where(rng.random(n) < 0.5, "A", "B")
    lifts = np.zeros(20)
    if effect:
        lifts[:3] = [0.03, 0.02, 0.015]
    data = {"user_id": [f"M{i:05d}" for i in range(1, n + 1)], "group": group}
    for j in range(20):
        values = rng.normal(10.0, 3.0, n)
        values = np.where(group == "B", values * (1 + lifts[j]), values)
        data[f"metric_{j + 1:02d}"] = np.round(values, 3)
    return pd.DataFrame(data)


def make_engagement_test(n=20_000, seed=76, lift=0.03):
    """A test on minutes spent, one row per user.

    Columns: user_id, group, pre_minutes (the two weeks before the test),
    minutes (the two weeks of the test), sessions (visits during the
    test). Each user has a lasting activity level, so pre_minutes and
    minutes move together. B truly raises minutes by `lift` (relative);
    sessions follow minutes, so B raises them too.
    """
    rng = np.random.default_rng(seed)
    group = np.where(rng.random(n) < 0.5, "A", "B")
    activity = rng.lognormal(3.0, 0.7, n)
    pre = activity * rng.lognormal(0.0, 0.35, n)
    during = activity * rng.lognormal(0.0, 0.35, n)
    during = np.where(group == "B", during * (1 + lift), during)
    sessions = 1 + rng.poisson(during / 8)
    return pd.DataFrame({"user_id": [f"U{i:05d}" for i in range(1, n + 1)], "group": group,
                         "pre_minutes": np.round(pre, 1), "minutes": np.round(during, 1),
                         "sessions": sessions})


def make_pageviews(n=6000, seed=77, lift=0.0):
    """Page views and clicks, one row per user (users were randomized).

    Columns: user_id, group, pageviews, clicks. Each user has their own
    click rate, so the views of one user are not independent of each
    other. B truly raises every user's click rate by `lift` (relative).
    """
    rng = np.random.default_rng(seed)
    group = np.where(rng.random(n) < 0.5, "A", "B")
    rate = rng.beta(2.0, 28.0, n)
    rate = np.where(group == "B", np.clip(rate * (1 + lift), 0, 1), rate)
    pageviews = 1 + rng.poisson(rng.lognormal(1.6, 0.9, n))
    clicks = rng.binomial(pageviews, rate)
    return pd.DataFrame({"user_id": [f"P{i:05d}" for i in range(1, n + 1)], "group": group,
                         "pageviews": pageviews, "clicks": clicks})
