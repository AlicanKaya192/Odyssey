def group_anagrams(words):
    groups = {}
    for word in words:
        key = "".join(sorted(word))
        groups.setdefault(key, []).append(word)
    return list(groups.values())


for group in group_anagrams(["tea", "eat", "tan", "ate", "nat", "bat"]):
    print(group)
print(group_anagrams([]))
