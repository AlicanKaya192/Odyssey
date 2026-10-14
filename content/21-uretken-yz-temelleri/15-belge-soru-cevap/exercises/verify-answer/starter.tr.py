import re

NOT_FOUND = "I could not find this in the sources."


def verify(answer, sources):
    return True


sources = ["Gift cards are valid for 3 years.", "Points expire after 12 months."]
for answer in ["Valid for 3 years. [1]", "Valid for 5 years. [1]", "Points [3]."]:
    print(verify(answer, sources))
