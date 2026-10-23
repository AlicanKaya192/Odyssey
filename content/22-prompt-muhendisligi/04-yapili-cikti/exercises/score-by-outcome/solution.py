LABELS = ["accepted", "rejected", "needs_clarification"]


def score_outcomes(pairs):
    score = {}
    for label in LABELS:
        cases = [got for expected, got in pairs if expected == label]
        score[label] = [cases.count(label), len(cases)]
    wrong = [e for e, g in pairs if g == "accepted" and e != "accepted"]
    score["false_accept"] = len(wrong)
    return score


PAIRS = [["accepted", "accepted"], ["rejected", "accepted"],
         ["rejected", "rejected"], ["needs_clarification", "accepted"],
         ["accepted", "rejected"]]
score = score_outcomes(PAIRS)
for label in LABELS:
    print(label, score.get(label))
print("false_accept", score.get("false_accept"))
