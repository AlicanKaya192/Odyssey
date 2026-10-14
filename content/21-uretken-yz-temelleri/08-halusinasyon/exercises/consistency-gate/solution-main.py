from collections import Counter
from tiny_chat import ask


def gate(country, n, threshold):
    answers = Counter(ask(country, temperature=1.0, seed=s)[0] for s in range(n))
    answer, count = sorted(answers.items(), key=lambda kv: (-kv[1], kv[0]))[0]
    return answer if count / n >= threshold else "I am not sure."


for country in ["japan", "chile"]:
    print(country, gate(country, 20, 0.6))
