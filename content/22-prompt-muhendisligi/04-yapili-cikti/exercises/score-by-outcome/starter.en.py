LABELS = ["accepted", "rejected", "needs_clarification"]


def score_outcomes(pairs):
    return {}


PAIRS = [["accepted", "accepted"], ["rejected", "accepted"],
         ["rejected", "rejected"], ["needs_clarification", "accepted"],
         ["accepted", "rejected"]]
score = score_outcomes(PAIRS)
for label in LABELS:
    print(label, score.get(label))
print("false_accept", score.get("false_accept"))
