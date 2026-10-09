def prefix_table(pattern):
    table = [0] * len(pattern)
    k = 0
    for i in range(1, len(pattern)):
        while k > 0 and pattern[i] != pattern[k]:
            k = table[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        table[i] = k
    return table


def kmp_count(text, pattern):
    table = prefix_table(pattern)
    total, k = 0, 0
    for ch in text:
        while k > 0 and ch != pattern[k]:
            k = table[k - 1]
        if ch == pattern[k]:
            k += 1
        if k == len(pattern):
            total += 1
            k = table[k - 1]
    return total

print(kmp_count("abababab", "abab"))
print(kmp_count("a" * 20, "aaa"))
print(kmp_count("data science", "xyz"))
