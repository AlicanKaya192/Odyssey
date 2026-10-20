def previous_version(history, alias):
    # Etiketin surumlerini topla, sondan geriye dogru farkli olani bul.
    pass


history = [
    ["production", 1],
    ["staging", 2],
    ["production", 3],
    ["staging", 4],
]
print(previous_version(history, "production"))
print(previous_version(history, "staging"))
print(previous_version([["production", 1]], "production"))
