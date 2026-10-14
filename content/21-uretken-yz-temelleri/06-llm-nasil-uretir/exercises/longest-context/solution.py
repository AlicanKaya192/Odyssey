from collections import Counter

DIALOGUES = [
    "<user> hi <assistant> hello <end>",
    "<user> bye <assistant> goodbye <end>",
    "<user> hi there <assistant> hello friend <end>",
]


def next_word(dialogues, context):
    tables = {}
    for text in dialogues:
        d = text.split()
        for i in range(1, len(d)):
            for n in range(1, min(i, 7) + 1):
                tables.setdefault(tuple(d[i - n:i]), Counter())[d[i]] += 1
    tokens = context.split()
    for n in range(min(len(tokens), 7), 0, -1):
        counts = tables.get(tuple(tokens[-n:]))
        if counts:
            return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    return ""


print(next_word(DIALOGUES, "<user> hi <assistant>"))
print(next_word(DIALOGUES, "hi there <assistant>"))
