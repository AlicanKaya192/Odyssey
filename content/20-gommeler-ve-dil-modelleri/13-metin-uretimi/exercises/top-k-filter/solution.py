def top_k_filter(probs, k):
    kept = sorted(probs.items(), key=lambda x: -x[1])[:k]
    total = sum(p for _, p in kept)
    return {w: round(p / total, 3) for w, p in kept}

probs = {"order": 0.5, "parcel": 0.3, "box": 0.15, "app": 0.05}
for k in [2, 1]:
    result = top_k_filter(probs, k)
    print(k, " ".join(f"{w}={x}" for w, x in result.items()))
