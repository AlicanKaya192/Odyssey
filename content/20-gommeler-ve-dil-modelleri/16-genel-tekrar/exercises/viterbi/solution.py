import math


def viterbi(words, start, trans, emit):
    tags = list(start)
    score = {t: math.log(start[t]) + math.log(emit[t][words[0]]) for t in tags}
    back = []
    for word in words[1:]:
        new, pointers = {}, {}
        for t in tags:
            prev = max(tags, key=lambda p: score[p] + math.log(trans[p][t]))
            new[t] = score[prev] + math.log(trans[prev][t]) + math.log(emit[t][word])
            pointers[t] = prev
        score = new
        back.append(pointers)
    best = max(tags, key=lambda t: score[t])
    path = [best]
    for pointers in reversed(back):
        path.append(pointers[path[-1]])
    return path[::-1]

start = {"DET": 0.8, "NOUN": 0.2}
trans = {"DET": {"DET": 0.1, "NOUN": 0.9}, "NOUN": {"DET": 0.4, "NOUN": 0.6}}
emit = {"DET": {"the": 0.9, "dog": 0.1}, "NOUN": {"the": 0.1, "dog": 0.9}}
print(viterbi(["the", "dog"], start, trans, emit))
print(viterbi(["dog", "the", "dog"], start, trans, emit))
