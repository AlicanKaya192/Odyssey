KEYWORDS = {
    "S": ["impersonat", "pretend", "fake login", "stolen password"],
    "T": ["alter", "modif", "tamper"],
    "R": ["deny", "not logged", "nothing is logged"],
    "I": ["leak", "expose", "disclos"],
    "D": ["flood", "crash", "overload"],
    "E": ["bypass", "privilege", "become admin"],
}


def classify_threat(text):
    lowered = text.lower()
    for letter, words in KEYWORDS.items():
        if any(word in lowered for word in words):
            return letter
    return "?"

reports = [
    "attacker could impersonate a teacher",
    "grades may be altered in the database",
    "error page could expose every grade",
    "student can bypass the admin check",
    "a flood of requests could crash the site",
    "nothing is logged, so a teacher can deny it",
    "the coffee machine is slow",
]
for text in reports:
    print(classify_threat(text), text[:30])
