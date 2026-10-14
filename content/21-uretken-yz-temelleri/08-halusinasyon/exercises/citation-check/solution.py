import re

SOURCES = [
    "Returns are accepted within 30 days of delivery.",
    "Standard delivery takes 3 to 5 working days.",
    "Refunds are paid within 7 days.",
]


def check_citations(answer, sources):
    results = []
    for sentence in answer.split(". "):
        cite = re.search(r"\[(\d+)\]", sentence)
        if not cite or not 1 <= int(cite.group(1)) <= len(sources):
            results.append(False)
            continue
        source = sources[int(cite.group(1)) - 1]
        claims = re.findall(r"\d+", sentence.replace(cite.group(0), ""))
        known = set(re.findall(r"\d+", source))
        results.append(all(c in known for c in claims))
    return results


answer = "Delivery takes 3 to 5 days [2]. Returns are accepted for 60 days [1]. Call us [4]."
print(check_citations(answer, SOURCES))
