from collections import Counter


def vote(answers):
    votes = Counter(a for a in answers if a is not None)
    if not votes:
        return [None, 0, 0.0]
    answer, count = votes.most_common(1)[0]
    return [answer, count, round(count / len(answers), 2)]


print(vote([193.41, 193.41, 182.16, 193.41, None]))
print(vote([None, None]))
