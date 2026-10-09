def count_prefix(words, prefixes):
    root = {"#": 0}
    for word in words:
        node = root
        node["#"] += 1
        for ch in word:
            node = node.setdefault(ch, {"#": 0})
            node["#"] += 1
    result = []
    for prefix in prefixes:
        node = root
        for ch in prefix:
            node = node.get(ch)
            if node is None:
                break
        result.append(node["#"] if node else 0)
    return result

words = ["data", "database", "dataset", "date", "deep",
         "model", "modem", "mode"]
print(count_prefix(words, ["dat", "d", "mode", "x", ""]))
