from collections import Counter

DIALOGUES = [
    "<user> hi <assistant> hello <end>",
    "<user> bye <assistant> goodbye <end>",
    "<user> hi there <assistant> hello friend <end>",
]


def next_word(dialogues, context):
    return ""


print(next_word(DIALOGUES, "<user> hi <assistant>"))
print(next_word(DIALOGUES, "hi there <assistant>"))
