import pandas as pd


def flag_notes(notes, words):
    s = pd.Series(notes, dtype=object)
    pattern = "|".join(words)
    return s.str.contains(pattern, case=False, na=False).tolist()

NOTES = ["late delivery", "Delivery OK", None, "BROKEN box", "fine"]
print(flag_notes(NOTES, ["late", "broken"]))
