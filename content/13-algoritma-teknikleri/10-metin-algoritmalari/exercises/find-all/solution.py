def find_all(text, pattern):
    found = []
    for i in range(len(text) - len(pattern) + 1):
        j = 0
        while j < len(pattern) and text[i + j] == pattern[j]:
            j += 1
        if j == len(pattern):
            found.append(i)
    return found

print(find_all("abracadabra", "abra"))
print(find_all("aaaa", "aa"))
print(find_all("data", "model"))
