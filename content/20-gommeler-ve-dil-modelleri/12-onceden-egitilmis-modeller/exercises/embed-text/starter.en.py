def embed_text(text, vectors):
    return []

vectors = {"parcel": [1.0, 0.0], "late": [0.0, 1.0], "box": [1.0, 1.0]}
print(embed_text("parcel late", vectors))
print(embed_text("Parcel BOX hello", vectors))
print(embed_text("hello there", vectors))
