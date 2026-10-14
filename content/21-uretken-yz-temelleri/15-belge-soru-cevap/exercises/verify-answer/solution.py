import re

NOT_FOUND = "I could not find this in the sources."


def verify(answer, sources):
    if answer == NOT_FOUND:
        return True
    cite = re.search(r"\[(\d+)\]", answer)
    if not cite or not 1 <= int(cite.group(1)) <= len(sources):
        return False
    source = sources[int(cite.group(1)) - 1]
    claims = re.findall(r"\d+", answer.replace(cite.group(0), ""))
    return all(c in re.findall(r"\d+", source) for c in claims)


sources = ["Gift cards are valid for 3 years.", "Points expire after 12 months."]
for answer in ["Valid for 3 years. [1]", "Valid for 5 years. [1]", "Points [3]."]:
    print(verify(answer, sources))
