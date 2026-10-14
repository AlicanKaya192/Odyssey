def score_by_outcome(results):
    return {}


RESULTS = [["sent", "sent"], ["blocked", "blocked"],
           ["handover", "sent"], ["handover", "handover"],
           ["fallback", "fallback"], ["sent", "handover"],
           ["sent", "sent"]]
for key, value in score_by_outcome(RESULTS).items():
    print(key, value)
