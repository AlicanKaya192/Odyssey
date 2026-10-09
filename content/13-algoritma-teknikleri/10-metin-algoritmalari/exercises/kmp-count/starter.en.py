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
    # Read the text once from left to right.
    return total

print(kmp_count("abababab", "abab"))
print(kmp_count("a" * 20, "aaa"))
print(kmp_count("data science", "xyz"))
