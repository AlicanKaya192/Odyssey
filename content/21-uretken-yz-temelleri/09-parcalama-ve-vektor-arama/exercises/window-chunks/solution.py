def windows(text, size, overlap):
    words = text.split()
    starts = range(0, max(len(words) - overlap, 1), size - overlap)
    return [" ".join(words[i:i + size]) for i in starts]


for chunk in windows("a b c d e f g h i j", 4, 1):
    print(chunk)
