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

print(prefix_table("abacab"))
print(prefix_table("aabaaab"))
print(prefix_table("abcd"))
