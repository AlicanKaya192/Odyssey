import difflib


def suggest(word, options):
    matches = difflib.get_close_matches(word, options, n=1)
    if matches:
        return matches[0]
    return None

commands = ["start", "stop", "status", "restart", "help"]
print(suggest("hlep", commands))
print(suggest("xyz", commands))
