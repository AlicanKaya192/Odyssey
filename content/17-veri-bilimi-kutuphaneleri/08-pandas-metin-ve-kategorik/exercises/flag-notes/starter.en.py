import pandas as pd


def flag_notes(notes, words):
    s = pd.Series(notes, dtype=object)
    return s.str.contains(words[0]).tolist()

NOTES = ["late delivery", "Delivery OK", None, "BROKEN box", "fine"]
print(flag_notes(NOTES, ["late", "broken"]))
