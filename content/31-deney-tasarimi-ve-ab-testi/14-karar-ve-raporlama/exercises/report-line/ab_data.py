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


def make_ramp_test(n_week1=20_000, n_week2=20_000, seed=78, lift=0.05):
    """A test whose traffic share for B was raised after the first week.

    Columns: user_id, week (1 or 2), group, bought (0/1). In week 1 B got
    10% of the users, in week 2 50%. Week 1 had a sale, so everyone bought
    more. In both weeks B truly raises buying by `lift` (relative).
    """
    rng = np.random.default_rng(seed)
    week = np.repeat([1, 2], [n_week1, n_week2])
    share_b = np.where(week == 1, 0.1, 0.5)
    group = np.where(rng.random(len(week)) < share_b, "B", "A")
    p_buy = np.where(week == 1, 0.12, 0.05)
    p_buy = np.where(group == "B", p_buy * (1 + lift), p_buy)
    bought = (rng.random(len(week)) < p_buy).astype(int)
    return pd.DataFrame({"user_id": [f"R{i:05d}" for i in range(1, len(week) + 1)], "week": week,
                         "group": group, "bought": bought})


def make_segment_test(n=40_000, seed=79, lift=0.08):
    """A 50/50 test with 16 segments, one row per user.

    Columns: user_id, group, platform (mobile / desktop), country (8
    countries), bought (0/1). Segments differ in how much they buy, but B
    truly raises buying by the same `lift` (relative) in every segment.
    """
    rng = np.random.default_rng(seed)
    countries = np.array(["TR", "DE", "FR", "UK", "US", "BR", "IN", "JP"])
    base = dict(zip(countries, [0.05, 0.07, 0.06, 0.08, 0.09, 0.04, 0.03, 0.06]))
    group = np.where(rng.random(n) < 0.5, "A", "B")
    platform = np.where(rng.random(n) < 0.6, "mobile", "desktop")
    country = rng.choice(countries, n)
    p_buy = np.array([base[c] for c in country])
    p_buy = np.where(platform == "mobile", p_buy * 0.8, p_buy)
    p_buy = np.where(group == "B", p_buy * (1 + lift), p_buy)
    bought = (rng.random(n) < p_buy).astype(int)
    return pd.DataFrame({"user_id": [f"S{i:05d}" for i in range(1, n + 1)], "group": group,
                         "platform": platform, "country": country, "bought": bought})


def make_novelty_test(n=30_000, seed=80, days=28, lasting=0.04, novelty=0.20):
    """Daily clicks of a 28-day test, one row per user per day.

    Columns: user_id, group, is_new (True for users who never saw the old
    design), day (1..days), clicks. For B the lasting effect is `lasting`
    (relative). Existing B users also get a novelty bonus that starts at
    `novelty` and halves every 3 days; new users get no novelty bonus.
    """
    rng = np.random.default_rng(seed)
    group = np.where(rng.random(n) < 0.5, "A", "B")
    is_new = rng.random(n) < 0.2
    level = rng.lognormal(0.5, 0.5, n)
    day = np.arange(1, days + 1)
    bonus = novelty * 0.5 ** ((day - 1) / 3)
    effect = np.where(group[:, None] == "B",
                      1 + lasting + np.where(is_new[:, None], 0.0, bonus[None, :]), 1.0)
    clicks = rng.poisson(level[:, None] * effect)
    ids = np.array([f"N{i:05d}" for i in range(1, n + 1)])
    return pd.DataFrame({"user_id": np.repeat(ids, days), "group": np.repeat(group, days),
                         "is_new": np.repeat(is_new, days), "day": np.tile(day, n),
                         "clicks": clicks.ravel()})


def make_market(n_cities=100, users=300, seed=81, design="user", share_b=0.5, boost=0.2):
    """A ride-sharing market where riders in a city share the same drivers.

    Columns: user_id, city, group, requested, completed. B makes riders
    request `boost` (relative) more rides. Each city has a fixed number of
    drivers; when requests exceed it, every request in the city has the
    same lower chance of being completed. design="user" assigns riders
    one by one (B with `share_b`), design="city" assigns whole cities
    (that share of the cities). The cities and riders depend only on
    `seed`, so the same seed with share_b=0 and share_b=1 gives the same
    market in an "all A" and an "all B" world.
    """
    world = np.random.default_rng([seed, 0])
    size = world.lognormal(0.0, 0.3, n_cities)
    want = world.gamma(2.0, 1.0, (n_cities, users)) * size[:, None]
    capacity = want.sum(axis=1) * world.uniform(0.85, 1.05, n_cities)
    assign = np.random.default_rng([seed, 1])
    if design == "city":
        city_b = np.zeros(n_cities, bool)
        city_b[assign.permutation(n_cities)[:round(n_cities * share_b)]] = True
        is_b = np.repeat(city_b[:, None], users, axis=1)
    else:
        is_b = assign.random((n_cities, users)) < share_b
    noise = np.random.default_rng([seed, 2])
    requested = noise.poisson(np.where(is_b, want * (1 + boost), want))
    p_done = np.minimum(1.0, capacity / np.maximum(requested.sum(axis=1), 1))
    completed = noise.binomial(requested, p_done[:, None])
    city = np.repeat([f"C{c + 1:03d}" for c in range(n_cities)], users)
    user = [f"{c}-{u + 1:03d}" for c, u in zip(city, np.tile(np.arange(users), n_cities))]
    return pd.DataFrame({"user_id": user, "city": city, "group": np.where(is_b.ravel(), "B", "A"),
                         "requested": requested.ravel(), "completed": completed.ravel()})


def make_capstone(n=40_000, seed=82, lift=0.12):
    """The capstone experiment: a lower free-shipping limit, one row per user.

    Columns: user_id, day (1..14), group, platform, pre_spend (spending in
    the four weeks before the test), bought (0/1), revenue, refunded (0/1).
    Each user has a lasting activity level that drives both pre_spend and
    buying. B truly raises buying by `lift` (relative); order sizes and
    refunds do not change.
    """
    rng = np.random.default_rng(seed)
    group = np.where(rng.random(n) < 0.5, "A", "B")
    day = rng.integers(1, 15, n)
    platform = np.where(rng.random(n) < 0.55, "mobile", "desktop")
    activity = rng.lognormal(0.0, 0.6, n)
    pre_orders = rng.poisson(activity * 1.5)
    pre_spend = np.round(pre_orders * rng.lognormal(4.0, 0.4, n) * np.sqrt(activity), 2)
    p_buy = np.clip(0.09 * activity, 0, 0.6)
    p_buy = np.where(platform == "mobile", p_buy * 0.85, p_buy)
    p_buy = np.where(group == "B", p_buy * (1 + lift), p_buy)
    bought = (rng.random(n) < p_buy).astype(int)
    revenue = np.where(bought == 1, np.round(rng.lognormal(4.0, 0.6, n) * np.sqrt(activity), 2), 0.0)
    refunded = bought * (rng.random(n) < 0.08).astype(int)
    return pd.DataFrame({"user_id": [f"K{i:05d}" for i in range(1, n + 1)], "day": day, "group": group,
                         "platform": platform, "pre_spend": pre_spend, "bought": bought,
                         "revenue": revenue, "refunded": refunded})
