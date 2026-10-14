def finish(proposed, max_tokens):
    out = []
    for token in proposed:
        if len(out) == max_tokens:
            return [" ".join(out), "length"]
        if token == "<end>":
            return [" ".join(out), "stop"]
        out.append(token)
    return [" ".join(out), "length"]


print(finish(["paris", ".", "<end>", "extra"], 10))
print(finish(["the", "capital", "of", "peru"], 3))
