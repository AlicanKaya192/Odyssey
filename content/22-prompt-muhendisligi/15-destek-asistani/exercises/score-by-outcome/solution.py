def score_by_outcome(results):
    table = {}
    for outcome, expected in results:
        right, total = table.get(expected, [0, 0])
        table[expected] = [right + (outcome == expected), total + 1]
    return {key: f"{right}/{total}" for key, (right, total) in sorted(table.items())}


RESULTS = [["sent", "sent"], ["blocked", "blocked"],
           ["handover", "sent"], ["handover", "handover"],
           ["fallback", "fallback"], ["sent", "handover"],
           ["sent", "sent"]]
for key, value in score_by_outcome(RESULTS).items():
    print(key, value)
