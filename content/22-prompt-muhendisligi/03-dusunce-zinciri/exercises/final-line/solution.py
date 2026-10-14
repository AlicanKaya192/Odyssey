import re


def final_answer(text):
    found = re.search(r"^Answer:\s*(\d+(?:\.\d+)?)\s*$", text, flags=re.M)
    return float(found.group(1)) if found else None


print(final_answer("2 + 3 = 5\nAnswer: 5"))
print(final_answer("Answer: 12.50\nThanks!"))
print(final_answer("The answer is 7."))
