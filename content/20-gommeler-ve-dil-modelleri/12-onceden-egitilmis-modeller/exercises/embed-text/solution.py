def embed_text(text, vectors):
    dims = len(next(iter(vectors.values())))
    known = [vectors[w] for w in text.lower().split() if w in vectors]
    if not known:
        return [0.0] * dims
    return [round(sum(v[i] for v in known) / len(known), 3) for i in range(dims)]

vectors = {"parcel": [1.0, 0.0], "late": [0.0, 1.0], "box": [1.0, 1.0]}
print(embed_text("parcel late", vectors))
print(embed_text("Parcel BOX hello", vectors))
print(embed_text("hello there", vectors))
