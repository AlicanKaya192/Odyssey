import math


def beam_step(beams, table, width):
    pool = []
    for score, words in beams:
        for w, p in table[words[-1]].items():
            pool.append([round(score + math.log(p), 3), words + [w]])
    pool.sort(key=lambda b: -b[0])
    return pool[:width]

table = {
    "<s>": {"my": 0.6, "the": 0.4},
    "my": {"order": 0.5, "parcel": 0.5},
    "the": {"app": 0.9, "box": 0.1},
}
beams = beam_step([[0.0, ["<s>"]]], table, 2)
for score, words in beam_step(beams, table, 2):
    print(score, words)
